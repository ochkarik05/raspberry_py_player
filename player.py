import platform

import vlc
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QTimer


class Player(QtWidgets.QWidget):
    trackFinished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.events = self.player.event_manager()

        self.events.event_attach(vlc.EventType.MediaPlayerEndReached, self._on_end_reached)
        # self.timer = QTimer()
        self.create_ui()

    def _on_end_reached(self, event):
        print(event)
        self._emit_track_finished()

    def _on_timer(self):
        self._emit_track_finished()

    def _emit_track_finished(self):
        # self.timer.stop()
        self.trackFinished.emit()

    def play(self, mrl):
        """Play video from mrl
        @param mrl: The MRL
        """
        print("Now playing: {}".format(mrl))
        self.player.set_mrl(mrl)
        # self.timer.singleShot(40000, self._on_timer)
        self.player.play()

    def create_ui(self):
        """Set up the user interface
        """

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

        self.setLayout(self.vboxlayout)

        if platform.system() == "Linux":  # for Linux using the X Server
            self.player.set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.player.set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.player.set_nsobject(int(self.videoframe.winId()))
        # self.setWindowState(Qt.WindowFullScreen)
