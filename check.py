from env import REQARGS, STICKERS, MONITOR
from requests import get as GET
from urllib.parse import parse_qs
from bs4 import BeautifulSoup as Soup
import utils
import json

try:
    with open('processed.json', 'r') as f:
        processed = json.load(f)
except FileNotFoundError:
    processed = []

def process(sid, uid):
    global processed
    if sid not in processed:
        print("Processing Post {} (?)".format(sid))
        p = utils.Post(sid, uid)
        p.react('哇')
        sticker = STICKERS[utils.stickerize(utils.classify(p.contents))]
        p.comment(sticker=sticker)

        processed.append(str(sid))
        with open('processed.json', 'w') as f:
            f.write(json.dumps(processed))
    else:
        print("Post: {} Already processed!".format(sid))

def checkURL(url, count=1):
    s = Soup(GET(url, **REQARGS).text, 'html5lib')
    for p in s.findAll(text="完整動態")[:count]:
        storyurl = p.parent.attrs['href']
        sid = parse_qs(storyurl)['/story.php?story_fbid'][0]
        uid = parse_qs(storyurl)['id'][0]
        process(sid, uid)

if __name__ == '__main__':
    for uid in MONITOR:
        checkURL('https://mbasic.facebook.com/profile.php?id={}'.format(uid), 2)
