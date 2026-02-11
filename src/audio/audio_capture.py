"""Audio capture engine for system audio and microphone input"""

import sys
import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Callable
from threading import Thread, Event, Lock
import time

# Import platform-specific audio libraries
if sys.platform == 'win32':
    try:
        import pyaudiowpatch as pyaudio
        PYAUDIO_AVAILABLE = True
    except ImportError:
        try:
            import pyaudio
            PYAUDIO_AVAILABLE = True
        except ImportError:
            PYAUDIO_AVAILABLE = False
            pyaudio = None
else:
    PYAUDIO_AVAILABLE = False
    pyaudio = None

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    sd = None

from src.config.config_manager import AudioConfig


@dataclass
class AudioDevice:
    """Represents an audio input device"""
    id: int
    name: str
    channels: int
    sample_rate: int
    is_loopback: bool = False
    is_default: bool = False


class AudioCaptureEngine:
    """
    Handles audio capture from system output or microphone.
    
    Platform-specific implementations:
    - Windows: PyAudioWPatch for WASAPI loopback support
    - macOS/Linux: sounddevice for audio capture
    """
    
    def __init__(self, config: AudioConfig):
        """
        Initialize audio capture engine.
        
        Args:
            config: Audio configuration settings
        """
        self.config = config
        self.is_capturing = False
        self.capture_thread: Optional[Thread] = None
        self.stop_event = Event()
        self.callback: Optional[Callable[[np.ndarray], None]] = None
        self.audio_lock = Lock()
        
        # Platform-specific audio interface
        if sys.platform == 'win32':
            self.pyaudio_instance = pyaudio.PyAudio() if PYAUDIO_AVAILABLE else None
            self.stream = None
        else:
            self.stream = None
        
        # Current device
        self.current_device_id: Optional[int] = None
        
        # Audio level tracking
        self.current_audio_level: float = 0.0
        self.silence_start_time: Optional[float] = None
        self.is_paused: bool = False
        
        # Error handling and recovery
        self.reconnect_attempts: int = 0
        self.max_reconnect_attempts: int = 5
        self.reconnect_delay: float = 5.0
        self.last_error: Optional[str] = None
        self.error_callback: Optional[Callable[[str], None]] = None
        
        # Multi-source capture
        self.secondary_stream = None
        self.secondary_device_id: Optional[int] = None
        self.secondary_thread: Optional[Thread] = None
        self.secondary_stop_event = Event()
        self.primary_buffer = []
        self.secondary_buffer = []
        self.buffer_lock = Lock()
    
    def list_devices(self) -> List[AudioDevice]:
        """
        List available audio input and loopback devices.
        
        Returns:
            List of AudioDevice objects
        """
        devices = []
        
        if sys.platform == 'win32':
            devices = self._list_devices_windows()
        else:
            devices = self._list_devices_unix()
        
        return devices
    
    def _list_devices_windows(self) -> List[AudioDevice]:
        """List audio devices on Windows using PyAudioWPatch"""
        devices = []
        
        if not self.pyaudio_instance:
            return devices
        
        try:
            # Get WASAPI host API
            wasapi_info = self.pyaudio_instance.get_host_api_info_by_type(pyaudio.paWASAPI)
            
            # Get default output device for loopback
            default_output_idx = wasapi_info.get("defaultOutputDevice", -1)
            
            # Enumerate all devices
            device_count = self.pyaudio_instance.get_device_count()
            
            for i in range(device_count):
                try:
                    device_info = self.pyaudio_instance.get_device_info_by_index(i)
                    
                    # Skip devices with no input channels
                    if device_info.get("maxInputChannels", 0) <= 0:
                        continue
                    
                    # Check if this is a loopback device
                    is_loopback = device_info.get("isLoopbackDevice", False)
                    is_default = (i == default_output_idx and is_loopback)
                    
                    device = AudioDevice(
                        id=i,
                        name=device_info.get("name", f"Device {i}"),
                        channels=device_info.get("maxInputChannels", 2),
                        sample_rate=int(device_info.get("defaultSampleRate", 44100)),
                        is_loopback=is_loopback,
                        is_default=is_default
                    )
                    devices.append(device)
                    
                except Exception as e:
                    print(f"Warning: Could not query device {i}: {e}")
                    continue
        
        except Exception as e:
            print(f"Error listing Windows audio devices: {e}")
        
        return devices
    
    def _list_devices_unix(self) -> List[AudioDevice]:
        """List audio devices on macOS/Linux using sounddevice"""
        devices = []
        
        if not SOUNDDEVICE_AVAILABLE:
            return devices
        
        try:
            device_list = sd.query_devices()
            default_input = sd.default.device[0] if isinstance(sd.default.device, tuple) else sd.default.device
            
            for i, device_info in enumerate(device_list):
                # Skip devices with no input channels
                if device_info.get("max_input_channels", 0) <= 0:
                    continue
                
                device_name = device_info.get("name", f"Device {i}")
                
                # Check if this is a monitor/loopback device (Linux PulseAudio)
                is_loopback = ".monitor" in device_name.lower() or "loopback" in device_name.lower()
                
                # Check if this is BlackHole (macOS virtual audio device)
                if sys.platform == 'darwin':
                    is_loopback = is_loopback or "blackhole" in device_name.lower()
                
                is_default = (i == default_input)
                
                device = AudioDevice(
                    id=i,
                    name=device_name,
                    channels=device_info.get("max_input_channels", 2),
                    sample_rate=int(device_info.get("default_samplerate", 44100)),
                    is_loopback=is_loopback,
                    is_default=is_default
                )
                devices.append(device)
        
        except Exception as e:
            print(f"Error listing audio devices: {e}")
        
        return devices
    
    def start_capture(self, device_id: int, callback: Callable[[np.ndarray], None], error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Start capturing audio from specified device.
        
        Args:
            device_id: Device ID to capture from
            callback: Function to call with audio chunks (numpy array, float32, 16kHz)
            error_callback: Optional function to call with error messages
        
        Returns:
            True if capture started successfully, False otherwise
        """
        if self.is_capturing:
            print("Warning: Already capturing audio")
            return False
        
        self.callback = callback
        self.error_callback = error_callback
        self.current_device_id = device_id
        self.stop_event.clear()
        self.reconnect_attempts = 0
        
        # Start capture in separate thread
        self.capture_thread = Thread(target=self._capture_loop, daemon=True)
        self.is_capturing = True
        self.capture_thread.start()
        
        return True
    
    def _capture_loop(self):
        """Main audio capture loop (runs in separate thread)"""
        while not self.stop_event.is_set():
            try:
                if sys.platform == 'win32':
                    self._capture_loop_windows()
                else:
                    self._capture_loop_unix()
                
                # If we get here, capture ended normally
                break
                
            except Exception as e:
                error_msg = f"Error in capture loop: {e}"
                print(error_msg)
                self.last_error = error_msg
                
                # Notify error callback
                if self.error_callback:
                    self.error_callback(error_msg)
                
                # Attempt reconnection
                if self.reconnect_attempts < self.max_reconnect_attempts:
                    self.reconnect_attempts += 1
                    reconnect_msg = f"Attempting to reconnect ({self.reconnect_attempts}/{self.max_reconnect_attempts})..."
                    print(reconnect_msg)
                    
                    if self.error_callback:
                        self.error_callback(reconnect_msg)
                    
                    # Wait before reconnecting
                    time.sleep(self.reconnect_delay)
                    
                    # Try to restart capture
                    continue
                else:
                    # Max reconnect attempts reached
                    failure_msg = "Maximum reconnection attempts reached. Please check your audio device."
                    print(failure_msg)
                    
                    if self.error_callback:
                        self.error_callback(failure_msg)
                    
                    self.is_capturing = False
                    break
    
    def _capture_loop_windows(self):
        """Windows audio capture using PyAudioWPatch"""
        if not self.pyaudio_instance:
            error_msg = "Error: PyAudio not available"
            print(error_msg)
            if self.error_callback:
                self.error_callback(error_msg)
            raise RuntimeError(error_msg)
        
        try:
            # Check if device is available
            if not self.check_device_available(self.current_device_id):
                self.handle_device_disconnection()
                raise RuntimeError(f"Device {self.current_device_id} not available")
            
            device_info = self.pyaudio_instance.get_device_info_by_index(self.current_device_id)
            
            # Open audio stream
            self.stream = self.pyaudio_instance.open(
                format=pyaudio.paFloat32,
                channels=min(device_info["maxInputChannels"], 2),  # Stereo or mono
                rate=self.config.sample_rate,
                input=True,
                input_device_index=self.current_device_id,
                frames_per_buffer=int(self.config.sample_rate * self.config.chunk_duration)
            )
            
            print(f"Started capturing from device {self.current_device_id}")
            
            # Reset reconnect attempts on successful start
            self.reconnect_attempts = 0
            
            # Capture loop
            consecutive_errors = 0
            max_consecutive_errors = 10
            
            while not self.stop_event.is_set():
                try:
                    # Read audio chunk
                    audio_data = self.stream.read(
                        int(self.config.sample_rate * self.config.chunk_duration),
                        exception_on_overflow=False
                    )
                    
                    # Reset error counter on successful read
                    consecutive_errors = 0
                    
                    # Convert to numpy array
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Convert stereo to mono if needed
                    if len(audio_array) > self.config.sample_rate * self.config.chunk_duration:
                        audio_array = audio_array.reshape(-1, 2).mean(axis=1)
                    
                    # Update audio level
                    self._update_audio_level(audio_array)
                    
                    # Check for silence (VAD)
                    if self._should_pause_on_silence():
                        if not self.is_paused:
                            print("Pausing on silence")
                            self.is_paused = True
                        continue
                    else:
                        if self.is_paused:
                            print("Resuming from silence")
                            self.is_paused = False
                    
                    # Call callback with audio data
                    if self.callback and not self.is_paused:
                        self.callback(audio_array)
                
                except OSError as e:
                    # Device disconnection or stream error
                    consecutive_errors += 1
                    error_msg = f"Audio stream error: {e}"
                    print(error_msg)
                    
                    if consecutive_errors >= max_consecutive_errors:
                        # Likely device disconnection
                        self.handle_device_disconnection()
                        raise RuntimeError("Device disconnected")
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    consecutive_errors += 1
                    print(f"Error reading audio: {e}")
                    
                    if consecutive_errors >= max_consecutive_errors:
                        raise
                    
                    time.sleep(0.1)
        
        finally:
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
                self.stream = None
    
    def _capture_loop_unix(self):
        """macOS/Linux audio capture using sounddevice"""
        if not SOUNDDEVICE_AVAILABLE:
            error_msg = "Error: sounddevice not available"
            print(error_msg)
            if self.error_callback:
                self.error_callback(error_msg)
            raise RuntimeError(error_msg)
        
        try:
            # Check if device is available
            if not self.check_device_available(self.current_device_id):
                self.handle_device_disconnection()
                raise RuntimeError(f"Device {self.current_device_id} not available")
            
            # Audio buffer for callback
            audio_buffer = []
            buffer_lock = Lock()
            stream_error = [None]  # Use list to allow modification in callback
            
            def audio_callback(indata, frames, time_info, status):
                """Callback for sounddevice stream"""
                if status:
                    error_msg = f"Audio callback status: {status}"
                    print(error_msg)
                    stream_error[0] = error_msg
                
                with buffer_lock:
                    # Convert to mono if stereo
                    if indata.shape[1] > 1:
                        mono_data = indata.mean(axis=1)
                    else:
                        mono_data = indata[:, 0]
                    
                    audio_buffer.append(mono_data.copy())
            
            # Open audio stream
            self.stream = sd.InputStream(
                device=self.current_device_id,
                channels=2,
                samplerate=self.config.sample_rate,
                dtype=np.float32,
                blocksize=int(self.config.sample_rate * self.config.chunk_duration),
                callback=audio_callback
            )
            
            self.stream.start()
            print(f"Started capturing from device {self.current_device_id}")
            
            # Reset reconnect attempts on successful start
            self.reconnect_attempts = 0
            
            # Process buffered audio
            consecutive_errors = 0
            max_consecutive_errors = 10
            
            while not self.stop_event.is_set():
                time.sleep(0.1)
                
                # Check for stream errors
                if stream_error[0]:
                    consecutive_errors += 1
                    if consecutive_errors >= max_consecutive_errors:
                        self.handle_device_disconnection()
                        raise RuntimeError("Stream error detected")
                    stream_error[0] = None
                else:
                    consecutive_errors = 0
                
                with buffer_lock:
                    if audio_buffer:
                        # Get all buffered chunks
                        audio_array = np.concatenate(audio_buffer)
                        audio_buffer.clear()
                        
                        # Update audio level
                        self._update_audio_level(audio_array)
                        
                        # Check for silence (VAD)
                        if self._should_pause_on_silence():
                            if not self.is_paused:
                                print("Pausing on silence")
                                self.is_paused = True
                            continue
                        else:
                            if self.is_paused:
                                print("Resuming from silence")
                                self.is_paused = False
                        
                        # Call callback with audio data
                        if self.callback and not self.is_paused:
                            self.callback(audio_array)
        
        finally:
            if self.stream:
                try:
                    self.stream.stop()
                    self.stream.close()
                except:
                    pass
                self.stream = None
    
    def stop_capture(self):
        """Stop audio capture"""
        if not self.is_capturing:
            return
        
        print("Stopping audio capture")
        self.stop_event.set()
        
        # Stop secondary capture if active
        if self.secondary_device_id is not None:
            self.secondary_stop_event.set()
            if self.secondary_thread:
                self.secondary_thread.join(timeout=2.0)
            self.secondary_device_id = None
            self.secondary_thread = None
        
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
        
        self.is_capturing = False
        self.callback = None
        self.current_device_id = None
        self.is_paused = False
        self.silence_start_time = None
        
        # Clear buffers
        with self.audio_lock:
            self.primary_buffer.clear()
            self.secondary_buffer.clear()
    
    def set_device(self, device_id: int):
        """
        Switch to a different audio device without restarting the application.
        
        Args:
            device_id: New device ID to switch to
        """
        if not self.is_capturing:
            self.current_device_id = device_id
            return
        
        # Save callback
        saved_callback = self.callback
        
        # Stop current capture
        self.stop_capture()
        
        # Start capture with new device
        if saved_callback:
            self.start_capture(device_id, saved_callback)
    
    def start_multi_source_capture(self, device_ids: List[int], callback: Callable[[np.ndarray], None]) -> bool:
        """
        Start capturing audio from multiple sources simultaneously and mix them.
        
        Args:
            device_ids: List of device IDs to capture from
            callback: Function to call with mixed audio chunks
        
        Returns:
            True if capture started successfully, False otherwise
        """
        if len(device_ids) == 0:
            print("Error: No devices specified")
            return False
        
        if len(device_ids) == 1:
            # Single device, use normal capture
            return self.start_capture(device_ids[0], callback)
        
        if self.is_capturing:
            print("Warning: Already capturing audio")
            return False
        
        # Start primary device
        primary_device = device_ids[0]
        secondary_device = device_ids[1]
        
        # Audio buffers for mixing
        self.primary_buffer = []
        self.secondary_buffer = []
        self.buffer_lock = Lock()
        
        # Callback for primary device
        def primary_callback(audio_data: np.ndarray):
            with self.buffer_lock:
                self.primary_buffer.append(audio_data)
                self._mix_and_callback(callback)
        
        # Start primary capture
        self.callback = primary_callback
        self.current_device_id = primary_device
        self.stop_event.clear()
        
        self.capture_thread = Thread(target=self._capture_loop, daemon=True)
        self.is_capturing = True
        self.capture_thread.start()
        
        # Start secondary capture in separate thread
        self.secondary_device_id = secondary_device
        self.secondary_stop_event = Event()
        self.secondary_thread = Thread(
            target=self._secondary_capture_loop,
            args=(secondary_device,),
            daemon=True
        )
        self.secondary_thread.start()
        
        return True
    
    def _secondary_capture_loop(self, device_id: int):
        """Capture loop for secondary audio source"""
        try:
            if sys.platform == 'win32':
                self._secondary_capture_windows(device_id)
            else:
                self._secondary_capture_unix(device_id)
        except Exception as e:
            print(f"Error in secondary capture loop: {e}")
    
    def _secondary_capture_windows(self, device_id: int):
        """Windows secondary audio capture"""
        if not self.pyaudio_instance:
            return
        
        try:
            device_info = self.pyaudio_instance.get_device_info_by_index(device_id)
            
            self.secondary_stream = self.pyaudio_instance.open(
                format=pyaudio.paFloat32,
                channels=min(device_info["maxInputChannels"], 2),
                rate=self.config.sample_rate,
                input=True,
                input_device_index=device_id,
                frames_per_buffer=int(self.config.sample_rate * self.config.chunk_duration)
            )
            
            print(f"Started secondary capture from device {device_id}")
            
            while not self.secondary_stop_event.is_set():
                try:
                    audio_data = self.secondary_stream.read(
                        int(self.config.sample_rate * self.config.chunk_duration),
                        exception_on_overflow=False
                    )
                    
                    audio_array = np.frombuffer(audio_data, dtype=np.float32)
                    
                    # Convert stereo to mono if needed
                    if len(audio_array) > self.config.sample_rate * self.config.chunk_duration:
                        audio_array = audio_array.reshape(-1, 2).mean(axis=1)
                    
                    with self.buffer_lock:
                        self.secondary_buffer.append(audio_array)
                
                except Exception as e:
                    print(f"Error reading secondary audio: {e}")
                    time.sleep(0.1)
        
        finally:
            if self.secondary_stream:
                self.secondary_stream.stop_stream()
                self.secondary_stream.close()
                self.secondary_stream = None
    
    def _secondary_capture_unix(self, device_id: int):
        """macOS/Linux secondary audio capture"""
        if not SOUNDDEVICE_AVAILABLE:
            return
        
        try:
            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(f"Secondary audio callback status: {status}")
                
                # Convert to mono if stereo
                if indata.shape[1] > 1:
                    mono_data = indata.mean(axis=1)
                else:
                    mono_data = indata[:, 0]
                
                with self.buffer_lock:
                    self.secondary_buffer.append(mono_data.copy())
            
            self.secondary_stream = sd.InputStream(
                device=device_id,
                channels=2,
                samplerate=self.config.sample_rate,
                dtype=np.float32,
                blocksize=int(self.config.sample_rate * self.config.chunk_duration),
                callback=audio_callback
            )
            
            self.secondary_stream.start()
            print(f"Started secondary capture from device {device_id}")
            
            # Keep thread alive
            while not self.secondary_stop_event.is_set():
                time.sleep(0.1)
        
        finally:
            if self.secondary_stream:
                self.secondary_stream.stop()
                self.secondary_stream.close()
                self.secondary_stream = None
    
    def _mix_and_callback(self, callback: Callable[[np.ndarray], None]):
        """Mix audio from primary and secondary buffers and call callback"""
        if not self.primary_buffer or not self.secondary_buffer:
            return
        
        # Get one chunk from each buffer
        primary_chunk = self.primary_buffer.pop(0)
        secondary_chunk = self.secondary_buffer.pop(0)
        
        # Ensure same length
        min_len = min(len(primary_chunk), len(secondary_chunk))
        primary_chunk = primary_chunk[:min_len]
        secondary_chunk = secondary_chunk[:min_len]
        
        # Mix audio (average)
        mixed_audio = (primary_chunk + secondary_chunk) / 2.0
        
        # Call callback with mixed audio
        callback(mixed_audio)
    
    def check_device_available(self, device_id: int) -> bool:
        """
        Check if a device is still available.
        
        Args:
            device_id: Device ID to check
        
        Returns:
            True if device is available, False otherwise
        """
        devices = self.list_devices()
        return any(d.id == device_id for d in devices)
    
    def detect_device_changes(self) -> bool:
        """
        Detect if the current device has been disconnected.
        
        Returns:
            True if device change detected, False otherwise
        """
        if self.current_device_id is None:
            return False
        
        return not self.check_device_available(self.current_device_id)
    
    def handle_device_disconnection(self):
        """Handle device disconnection gracefully"""
        if not self.is_capturing:
            return
        
        error_msg = f"Audio device {self.current_device_id} disconnected"
        print(error_msg)
        self.last_error = error_msg
        
        if self.error_callback:
            self.error_callback(error_msg)
        
        # Stop current capture
        self.stop_capture()
        
        # Notify user to reconfigure
        if self.error_callback:
            self.error_callback("Please select a different audio device in settings")
    
    def get_audio_level(self) -> float:
        """
        Get current audio input level.
        
        Returns:
            Audio level from 0.0 (silence) to 1.0 (maximum)
        """
        return self.current_audio_level
    
    def _update_audio_level(self, audio_array: np.ndarray):
        """Update current audio level from audio data"""
        if len(audio_array) > 0:
            # Calculate RMS amplitude
            rms = np.sqrt(np.mean(audio_array ** 2))
            self.current_audio_level = float(min(rms, 1.0))
    
    def _should_pause_on_silence(self) -> bool:
        """Check if capture should pause due to silence"""
        if self.current_audio_level < self.config.vad_threshold:
            # Audio is below threshold
            if self.silence_start_time is None:
                self.silence_start_time = time.time()
            else:
                # Check if silence duration exceeded
                silence_duration = time.time() - self.silence_start_time
                if silence_duration > 3.0:  # 3 seconds of silence
                    return True
        else:
            # Audio detected, reset silence timer
            self.silence_start_time = None
        
        return False
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop_capture()
        
        if sys.platform == 'win32' and self.pyaudio_instance:
            self.pyaudio_instance.terminate()
