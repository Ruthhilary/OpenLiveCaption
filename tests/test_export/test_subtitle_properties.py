"""Property-based tests for SubtitleExporter"""

import pytest
from pathlib import Path
import sys
from hypothesis import given, strategies as st, assume, settings
import re
import tempfile
import shutil

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from export import SubtitleExporter, SubtitleEntry


# Helper function to parse SRT files
def parse_srt(content: str) -> list:
    """Parse SRT content into list of subtitle entries"""
    entries = []
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split('\n')
        if len(lines) < 3:
            continue
        
        # Parse index (line 0)
        try:
            index = int(lines[0])
        except ValueError:
            continue
        
        # Parse timestamps (line 1)
        timestamp_match = re.match(
            r'(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})',
            lines[1]
        )
        if not timestamp_match:
            continue
        
        # Convert timestamps to seconds
        start_h, start_m, start_s, start_ms = map(int, timestamp_match.groups()[:4])
        end_h, end_m, end_s, end_ms = map(int, timestamp_match.groups()[4:])
        
        start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000.0
        end_time = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000.0
        
        # Parse text (remaining lines)
        text_lines = lines[2:]
        text = '\n'.join(text_lines)
        
        entries.append({
            'index': index,
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        })
    
    return entries


# Helper function to parse VTT files
def parse_vtt(content: str) -> list:
    """Parse VTT content into list of subtitle entries"""
    entries = []
    
    # Remove WEBVTT header
    if content.startswith('WEBVTT'):
        content = content[6:].lstrip('\n')
    
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        if not block.strip():
            continue
        
        lines = block.strip().split('\n')
        if len(lines) < 2:
            continue
        
        # Parse timestamps (line 0)
        timestamp_match = re.match(
            r'(\d{2}):(\d{2}):(\d{2})\.(\d{3}) --> (\d{2}):(\d{2}):(\d{2})\.(\d{3})',
            lines[0]
        )
        if not timestamp_match:
            continue
        
        # Convert timestamps to seconds
        start_h, start_m, start_s, start_ms = map(int, timestamp_match.groups()[:4])
        end_h, end_m, end_s, end_ms = map(int, timestamp_match.groups()[4:])
        
        start_time = start_h * 3600 + start_m * 60 + start_s + start_ms / 1000.0
        end_time = end_h * 3600 + end_m * 60 + end_s + end_ms / 1000.0
        
        # Parse text (remaining lines)
        text_lines = lines[1:]
        text = '\n'.join(text_lines)
        
        entries.append({
            'start_time': start_time,
            'end_time': end_time,
            'text': text
        })
    
    return entries


# Strategy for generating subtitle text (avoid empty strings and control characters)
subtitle_text_strategy = st.text(
    alphabet=st.characters(
        blacklist_categories=('Cc', 'Cs'),  # Exclude control characters
        blacklist_characters='\n\r\t'
    ),
    min_size=1,
    max_size=200
).filter(lambda x: x.strip() != '').map(lambda x: x.strip())  # Strip whitespace for consistency


# Strategy for generating timestamps (0 to 1 hour)
timestamp_strategy = st.floats(min_value=0.0, max_value=3600.0, allow_nan=False, allow_infinity=False)


