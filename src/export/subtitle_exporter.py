"""Subtitle export functionality for SRT and VTT formats"""

from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class SubtitleEntry:
    """Represents a single subtitle entry"""
    text: str
    start_time: float  # seconds
    end_time: float    # seconds
    translated_text: Optional[str] = None


class SubtitleExporter:
    """Exports captions to SRT or VTT subtitle formats"""
    
    def __init__(self, output_path: str, format: str = "srt"):
        """
        Initialize subtitle exporter.
        
        Args:
            output_path: Path to output subtitle file
            format: Subtitle format - "srt" or "vtt"
        
        Raises:
            ValueError: If format is not "srt" or "vtt"
        """
        if format not in ["srt", "vtt"]:
            raise ValueError(f"Unsupported format: {format}. Must be 'srt' or 'vtt'")
        
        self.output_path = Path(output_path)
        self.format = format
        self.entries: List[SubtitleEntry] = []
        self.subtitle_index = 1
        self._file_handle = None
        self._is_finalized = False
        
        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def add_subtitle(self, text: str, start_time: float, end_time: float, 
                     translated_text: Optional[str] = None) -> None:
        """
        Add a subtitle entry.
        
        Args:
            text: Original subtitle text
            start_time: Start time in seconds
            end_time: End time in seconds
            translated_text: Optional translated text for dual-language export
        """
        if self._is_finalized:
            raise RuntimeError("Cannot add subtitles after finalization")
        
        entry = SubtitleEntry(
            text=text,
            start_time=start_time,
            end_time=end_time,
            translated_text=translated_text
        )
        self.entries.append(entry)
    
    def _format_timestamp_srt(self, seconds: float) -> str:
        """
        Format timestamp for SRT format (HH:MM:SS,mmm).
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp string
        """
        # Round to millisecond precision to avoid truncation errors
        total_ms = round(seconds * 1000)
        
        hours = total_ms // 3600000
        total_ms %= 3600000
        
        minutes = total_ms // 60000
        total_ms %= 60000
        
        secs = total_ms // 1000
        millis = total_ms % 1000
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def _format_timestamp_vtt(self, seconds: float) -> str:
        """
        Format timestamp for VTT format (HH:MM:SS.mmm).
        
        Args:
            seconds: Time in seconds
            
        Returns:
            Formatted timestamp string
        """
        # Round to millisecond precision to avoid truncation errors
        total_ms = round(seconds * 1000)
        
        hours = total_ms // 3600000
        total_ms %= 3600000
        
        minutes = total_ms // 60000
        total_ms %= 60000
        
        secs = total_ms // 1000
        millis = total_ms % 1000
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    def _write_srt_entry(self, f, entry: SubtitleEntry, index: int) -> None:
        """Write a single SRT entry to file"""
        f.write(f"{index}\n")
        f.write(f"{self._format_timestamp_srt(entry.start_time)} --> ")
        f.write(f"{self._format_timestamp_srt(entry.end_time)}\n")
        
        # Write original text
        f.write(f"{entry.text}\n")
        
        # Write translated text if available (dual-language)
        if entry.translated_text:
            f.write(f"{entry.translated_text}\n")
        
        f.write("\n")
    
    def _write_vtt_entry(self, f, entry: SubtitleEntry) -> None:
        """Write a single VTT entry to file"""
        f.write(f"{self._format_timestamp_vtt(entry.start_time)} --> ")
        f.write(f"{self._format_timestamp_vtt(entry.end_time)}\n")
        
        # Write original text
        f.write(f"{entry.text}\n")
        
        # Write translated text if available (dual-language)
        if entry.translated_text:
            f.write(f"{entry.translated_text}\n")
        
        f.write("\n")
    
    def finalize(self) -> None:
        """
        Write all subtitle entries to file and close it.
        This should be called when the caption session ends.
        """
        if self._is_finalized:
            return  # Already finalized
        
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                if self.format == "vtt":
                    # VTT files start with "WEBVTT" header
                    f.write("WEBVTT\n\n")
                
                # Write all entries
                for idx, entry in enumerate(self.entries, start=1):
                    if self.format == "srt":
                        self._write_srt_entry(f, entry, idx)
                    else:  # vtt
                        self._write_vtt_entry(f, entry)
            
            self._is_finalized = True
        except IOError as e:
            raise IOError(f"Failed to write subtitle file: {e}")
    
    def is_finalized(self) -> bool:
        """Check if the subtitle file has been finalized"""
        return self._is_finalized
    
    def get_entry_count(self) -> int:
        """Get the number of subtitle entries"""
        return len(self.entries)
    
    def clear(self) -> None:
        """Clear all subtitle entries (useful for starting a new session)"""
        if self._is_finalized:
            raise RuntimeError("Cannot clear after finalization")
        self.entries.clear()
        self.subtitle_index = 1

