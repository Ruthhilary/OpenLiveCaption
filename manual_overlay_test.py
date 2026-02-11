"""Manual test script for overlay functionality

This script demonstrates the overlay appearing on top of other applications,
click-through behavior, and text display with various lengths.

Instructions:
1. Run this script
2. Open other applications (browser, text editor, etc.)
3. Verify the overlay appears on top of all windows
4. Try clicking through the overlay to interact with underlying windows
5. Observe text display with short, medium, and long captions
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from src.ui.caption_overlay import CaptionOverlay, Position
from src.config.config_manager import OverlayConfig


def main():
    app = QApplication(sys.argv)
    
    # Create overlay with default configuration
    config = OverlayConfig(
        position="bottom",
        font_size=24,
        text_color="#FFFFFF",
        background_color="#000000",
        background_opacity=0.8,
        scroll_mode="scroll",
        max_lines=3
    )
    
    overlay = CaptionOverlay(config)
    overlay.show_overlay()
    
    print("=" * 60)
    print("MANUAL OVERLAY TEST")
    print("=" * 60)
    print("\nThe overlay window should now be visible at the bottom of your screen.")
    print("\nTest checklist:")
    print("1. ✓ Overlay appears on top of other applications")
    print("   - Open a browser or text editor")
    print("   - The overlay should remain visible on top")
    print("\n2. ✓ Click-through behavior")
    print("   - Try clicking on the overlay")
    print("   - Clicks should pass through to underlying windows")
    print("\n3. ✓ Text display with various lengths")
    print("   - Watch as different length captions appear")
    print("   - Short, medium, and long text will be displayed")
    print("\nThe test will run for 30 seconds with various captions...")
    print("=" * 60)
    
    # Test captions of various lengths
    test_captions = [
        "Short caption",
        "This is a medium length caption that demonstrates text wrapping",
        "This is a very long caption that will definitely wrap across multiple lines to demonstrate the overlay's ability to handle lengthy text content properly",
        "Line 1",
        "Line 2",
        "Line 3",
        "Line 4 - should push Line 1 off",
        "Testing scroll mode with multiple lines of text",
        "Final caption to verify everything works correctly"
    ]
    
    caption_index = [0]
    
    def update_caption():
        if caption_index[0] < len(test_captions):
            caption = test_captions[caption_index[0]]
            overlay.update_caption(caption)
            print(f"[{caption_index[0] + 1}/{len(test_captions)}] Displayed: {caption[:50]}...")
            caption_index[0] += 1
        else:
            print("\n" + "=" * 60)
            print("TEST COMPLETE")
            print("=" * 60)
            print("\nAll captions have been displayed.")
            print("The overlay will remain visible for 5 more seconds.")
            print("\nDid you observe:")
            print("  ✓ Overlay staying on top of other windows?")
            print("  ✓ Click-through behavior working?")
            print("  ✓ Text wrapping and scrolling correctly?")
            print("\nClosing in 5 seconds...")
            QTimer.singleShot(5000, app.quit)
    
    # Display captions every 3 seconds
    timer = QTimer()
    timer.timeout.connect(update_caption)
    timer.start(3000)
    
    # Start with first caption immediately
    update_caption()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