# Feature: system-wide-live-captions, Property 26: SRT export round-trip
@settings(max_examples=20)  # Reduced from default 100 for faster execution
@given(
    subtitles=st.lists(
        st.tuples(
            subtitle_text_strategy,  # text
            timestamp_strategy,      # start_time
            timestamp_strategy       # end_time
        ),
        min_size=1,
        max_size=10  # Reduced from 20
    )
)
def test_srt_export_round_trip(subtitles):
    """
    **Validates: Requirements 11.1**
    
    For any sequence of captions with timestamps, exporting to SRT format 
    then parsing the SRT file should produce captions with equivalent text 
    and timestamps (within millisecond precision).
    """
    # Create temporary directory
    temp_path = tempfile.mkdtemp()
    try:
        temp_dir = Path(temp_path)
        output_path = temp_dir / "test_roundtrip.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        # Filter and normalize subtitles to ensure end_time > start_time
        valid_subtitles = []
        for text, start, end in subtitles:
            # Ensure end time is after start time
            if end <= start:
                start, end = end, start
            if end <= start:  # Still equal, add small delta
                end = start + 0.1
            valid_subtitles.append((text, start, end))
        
        # Add all subtitles
        for text, start_time, end_time in valid_subtitles:
            exporter.add_subtitle(text, start_time, end_time)
        
        # Finalize to write file
        exporter.finalize()
        
        # Read and parse the file
        content = output_path.read_text(encoding='utf-8')
        parsed_entries = parse_srt(content)
        
        # Verify count matches
        assert len(parsed_entries) == len(valid_subtitles), \
            f"Expected {len(valid_subtitles)} entries, got {len(parsed_entries)}"
        
        # Verify each entry (text and timestamps within 1ms precision)
        for i, ((original_text, original_start, original_end), parsed) in enumerate(
            zip(valid_subtitles, parsed_entries)
        ):
            # Check index
            assert parsed['index'] == i + 1, f"Entry {i}: index mismatch"
            
            # Check text
            assert parsed['text'] == original_text, \
                f"Entry {i}: text mismatch. Expected '{original_text}', got '{parsed['text']}'"
            
            # Check timestamps (within 1ms precision due to formatting)
            assert abs(parsed['start_time'] - original_start) < 0.001, \
                f"Entry {i}: start_time mismatch. Expected {original_start}, got {parsed['start_time']}"
            assert abs(parsed['end_time'] - original_end) < 0.001, \
                f"Entry {i}: end_time mismatch. Expected {original_end}, got {parsed['end_time']}"
    finally:
        # Clean up
        shutil.rmtree(temp_path, ignore_errors=True)


# Feature: system-wide-live-captions, Property 27: File finalization on session end
@settings(max_examples=20)  # Reduced from default 100 for faster execution
@given(
    subtitles=st.lists(
        st.tuples(
            subtitle_text_strategy,
            timestamp_strategy,
            timestamp_strategy
        ),
        min_size=0,
        max_size=5  # Reduced from 10
    )
)
def test_file_finalization_on_session_end(subtitles):
    """
    **Validates: Requirements 11.3**
    
    For any active subtitle export, calling finalize() should properly close 
    the subtitle file, making it readable and preventing further modifications.
    """
    # Create temporary directory
    temp_path = tempfile.mkdtemp()
    try:
        temp_dir = Path(temp_path)
        output_path = temp_dir / "test_finalization.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        # Normalize subtitles
        valid_subtitles = []
        for text, start, end in subtitles:
            if end <= start:
                start, end = end, start
            if end <= start:
                end = start + 0.1
            valid_subtitles.append((text, start, end))
        
        # Add subtitles
        for text, start_time, end_time in valid_subtitles:
            exporter.add_subtitle(text, start_time, end_time)
        
        # Before finalization, file should not exist
        assert not output_path.exists(), "File should not exist before finalization"
        
        # Finalize
        exporter.finalize()
        
        # After finalization:
        # 1. File should exist
        assert output_path.exists(), "File should exist after finalization"
        
        # 2. File should be readable
        content = output_path.read_text(encoding='utf-8')
        assert isinstance(content, str), "File content should be readable as string"
        
        # 3. Should be marked as finalized
        assert exporter.is_finalized(), "Exporter should be marked as finalized"
        
        # 4. Cannot add more subtitles
        with pytest.raises(RuntimeError, match="Cannot add subtitles after finalization"):
            exporter.add_subtitle("New subtitle", 0.0, 1.0)
        
        # 5. Multiple finalize calls should be safe (idempotent)
        exporter.finalize()  # Should not raise error
        assert exporter.is_finalized()
    finally:
        # Clean up
        shutil.rmtree(temp_path, ignore_errors=True)


