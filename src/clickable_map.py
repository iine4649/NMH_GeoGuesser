from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QMouseEvent


class ClickableMap(QLabel):
    clicked = Signal(int, int)

    def __init__(self, map_image_path):
        super().__init__()
        self.original_pixmap = QPixmap(map_image_path)
        if not self.original_pixmap.isNull():
            self.setPixmap(self.original_pixmap)
        else:
            self.setText("Map failed to load")
        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.original_pixmap:
            self.setPixmap(self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self.pixmap() and self.original_pixmap:
            pos = event.position()
            pixmap_size = self.pixmap().size()
            x_offset = (self.width() - pixmap_size.width()) // 2
            y_offset = (self.height() - pixmap_size.height()) // 2
            click_x = pos.x() - x_offset
            click_y = pos.y() - y_offset
            
            if 0 <= click_x <= pixmap_size.width() and 0 <= click_y <= pixmap_size.height():
                original_size = self.original_pixmap.size()
                scaled_x = int(click_x * original_size.width() / pixmap_size.width())
                scaled_y = int(click_y * original_size.height() / pixmap_size.height())
                self.clicked.emit(scaled_x, scaled_y)
