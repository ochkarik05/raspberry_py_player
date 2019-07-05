# PyQt5 Video player
#!/usr/bin/env python

import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QVBoxLayout)
from PyQt5.QtWidgets import QMainWindow, QWidget


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com")

        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        playlist = QMediaPlaylist(self.player)

        self.player.setMedia(QMediaContent(QUrl("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4")))

        videoWidget = QVideoWidget()
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)

        self.player.setVideoOutput(videoWidget)
        playlist.setCurrentIndex(0)

        wid = QWidget(self)
        self.setCentralWidget(wid)
        wid.setLayout(layout)

        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())