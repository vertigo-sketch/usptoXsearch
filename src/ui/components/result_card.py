from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal

class ResultCard(QFrame):
    """A widget to display a single search result summary."""
    download_requested = Signal(str, str)  # data_source, title (as filename placeholder)

    def __init__(self, title: str, description: str, data_source: str, parent=None):
        super().__init__(parent)
        self.title = title
        self.data_source = data_source
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(1)
        self.setStyleSheet("background-color: #ffffff; border-radius: 5px; margin: 5px;")
        
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.title_label.setWordWrap(True)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("color: #7f8c8d;")
        desc_label.setWordWrap(True)
        
        self.download_button = QPushButton("Download")
        self.download_button.setVisible(False)  # Only show if it's a downloadable type
        self.download_button.clicked.connect(self._on_download_clicked)
        self.download_button.setStyleSheet("background-color: #3498db; color: white; border-radius: 3px;")
        
        layout.addWidget(self.title_label)
        layout.addWidget(desc_label)
        layout.addWidget(self.download_button, alignment=Qt.AlignmentFlag.AlignRight)

    def show_download_button(self):
        self.download_button.setVisible(True)

    def _on_download_clicked(self):
        # Emit the signal with data source and title (used as filename placeholder)
        self.download_requested.emit(self.data_source, self.title)