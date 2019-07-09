from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThreadPool, QRunnable


class PlayListScanner(QObject):

    dataLoaded = pyqtSignal(list)

    catId = 1

    def __init__(self, dataSource):
        super().__init__()
        self.dataSource = dataSource
        self.timer = QTimer()
        self.timer.setInterval(5 * 60_000)
        self.timer.timeout.connect(self._on_timer)
        self.timer.start()
        self._on_timer()

    def __del__(self):
        self.timer.stop()

    def _on_timer(self):
        runnable = DataLoader(self.dataSource, self.dataLoaded, self.catId)
        self.catId = self.catId + 1

        if self.catId > 3:
            self.catId = 0
            self.timer.stop()

        QThreadPool.globalInstance().start(runnable)


class DataLoader(QRunnable):

    def __init__(self, dataSource, signal, catId = None):
        super().__init__()

        self.dataSource = dataSource
        self.signal = signal
        self.catId = catId


    def run(self):
        result = self.dataSource.load(self.catId)
        self.signal.emit(result)