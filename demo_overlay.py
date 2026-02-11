"""Demo script to test the CaptionOverlay window"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from src.ui.caption_overlay import CaptionOverlay, Position
from src.config.config_manager import OverlayConfig


class DemoWindow(QMainWindow):
    """Demo control window to test overlay functionality"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caption Overlay Demo")
        self.setGeometry(100, 100, 400, 300)
        
        # Create overlay with default config
        config = OverlayConfig()
        config.position = "bottom"
        config.font_size = 28
        config.background_opacity = 0.8
        
        self.overlay = CaptionOverlay(config)
        
        # Create UI
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Show/Hide buttons
        show_btn = QPushButton("Show Overlay")
        show_btn.clicked.connect(self.overlay.show_overlay)
        layout.addWidget(show_btn)
        
        hide_btn = QPushButton("Hide Overlay")
        hide_btn.clicked.connect(self.overlay.hide_overlay)
        layout.addWidget(hide_btn)
        
        # Test caption buttons
        test_btn1 = QPushButton("Test Caption 1")
        test_btn1.clicked.connect(lambda: self.overlay.update_caption("Hello, this is a test caption!"))
        layout.addWidget(test_btn1)
        
        test_btn2 = QPushButton("Test Caption 2")
        test_btn2.clicked.connect(lambda: self.overlay.update_caption("This is another caption with more text to test wrapping"))
        layout.addWidget(test_btn2)
        
        test_btn3 = QPushButton("Test Long Caption")
        test_btn3.clicked.connect(lambda: self.overlay.update_caption(
            "This is a very long caption that should wrap at word boundaries and demonstrate the text wrapping functionality of the overlay window"
        ))
        layout.addWidget(test_btn3)
        
        # Position buttons
        top_btn = QPushButton("Move to Top")
        top_btn.clicked.connect(lambda: self.overlay.set_position(Position.TOP))
        layout.addWidget(top_btn)
        
        bottom_btn = QPushButton("Move to Bottom")
        bottom_btn.clicked.connect(lambda: self.overlay.set_position(Position.BOTTOM))
        layout.addWidget(bottom_btn)
        
        # Style buttons
        style_btn1 = QPushButton("Red Text")
        style_btn1.clicked.connect(lambda: self.overlay.set_colors("#FF0000", "#000000"))
        layout.addWidget(style_btn1)
        
        style_btn2 = QPushButton("Green Text")
        style_btn2.clicked.connect(lambda: self.overlay.set_colors("#00FF00", "#000000"))
        layout.addWidget(style_btn2)
        
        style_btn3 = QPushButton("Large Font")
        style_btn3.clicked.connect(lambda: self.overlay.set_font("Arial", 36))
        layout.addWidget(style_btn3)
        
        # Scroll mode test
        scroll_btn = QPushButton("Test Scroll Mode")
        scroll_btn.clicked.connect(self.test_scroll_mode)
        layout.addWidget(scroll_btn)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        # Show overlay initially
        self.overlay.show_overlay()
        self.overlay.update_caption("Caption Overlay Demo - Click buttons to test!")
    
    def test_scroll_mode(self):
        """Test scroll mode with multiple captions"""
        self.overlay.config.scroll_mode = "scroll"
        self.overlay.update_caption("First line")
        
        QTimer.singleShot(1000, lambda: self.overlay.update_caption("Second line"))
        QTimer.singleShot(2000, lambda: self.overlay.update_caption("Third line"))
        QTimer.singleShot(3000, lambda: self.overlay.update_caption("Fourth line (first should disappear)"))
    
    def closeEvent(self, event):
        """Clean up overlay when closing"""
        self.overlay.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    demo = DemoWindow()
    demo.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
