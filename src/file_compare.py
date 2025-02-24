

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, \
    QLabel, QTextBrowser, QFileDialog
import sys
import os


class FileCompare(QMainWindow):
    def __init__(self):
        super().__init__()

        # All UI elements here
        # Line edits
        self.gold_path = QLineEdit()
        self.new_path = QLineEdit()
        self.gold_error = QLabel('')
        self.new_error = QLabel('')

        # Text box
        self.text_browser = QTextBrowser()

        #Buttons
        self.compare_button = QPushButton('Compare')
        self.reset_button = QPushButton('Reset')
        self.close_button = QPushButton('Close')
        self.open_gold_button = QPushButton('+')
        self.open_new_button = QPushButton('+')

        self.setup_window()

    def setup_window(self):
        
        self.setMinimumSize(800,800)
        self.setWindowTitle('File Compare')

        # File name input
        self.gold_path.setPlaceholderText('Enter Gold file path...')
        self.gold_path.setAcceptDrops(True)
        self.gold_path.dragEnterEvent = self.dragEnterEvent
        self.gold_path.dropEvent = lambda event: self.dropEvent(event, self.gold_path)

        self.new_path.setPlaceholderText('Enter New file path...')
        self.new_path.setAcceptDrops(True)
        self.new_path.dragEnterEvent = self.dragEnterEvent
        self.new_path.dropEvent = lambda event: self.dropEvent(event, self.new_path)

        # Error Labels
        self.gold_error.setStyleSheet('color: red;')
        self.new_error.setStyleSheet('color: red;')

        # Text Box
        self.text_browser = QTextBrowser()

        # Button Actions
        self.compare_button.setDisabled(True)
        self.compare_button.clicked.connect(self.compare_action)
        self.reset_button.clicked.connect(self.reset_action)
        self.close_button.clicked.connect(self.close_action)
        self.open_gold_button.clicked.connect(self.open_file_dialog_action)
        self.open_new_button.clicked.connect(self.open_file_dialog_action)

        # Layout boxes
        layout = QVBoxLayout()
        gold_layout = QHBoxLayout()
        new_layout = QHBoxLayout()
        button_row = QHBoxLayout()

        # Layout
        gold_layout.addWidget(QLabel('Gold Path:'))
        gold_layout.addWidget(self.gold_path)
        gold_layout.addWidget(self.gold_error)
        gold_layout.addWidget(self.open_gold_button)
        new_layout.addWidget(QLabel('New Path:'))
        new_layout.addWidget(self.new_path)
        new_layout.addWidget(self.new_error)
        new_layout.addWidget(self.open_new_button)
        layout.addLayout(gold_layout)
        layout.addLayout(new_layout)
        layout.addWidget(self.text_browser)
        button_row.addWidget(self.close_button)
        button_row.addWidget(self.reset_button)
        button_row.addWidget(self.compare_button)
        layout.addLayout(button_row)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Signals and Slots
        self.gold_path.textChanged.connect(self.check_inputs)
        self.new_path.textChanged.connect(self.check_inputs)

    def check_inputs(self):
        gold_path_filled = bool(self.gold_path.text().strip())
        new_path_filled = bool(self.new_path.text().strip())
        self.compare_button.setEnabled(gold_path_filled and new_path_filled)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event, line_edit):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            line_edit.setText(file_path)

    def compare_action(self):
        unique_lines = []
        data = ''
        gold_path = self.gold_path.text()
        new_path = self.new_path.text()

        # Reset error messages
        self.gold_error.setText('')
        self.new_error.setText('')
        self.gold_path.setStyleSheet('')
        self.new_path.setStyleSheet('')

         # Validate file paths
        valid_paths = True
        if not os.path.isfile(gold_path):
            self.gold_error.setText('Invalid path')
            self.gold_path.setStyleSheet("border: 1px solid red;")
            valid_paths = False
        if not os.path.isfile(new_path):
            self.new_error.setText('Invalid path')
            self.new_path.setStyleSheet("border: 1px solid red;")
            valid_paths = False
        
        if not valid_paths:
            return  # Stop execution if paths are invalid
        
        gold_lines = self.readfile(gold_path)
        new_lines = self.readfile(new_path)

        for line in gold_lines:
            if line not in new_lines:
                unique_lines.append(f'Gold: {line}')
        for line_ in new_lines:
            if line_ not in gold_lines:
                unique_lines.append(f'New: {line_}')

        for text in unique_lines:
            data += f'{text}\n'

        self.text_browser.setText(data)

    def reset_action(self):
        self.gold_path.clear()
        self.new_path.clear()
        self.text_browser.setText('')
        self.gold_error.setText('')
        self.new_error.setText('')
        self.gold_path.setStyleSheet('')
        self.new_path.setStyleSheet('')

    def open_file_dialog_action(self):
        sender = self.sender()
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', "", "All Files (*);;Text Files (*.txt)", options=options)

        if file_path:
            if sender == self.open_gold_button:
                self.gold_path.setText(file_path)
            elif sender == self.open_new_button:
                self.new_path.setText(file_path)

    def close_action(self, *args, **kwargs):
        QApplication.quit()

    def readfile(self, filename) -> list:
        with open(filename, 'r') as inputfile:
            lines = inputfile.readlines()

        return lines
    
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setApplicationName('File Compare')
        window = FileCompare()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f'An error occurred: {e}')