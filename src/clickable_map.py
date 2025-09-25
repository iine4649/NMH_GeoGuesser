from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QMouseEvent


class ClickableMap(QLabel):
    # Signal emitted when map is clicked with (x, y) coordinates
    clicked = Signal(int, int)

    def __init__(self, map_image_path: str):
        super().__init__()

        # Load the original map image
        self.original_pixmap = QPixmap(map_image_path)

        if not self.original_pixmap.isNull():
            self.setPixmap(self.original_pixmap)
        else:
            self.setText("Map failed to load")

        # Configure widget properties
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)
        self.setMinimumSize(300, 200)  # Set minimum size for usability

    def resizeEvent(self, event):
        super().resizeEvent(event)

        if self.original_pixmap and not self.original_pixmap.isNull():
            # Scale the image to fit the new size while keeping aspect ratio
            scaled_pixmap = self.original_pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.setPixmap(scaled_pixmap)

    def mousePressEvent(self, event: QMouseEvent):
        # Only handle left mouse button clicks
        if event.button() == Qt.LeftButton and self.pixmap() and self.original_pixmap:
            # Get click position
            pos = event.position()

            # Get the size of the currently displayed (scaled) pixmap
            pixmap_size = self.pixmap().size()

            # Calculate offset of the image within the widget
            x_offset = (self.width() - pixmap_size.width()) // 2
            y_offset = (self.height() - pixmap_size.height()) // 2

            # Convert click position to coordinates within the scaled image
            click_x = pos.x() - x_offset
            click_y = pos.y() - y_offset

            # Check if click is within the image bounds
            if (
                0 <= click_x <= pixmap_size.width()
                and 0 <= click_y <= pixmap_size.height()
            ):
                # Convert scaled image coordinates back to original image coordinates
                original_size = self.original_pixmap.size()
                scaled_x = int(click_x * original_size.width() / pixmap_size.width())
                scaled_y = int(click_y * original_size.height() / pixmap_size.height())

                # Emit the click signal with original map coordinates
                self.clicked.emit(scaled_x, scaled_y)
