from PyQt5.QtCore import QObject


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
        if oldList != trackList:
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