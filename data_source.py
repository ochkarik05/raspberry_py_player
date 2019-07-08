import json
import urllib.request


class VideoItem:

    def __init__(self, itemJson):
        self.itemJson = itemJson

    @property
    def url(self):
        return self.itemJson["sources"][0]


class DataSource(object):

    def __init__(self, url):
        self.url = url

    def load(self):
        print("loading data...")
        response = urllib.request.urlopen(self.url)
        return [VideoItem(n) for n in json.loads(response.read())]
