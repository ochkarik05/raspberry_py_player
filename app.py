import sys

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QTimer, QRunnable, QThreadPool
from PyQt5 import QtWidgets

from data_source import DataSource

class DataLoader(QRunnable):

    def __init__(self, dataSource, signal):
        super().__init__()

        self.dataSource = dataSource
        self.signal = signal


    def run(self):
        result = self.dataSource.load()
        self.signal.emit(result)

class PlayListScanner(QObject):

    dataLoaded = pyqtSignal(list)

    def __init__(self, dataSource):
        super().__init__()
        self.dataSource = dataSource
        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start()


    def __del__(self):
        self.timer.stop()

    def on_timer(self):
        runnable = DataLoader(self.dataSource, self.dataLoaded)
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


class VlcPlayer(QObject):

    trackFinished = pyqtSignal()

    def play(self, path):
        print("play track: {}".format(path))
        QTimer().singleShot(1000, self.trackFinished.emit)


def main():
    """Entry point for our simple vlc player
    """
    app = QtWidgets.QApplication(sys.argv)

    dataSource = DataSource("https://my-json-server.typicode.com/ochkarik05/jsonservers/videos")

    player = VlcPlayer()

    playList = PlayList(player)

    playListScanner = PlayListScanner(dataSource)

    playListScanner.dataLoaded.connect(playList.set_track_list)
    player.trackFinished.connect(playList.next)

    # gui = MainWindow(dataSource)

    # player = Player()
    # player.show()
    # player.resize(640, 480)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
