from PyQt5.QtCore import QObject, pyqtSignal


class DataSource(object):

    playListLoaded = pyqtSignal([str])

    def load(self):
        print("loading data...")
        return ["one", "two", "thee"]