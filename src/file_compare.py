from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, \
    QLabel, QTextBrowser, QFileDialog, QToolTip, QMenu, QMenuBar, QMessageBox
from PyQt5.QtCore import QTimer, Qt, QEvent
import sys
import os
import configparser
import platform
from custom_title_bar import CustomTitleBar


class FileCompare(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initial_pos = None
        self.title_bar = CustomTitleBar(parent=self, name='File Compare')
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
        self.open_gold_button.setMinimumSize(70, 25)
        self.open_new_button = QPushButton('+')
        self.open_new_button.setMinimumSize(70, 25)

        # Button properties
        self.compare_button.setProperty('bottom_row', True)
        self.reset_button.setProperty('bottom_row', True)
        self.close_button.setProperty('bottom_row', True)
        self.open_gold_button.setProperty('file_button', True)
        self.open_new_button.setProperty('file_button', True)

        # Tool tips
        self.compare_button.setToolTip('Compares two files')
        self.reset_button.setToolTip('Resets all data')
        self.close_button.setToolTip('Exits program')
        self.open_gold_button.setToolTip('Searches for gold files')
        self.open_new_button.setToolTip('Searches for new files')

        self.setup_window()
        self.setup_menu()
        self.setup_icon()


        # Calling Stylesheet
        self.load_theme()

    def setup_window(self):
        
        self.setMinimumSize(800,900)
        self.setWindowTitle('File Compare')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        #self.title_bar = CustomTitleBar(self)
        central_widget = QWidget()
        central_widget.setObjectName("Container")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.addWidget(self.title_bar)

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
        self.open_gold_button.clicked.connect(lambda: self.open_file_dialog_action('gold'))
        self.open_new_button.clicked.connect(lambda: self.open_file_dialog_action('new'))

        # Layout boxes
        #layout = QVBoxLayout()
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
        main_layout.addLayout(gold_layout)
        main_layout.addLayout(new_layout)
        main_layout.addWidget(self.text_browser)
        button_row.addWidget(self.close_button)
        button_row.addWidget(self.reset_button)
        button_row.addWidget(self.compare_button)
        main_layout.addLayout(button_row)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Signals and Slots
        self.gold_path.textChanged.connect(self.check_inputs)
        self.new_path.textChanged.connect(self.check_inputs)

    def setup_menu(self):
        menu = self.menuBar()

        # Adding file menu items
        file_menu = menu.addMenu('File')
        add_gold_item = file_menu.addAction('Add Gold File')
        add_new_item = file_menu.addAction('Add New File')
        reset_item = file_menu.addAction('Reset')
        close_item = file_menu.addAction('Close')

        # Adding actions for file menu items
        add_gold_item.triggered.connect(lambda: self.open_file_dialog_action('gold'))
        add_new_item.triggered.connect(lambda: self.open_file_dialog_action('new'))
        reset_item.triggered.connect(self.reset_action)
        close_item.triggered.connect(self.close_action)

        # Adding settings menu
        settings_menu = menu.addMenu('Settings')
        theme_menu = settings_menu.addMenu('Theme')
        dark_theme_item = theme_menu.addAction('Dark Theme')
        light_theme_item = theme_menu.addAction('Light Theme')
        blue_theme_item = theme_menu.addAction('Blue Theme')

        # Adding actions for settings menu items
        dark_theme_item.triggered.connect(lambda: self.apply_stylesheet('dark'))
        light_theme_item.triggered.connect(lambda: self.apply_stylesheet('light'))
        blue_theme_item.triggered.connect(lambda: self.apply_stylesheet('blue'))

        # Adding Help menu
        help_menu = menu.addMenu('Help')
        about_action = help_menu.addAction('About')

        # Adding actions for help menu
        about_action.triggered.connect(lambda: self.show_about_dialog())

    def setup_icon(self):
        self.setWindowIcon(QIcon('../resources/icons/icon.ico'))

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

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            self.title_bar.window_state_changed(self.windowState())
        super().changeEvent(event)
        event.accept()

    def window_state_changed(self, state):
        self.normal_button.setVisible(state == Qt.WindowMaximized)
        self.max_button.setVisible(state != Qt.WindowMaximized)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.initial_pos = event.pos()
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None:
            delta = event.pos() - self.initial_pos
            self.window().move(self.window().x() + delta.x(), self.window().y() + delta.y())
        super().mouseMoveEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)
        event.accept()

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

        if unique_lines:
            for text in unique_lines:
                data += f'{text}\n'
        else:
            data += 'These files are identical!'

        self.text_browser.setText(data)

    def reset_action(self):
        self.gold_path.clear()
        self.new_path.clear()
        self.text_browser.setText('')
        self.gold_error.setText('')
        self.new_error.setText('')
        self.gold_path.setStyleSheet('')
        self.new_path.setStyleSheet('')

    def open_file_dialog_action(self, target):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', "", "All Files (*);;Text Files (*.txt);;Python Files (*.py)", options=options)

        if file_path:
            if target == 'gold':
                self.gold_path.setText(file_path)
            elif target == 'new':
                self.new_path.setText(file_path)

    def show_about_dialog(self):
        QMessageBox.about(self, 'About File Compare', 'File Compare Version 2.0\n\nA simple file comparison tool.\nCreated by Kyle Simpson.')

    @staticmethod
    def close_action(*args, **kwargs):
        QApplication.quit()

    @staticmethod
    def readfile(filename) -> list:
        try:
            with open(filename, 'r') as inputfile:
                lines = inputfile.readlines()

        except FileNotFoundError:
            lines = ['File not found']
        except PermissionError:
            lines = ['Permission denied']
        except UnicodeDecodeError:
            lines = ['UnicodeDecodeError: Invalid file. File must be UTF-8']
        except Exception as error:
            lines = ['Error: ' + str(error)]

        return lines
    def apply_stylesheet(self, theme):
        theme_path = os.path.join(os.path.dirname(__file__), f'../resources/themes/{theme}.qss')

        if os.path.isfile(theme_path):
            with open(theme_path, 'r') as theme_file:
                self.setStyleSheet(theme_file.read())

            self.save_theme(theme)

    def load_theme(self):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), f'../resources/config.ini')

        if os.path.isfile(config_path):
            config.read(config_path)
            theme = config.get('Settings', 'theme', fallback='dark')
        else:
            theme = 'dark'
        self.apply_stylesheet(theme)

    @staticmethod
    def save_theme(theme):
        config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), f'../resources/config.ini')

        config.read(config_path)

        if "Settings" not in config:
            config['Settings'] = {}

        config['Settings']['theme'] = theme

        with open(config_path, 'w') as configfile:
            config.write(configfile)


    def reload_stylesheet(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.apply_stylesheet, 'dark')
        self.timer.start(1000)

    
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        app.setApplicationName('File Compare')
        app.setWindowIcon(QIcon('../resources/icons/icon.ico'))
        window = FileCompare()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f'An error occurred: {e}')