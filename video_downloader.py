from PySide6.QtCore import QRunnable, Q_ARG, QMetaObject, Qt
from pytube import YouTube

class VideoDownloader(QRunnable):
    def __init__(self, url, quality, download_path, widget):
        super().__init__()
        self.url = url
        self.quality = quality
        self.download_path = download_path
        self.widget = widget

    def run(self):
        try:
            yt = YouTube(self.url, on_progress_callback=self.on_progress)
            video = yt.streams.filter(file_extension='mp4', res=self.quality).first()
            if video:
                video.download(self.download_path)
                QMetaObject.invokeMethod(self.widget, "update_progress_bar", Qt.QueuedConnection, Q_ARG(int, 100))
        except Exception as e:
            print(f'Ошибка при загрузке видео: {e}')

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = int((bytes_downloaded / total_size) * 100)
        QMetaObject.invokeMethod(self.widget, "update_progress_bar", Qt.QueuedConnection, Q_ARG(int, percentage))
