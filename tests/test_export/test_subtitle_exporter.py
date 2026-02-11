"""Unit tests for SubtitleExporter"""

import pytest
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from export import SubtitleExporter, SubtitleEntry


class TestSubtitleExporter:
    """Unit tests for SubtitleExporter functionality"""
    
    def test_create_srt_exporter(self, temp_dir):
        """Test creating SRT exporter"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        assert exporter.output_path == output_path
        assert exporter.format == "srt"
        assert exporter.get_entry_count() == 0
        assert not exporter.is_finalized()
    
    def test_create_vtt_exporter(self, temp_dir):
        """Test creating VTT exporter"""
        output_path = temp_dir / "test.vtt"
        exporter = SubtitleExporter(str(output_path), format="vtt")
        
        assert exporter.output_path == output_path
        assert exporter.format == "vtt"
        assert exporter.get_entry_count() == 0
    
    def test_invalid_format_raises_error(self, temp_dir):
        """Test that invalid format raises ValueError"""
        output_path = temp_dir / "test.txt"
        
        with pytest.raises(ValueError, match="Unsupported format"):
            SubtitleExporter(str(output_path), format="txt")
    
    def test_add_subtitle_entry(self, temp_dir):
        """Test adding subtitle entries"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("Hello world", 0.0, 2.0)
        assert exporter.get_entry_count() == 1
        
        exporter.add_subtitle("Second subtitle", 2.0, 4.0)
        assert exporter.get_entry_count() == 2
    
    def test_add_subtitle_with_translation(self, temp_dir):
        """Test adding subtitle with translation"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle(
            "Hello world",
            0.0,
            2.0,
            translated_text="Hola mundo"
        )
        
        assert exporter.get_entry_count() == 1
        assert exporter.entries[0].translated_text == "Hola mundo"
    
    def test_srt_timestamp_formatting(self, temp_dir):
        """Test SRT timestamp format (HH:MM:SS,mmm)"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        # Test various timestamps
        assert exporter._format_timestamp_srt(0.0) == "00:00:00,000"
        assert exporter._format_timestamp_srt(1.5) == "00:00:01,500"
        assert exporter._format_timestamp_srt(65.123) == "00:01:05,123"
        assert exporter._format_timestamp_srt(3661.456) == "01:01:01,456"
    
    def test_vtt_timestamp_formatting(self, temp_dir):
        """Test VTT timestamp format (HH:MM:SS.mmm)"""
        output_path = temp_dir / "test.vtt"
        exporter = SubtitleExporter(str(output_path), format="vtt")
        
        # Test various timestamps
        assert exporter._format_timestamp_vtt(0.0) == "00:00:00.000"
        assert exporter._format_timestamp_vtt(1.5) == "00:00:01.500"
        assert exporter._format_timestamp_vtt(65.123) == "00:01:05.123"
        assert exporter._format_timestamp_vtt(3661.456) == "01:01:01.456"
    
    def test_finalize_srt_file(self, temp_dir):
        """Test finalizing SRT file"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("First subtitle", 0.0, 2.0)
        exporter.add_subtitle("Second subtitle", 2.0, 4.0)
        exporter.finalize()
        
        assert exporter.is_finalized()
        assert output_path.exists()
        
        # Read and verify content
        content = output_path.read_text(encoding='utf-8')
        assert "1\n" in content
        assert "00:00:00,000 --> 00:00:02,000" in content
        assert "First subtitle" in content
        assert "2\n" in content
        assert "00:00:02,000 --> 00:00:04,000" in content
        assert "Second subtitle" in content
    
    def test_finalize_vtt_file(self, temp_dir):
        """Test finalizing VTT file"""
        output_path = temp_dir / "test.vtt"
        exporter = SubtitleExporter(str(output_path), format="vtt")
        
        exporter.add_subtitle("First subtitle", 0.0, 2.0)
        exporter.add_subtitle("Second subtitle", 2.0, 4.0)
        exporter.finalize()
        
        assert exporter.is_finalized()
        assert output_path.exists()
        
        # Read and verify content
        content = output_path.read_text(encoding='utf-8')
        assert content.startswith("WEBVTT\n")
        assert "00:00:00.000 --> 00:00:02.000" in content
        assert "First subtitle" in content
        assert "00:00:02.000 --> 00:00:04.000" in content
        assert "Second subtitle" in content
    
    def test_finalize_with_dual_language(self, temp_dir):
        """Test finalizing with dual-language export"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle(
            "Hello world",
            0.0,
            2.0,
            translated_text="Hola mundo"
        )
        exporter.add_subtitle(
            "How are you?",
            2.0,
            4.0,
            translated_text="¿Cómo estás?"
        )
        exporter.finalize()
        
        # Read and verify both languages are present
        content = output_path.read_text(encoding='utf-8')
        assert "Hello world" in content
        assert "Hola mundo" in content
        assert "How are you?" in content
        assert "¿Cómo estás?" in content
    
    def test_cannot_add_after_finalization(self, temp_dir):
        """Test that adding subtitles after finalization raises error"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("Test", 0.0, 2.0)
        exporter.finalize()
        
        with pytest.raises(RuntimeError, match="Cannot add subtitles after finalization"):
            exporter.add_subtitle("Another", 2.0, 4.0)
    
    def test_cannot_clear_after_finalization(self, temp_dir):
        """Test that clearing after finalization raises error"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("Test", 0.0, 2.0)
        exporter.finalize()
        
        with pytest.raises(RuntimeError, match="Cannot clear after finalization"):
            exporter.clear()
    
    def test_finalize_idempotent(self, temp_dir):
        """Test that calling finalize multiple times is safe"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("Test", 0.0, 2.0)
        exporter.finalize()
        exporter.finalize()  # Should not raise error
        
        assert exporter.is_finalized()
    
    def test_clear_entries(self, temp_dir):
        """Test clearing subtitle entries"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.add_subtitle("First", 0.0, 2.0)
        exporter.add_subtitle("Second", 2.0, 4.0)
        assert exporter.get_entry_count() == 2
        
        exporter.clear()
        assert exporter.get_entry_count() == 0
    
    def test_empty_finalization(self, temp_dir):
        """Test finalizing with no entries creates empty file"""
        output_path = temp_dir / "test.srt"
        exporter = SubtitleExporter(str(output_path), format="srt")
        
        exporter.finalize()
        
        assert output_path.exists()
        content = output_path.read_text(encoding='utf-8')
        assert content == ""  # Empty SRT file
    
    def test_empty_vtt_finalization(self, temp_dir):
        """Test finalizing VTT with no entries creates file with header"""
        output_path = temp_dir / "test.vtt"
        exporter = SubtitleExporter(str(output_path), format="vtt")
        
        exporter.finalize()
        
        assert output_path.exists()
        content = output_path.read_text(encoding='utf-8')
        assert content == "WEBVTT\n\n"  # VTT header only
    
    def test_output_directory_creation(self, temp_dir):
        """Test that output directory is created if it doesn't exist"""
        nested_path = temp_dir / "nested" / "dir" / "test.srt"
        exporter = SubtitleExporter(str(nested_path), format="srt")
        
        assert nested_path.parent.exists()
        
        exporter.add_subtitle("Test", 0.0, 2.0)
        exporter.finalize()
        
        assert nested_path.exists()

