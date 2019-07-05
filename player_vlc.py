import platform
import sys

import vlc
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


class Player(QtWidgets.QMainWindow):
    """A simple Media Player using VLC and Qt
    """



    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new(
            "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4")

        self.create_ui()

        self.events = self.mediaplayer.event_manager()
        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self.track_finished)
        self.start_playing()

    @staticmethod
    def track_finished(event):
        print("Finished")

    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if platform.system() == "Darwin":  # for MacOS
            self.videoframe = QtWidgets.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtWidgets.QFrame()

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.setContentsMargins(0, 0, 0, 0)

        self.widget.setLayout(self.vboxlayout)
        self.setWindowState(Qt.WindowFullScreen)

    def start_playing(self):

        if platform.system() == "Linux":  # for Linux using the X Server
            self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.mediaplayer.set_nsobject(int(self.videoframe.winId()))

        self.mediaplayer.play()


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
