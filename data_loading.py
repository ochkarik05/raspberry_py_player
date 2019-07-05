import signal
import sys
import asyncio
import aiohttp
import json

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)

app = QApplication(sys.argv)


async def get_json(client, url):
    async with client.get(url) as response:
        assert response.status == 200
        return await response.read()


async def get_reddit_top(subreddit, client):
    data1 = await get_json(client, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')

    j = json.loads(data1.decode('utf-8'))
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print(str(score) + ': ' + title + ' (' + link + ')')

    print('DONE:', subreddit + '\n')


def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def func():
    asyncio.ensure_future(get_reddit_top('python', client))
    app.exit(0)
    # asyncio.ensure_future(get_reddit_top('programming', client))
    # asyncio.ensure_future(get_reddit_top('compsci', client))
    # loop.stop()


timer = QTimer()

timer.singleShot(3000, func)

# loop.run_forever()

app.exec()
