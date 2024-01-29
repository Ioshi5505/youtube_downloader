import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox, QProgressBar, QFileDialog, QSizePolicy
from PySide6.QtCore import QThreadPool, Slot
from video_downloader import VideoDownloader
from utils import validate_url

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.download_path = os.path.expanduser("~/Downloads")
        self.thread_pool = QThreadPool()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 400, 200)
        self.load_styles()

        layout = QVBoxLayout()

        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('Введите URL видео с YouTube')
        self.url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.url_input)

        self.quality_combo = QComboBox(self)
        self.quality_combo.addItems(['240p', '360p', '720p'])
        self.quality_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.quality_combo)

        self.path_button = QPushButton('Выбрать путь загрузки', self)
        self.path_button.clicked.connect(self.choose_download_path)
        self.path_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.path_button)

        self.download_button = QPushButton('Скачать', self)
        self.download_button.clicked.connect(self.download_video)
        self.download_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel('', self)
        self.status_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def load_styles(self):
        try:
            with open('style.css', 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            pass

    def choose_download_path(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec():
            self.download_path = dialog.selectedFiles()[0]
            self.status_label.setText(f'Выбран путь для загрузки: {self.download_path}')

    def download_video(self):
        url = self.url_input.text()
        if not validate_url(url):
            self.status_label.setText('Ошибка: Неверный URL YouTube')
            return

        quality = self.quality_combo.currentText()
        self.status_label.setText('Начало загрузки...')
        self.progress_bar.setValue(0)

        downloader = VideoDownloader(url, quality, self.download_path, self)
        self.thread_pool.start(downloader)

    @Slot(int)
    def update_progress_bar(self, percentage):
        self.progress_bar.setValue(percentage)
        if percentage > 0 and self.status_label.text() == 'Начало загрузки...':
            self.status_label.setText("Загрузка...")
        if percentage >= 100:
            self.status_label.setText("Загрузка завершена.")
