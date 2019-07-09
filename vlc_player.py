import platform

import vlc
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QTimer


class VlcPlayer(QtWidgets.QWidget):
    trackFinished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.instance = vlc.Instance()
        self.player = self.instance.media_list_player_new()
        self.events = self.player.event_manager()

        # EventType.MediaListEndReached           = EventType(516)
        # EventType.MediaListItemAdded            = EventType(0x200)
        # EventType.MediaListItemDeleted          = EventType(514)
        # EventType.MediaListPlayerNextItemSet    = EventType(1025)
        # EventType.MediaListPlayerPlayed         = EventType(0x400)
        # EventType.MediaListPlayerStopped        = EventType(1026)
        # EventType.MediaListViewItemAdded        = EventType(0x300)
        # EventType.MediaListViewItemDeleted      = EventType(770)
        # EventType.MediaListViewWillAddItem      = EventType(769)
        # EventType.MediaListViewWillDeleteItem   = EventType(771)
        # EventType.MediaListWillAddItem          = EventType(513)
        # EventType.MediaListWillDeleteItem       = EventType(515)

        self.events.event_attach(vlc.EventType.MediaListPlayerNextItemSet, self.next_item_handler)
        self.events.event_attach(vlc.EventType.MediaListViewWillAddItem, lambda event: print(event))

        self.timer = QTimer()
        self.timer.setInterval(8000)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start()

        self.create_ui()

    def next_item_handler(self, event):
        p = self.player.get_media_player()
        m = p.get_media().get_mrl()
        print(m)


    def on_timer(self):
        self.player.next()

    # def play(self, path):
    #     print("play track: {}".format(path))
    #     QTimer().singleShot(1000, self.trackFinished.emit)

    def playlist_play(self, videoItems):
        uris = [item.url for item in videoItems]
        print(uris)
        media_list = self.instance.media_list_new()

        for uri in uris:
            media_list.add_media(uri)

        self.player.set_media_list(media_list)
        self.player.play()

        # for uri in uris:

        # vlc.libvlc_media_list_set_media(self.player, media_library)
        # vlc.libvlc_playlist_play(self.player, -1, 0, None)

    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        # self.widget = QtWidgets.QWidget(self)
        # self.setCentralWidget(self.widget)

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
            self.player.get_media_player().set_xwindow(int(self.videoframe.winId()))
        elif platform.system() == "Windows":  # for Windows
            self.player.get_media_player().set_hwnd(int(self.videoframe.winId()))
        elif platform.system() == "Darwin":  # for MacOS
            self.player.get_media_player().set_nsobject(int(self.videoframe.winId()))
        # self.setWindowState(Qt.WindowFullScreen)