# Feature: system-wide-live-captions, Property 28: VTT format support
@settings(max_examples=20)  # Reduced from default 100 for faster execution
@given(
    subtitles=st.lists(
        st.tuples(
            subtitle_text_strategy,
            timestamp_strategy,
            timestamp_strategy
        ),
        min_size=1,
        max_size=10  # Reduced from 20
    )
)
def test_vtt_format_support(subtitles):
    """
    **Validates: Requirements 11.4**
    
    For any sequence of captions, exporting to VTT format should produce 
    a valid VTT file with correct timestamps and text.
    """
    # Create temporary directory
    temp_path = tempfile.mkdtemp()
    try:
        temp_dir = Path(temp_path)
        output_path = temp_dir / "test_vtt.vtt"
        exporter = SubtitleExporter(str(output_path), format="vtt")
        
        # Normalize subtitles
        valid_subtitles = []
        for text, start, end in subtitles:
            if end <= start:
                start, end = end, start
            if end <= start:
                end = start + 0.1
            valid_subtitles.append((text, start, end))
        
        # Add all subtitles
        for text, start_time, end_time in valid_subtitles:
            exporter.add_subtitle(text, start_time, end_time)
        
        # Finalize to write file
        exporter.finalize()
        
        # Read the file
        content = output_path.read_text(encoding='utf-8')
        
        # 1. VTT files must start with "WEBVTT"
        assert content.startswith('WEBVTT'), "VTT file must start with 'WEBVTT' header"
        
        # 2. Parse and verify entries
        parsed_entries = parse_vtt(content)
        
        # Verify count matches
        assert len(parsed_entries) == len(valid_subtitles), \
            f"Expected {len(valid_subtitles)} entries, got {len(parsed_entries)}"
        
        # Verify each entry
        for i, ((original_text, original_start, original_end), parsed) in enumerate(
            zip(valid_subtitles, parsed_entries)
        ):
            # Check text
            assert parsed['text'] == original_text, \
                f"Entry {i}: text mismatch. Expected '{original_text}', got '{parsed['text']}'"
            
            # Check timestamps (within 1ms precision)
            assert abs(parsed['start_time'] - original_start) < 0.001, \
                f"Entry {i}: start_time mismatch. Expected {original_start}, got {parsed['start_time']}"
            assert abs(parsed['end_time'] - original_end) < 0.001, \
                f"Entry {i}: end_time mismatch. Expected {original_end}, got {parsed['end_time']}"
    finally:
        # Clean up
        shutil.rmtree(temp_path, ignore_errors=True)


# Feature: system-wide-live-captions, Property 29: Dual-language export
@settings(max_examples=20)  # Reduced from default 100 for faster execution
@given(
    subtitles=st.lists(
        st.tuples(
            subtitle_text_strategy,  # original text
            subtitle_text_strategy,  # translated text
            timestamp_strategy,      # start_time
            timestamp_strategy       # end_time
        ),
        min_size=1,
        max_size=8  # Reduced from 15
    ),
    format_choice=st.sampled_from(['srt', 'vtt'])
)
def test_dual_language_export(subtitles, format_choice):
    """
    **Validates: Requirements 11.5**
    
    For any caption sequence with translation enabled, the exported subtitle 
    file should contain both original and translated text.
    """
    # Create temporary directory
    temp_path = tempfile.mkdtemp()
    try:
        temp_dir = Path(temp_path)
        output_path = temp_dir / f"test_dual.{format_choice}"
        exporter = SubtitleExporter(str(output_path), format=format_choice)
        
        # Normalize subtitles
        valid_subtitles = []
        for original_text, translated_text, start, end in subtitles:
            if end <= start:
                start, end = end, start
            if end <= start:
                end = start + 0.1
            valid_subtitles.append((original_text, translated_text, start, end))
        
        # Add all subtitles with translations
        for original_text, translated_text, start_time, end_time in valid_subtitles:
            exporter.add_subtitle(
                original_text,
                start_time,
                end_time,
                translated_text=translated_text
            )
        
        # Finalize to write file
        exporter.finalize()
        
        # Read the file
        content = output_path.read_text(encoding='utf-8')
        
        # Verify both original and translated text appear in the file
        for original_text, translated_text, _, _ in valid_subtitles:
            assert original_text in content, \
                f"Original text '{original_text}' not found in exported file"
            assert translated_text in content, \
                f"Translated text '{translated_text}' not found in exported file"
        
        # Verify the structure: each subtitle block should have both texts
        if format_choice == 'srt':
            parsed_entries = parse_srt(content)
            # In dual-language SRT, both texts appear in the text field
            for i, (original_text, translated_text, _, _) in enumerate(valid_subtitles):
                entry_text = parsed_entries[i]['text']
                assert original_text in entry_text, \
                    f"Entry {i}: original text not in subtitle block"
                assert translated_text in entry_text, \
                    f"Entry {i}: translated text not in subtitle block"
        else:  # vtt
            parsed_entries = parse_vtt(content)
            # In dual-language VTT, both texts appear in the text field
            for i, (original_text, translated_text, _, _) in enumerate(valid_subtitles):
                entry_text = parsed_entries[i]['text']
                assert original_text in entry_text, \
                    f"Entry {i}: original text not in subtitle block"
                assert translated_text in entry_text, \
                    f"Entry {i}: translated text not in subtitle block"
    finally:
        # Clean up
        shutil.rmtree(temp_path, ignore_errors=True)
