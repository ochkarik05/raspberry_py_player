import sys

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QRunnable, QThreadPool
from PyQt5 import QtWidgets

from data_source import DataSource
from main_window import MainWindow
from vlc_player import VlcPlayer


class DataLoader(QRunnable):

    def __init__(self, dataSource, signal, catId = None):
        super().__init__()

        self.dataSource = dataSource
        self.signal = signal
        self.catId = catId


    def run(self):
        result = self.dataSource.load(self.catId)
        self.signal.emit(result)

class PlayListScanner(QObject):

    dataLoaded = pyqtSignal(list)
    catId = 1

    def __init__(self, dataSource):
        super().__init__()
        self.dataSource = dataSource
        self.timer = QTimer()
        self.timer.setInterval(30000)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start()
        self.on_timer()

    def __del__(self):
        self.timer.stop()

    def on_timer(self):
        runnable = DataLoader(self.dataSource, self.dataLoaded, self.catId)
        self.catId = self.catId + 1

        if self.catId > 3:
            self.catId = 0
            self.timer.stop()

        QThreadPool.globalInstance().start(runnable)


class PlayList(QObject):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.trackList = None
        self.current = None

    def set_track_list(self, trackList):
        print(trackList)
        oldList = self.trackList
        self.trackList = trackList
        if not oldList:
            self.next()

    def next(self):
        if self.trackList:
            if self.current is None:
                self.current = 0
            else:
                self.current = self.current + 1
            self.play_current()

    def play_current(self):

        trackToPlay = self.current % len(self.trackList)

        print("current: {}".format(trackToPlay))
        self.player.play(self.trackList[trackToPlay].url)


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)

    dataSource = DataSource("https://my-json-server.typicode.com/ochkarik05/jsonservers/videos")

    player = VlcPlayer()

    playList = PlayList(player)

    playListScanner = PlayListScanner(dataSource)

    playListScanner.dataLoaded.connect(player.playlist_play)

    player.trackFinished.connect(playList.next)

    gui = MainWindow(player)

    # player = Player()
    gui.show()
    gui.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
