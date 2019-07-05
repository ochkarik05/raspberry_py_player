import sys
from PyQt5.QtCore import Qt, QTimer, QCoreApplication

app = QCoreApplication([])

timer = QTimer()

def on_timer():
    print("Hello")
    timer.stop()
    app.exit(0)

timer.timeout.connect(on_timer)
timer.start(5000)
timer.singleShot(1000, on_timer)

app.exec()