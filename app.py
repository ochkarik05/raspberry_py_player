import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from data_source import DataSource
from main_window import MainWindow
from play_list import PlayList
from play_list_scanner import PlayListScanner
from player import Player


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)

    dataSource = DataSource("https://my-json-server.typicode.com/ochkarik05/jsonservers/videos")

    player = Player()

    playList = PlayList(player)

    playListScanner = PlayListScanner(dataSource)

    playListScanner.dataLoaded.connect(playList.set_track_list)

    player.trackFinished.connect(playList.next)

    gui = MainWindow(player)

    gui.show()
    gui.resize(640, 480)

    gui.setWindowState(Qt.WindowFullScreen)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
