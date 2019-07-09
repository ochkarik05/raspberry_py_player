from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, player, master = None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setCentralWidget(player)

        # self.setWindowState(Qt.WindowFullScreen)
