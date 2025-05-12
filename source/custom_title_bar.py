from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
import platform
import os
import sys

class CustomTitleBar(QWidget):
    def __init__(self, name, parent):
        super().__init__(parent)        
        self.initial_pos = None
        self.name = name
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1, 1, 1, 1)
        title_bar_layout.setSpacing(2)
        self.title = QLabel(f"{self.name}", self)
        self.title.setAlignment(Qt.AlignCenter)  # PyQt5 does not use AlignmentFlag
        if platform.system() == 'Windows':
            self.title.setStyleSheet("""
                QLabel { text-transform: uppercase; font-size: 12pt; margin-left: 48px; font-family: Copperplate; }        
                """)
        if platform.system() == 'Darwin':
            self.title.setStyleSheet("""
                    QLabel { text-transform: uppercase; font-size: 12pt; margin-right: 70px; font-family: Copperplate; }        
                    """)
    
        if title := parent.windowTitle():
            self.title.setText(title)
        if platform.system() == "Windows":
            title_bar_layout.addWidget(self.title)
        
        # Min button
        self.min_button = QToolButton(self)
        min_icon = QIcon()
        min_icon_path = self.get_resource_path('resources/icons/min.svg')
        min_icon.addFile(min_icon_path)
        self.min_button.setIcon(min_icon)
        self.min_button.clicked.connect(self.window().showMinimized)

        # Max button
        self.max_button = QToolButton(self)
        max_icon = QIcon()
        max_icon_path = self.get_resource_path('resources/icons/max.svg')
        max_icon.addFile(max_icon_path)
        self.max_button.setIcon(max_icon)
        self.max_button.clicked.connect(self.window().showMaximized)

        # Close button
        self.close_button = QToolButton(self)
        close_icon = QIcon()
        close_icon_path = self.get_resource_path('resources/icons/close.svg')
        close_icon.addFile(close_icon_path)
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)
        
        # Normal button
        self.normal_button = QToolButton(self)
        normal_icon = QIcon()
        normal_icon_path = self.get_resource_path('resources/icons/normal.svg')
        normal_icon.addFile(normal_icon_path)
        self.normal_button.setIcon(normal_icon)
        self.normal_button.clicked.connect(self.window().showNormal)
        self.normal_button.setVisible(False)

        # Add buttons             
        buttons = [
            self.min_button,
            self.normal_button,
            self.max_button,
            self.close_button,
        ]
        if platform.system() == "Darwin":
            buttons.reverse()
        for button in buttons:
            button.setFocusPolicy(Qt.NoFocus)
            button.setFixedSize(QSize(16, 16))
            button.setStyleSheet(
                """QToolButton {
                    border: none;
                    padding: 2px;
                }
                """
            )

            title_bar_layout.addWidget(button)
        if platform.system() == "Darwin":
            title_bar_layout.addWidget(self.title)

    def window_state_changed(self, state):
        if state == Qt.WindowMaximized:
            self.normal_button.setVisible(True)
            self.max_button.setVisible(False)
        else:
            self.normal_button.setVisible(False)
            self.max_button.setVisible(True)

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)
        

