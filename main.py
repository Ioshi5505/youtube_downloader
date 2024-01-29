from PySide6.QtWidgets import QApplication
from youtube_downloader import YouTubeDownloader
import sys

def main():
    app = QApplication(sys.argv)
    ex = YouTubeDownloader()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
