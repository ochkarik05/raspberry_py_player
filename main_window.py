from PyQt5.uic.properties import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, master = None):
        QtWidgets.QMainWindow.__init__(self, master)
        # self.setCentralWidget(player)

        # self.setWindowState(Qt.WindowFullScreen)
