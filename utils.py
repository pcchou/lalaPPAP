from bs4 import BeautifulSoup as Soup
from env import REQARGS, CLASSES, CHOOSE
from requests import get as GET, post as POST
from random import randint
from math import pi
from time import strftime

def classify(text):
    """Classify the given text.

    Currently a naive text ranker, some Machine Learning™ is urgently needed.

    :param text: The given text (in Chinese)
a   :return (string) The category of the text
    """
    rank = [(sum(map(lambda x: text.count(x), (w for w in wl))), c) for (c, wl) in CLASSES]
    rank.sort(key=lambda x: x[0])
    with open('history', 'a') as f:
        f.write("[{}] {} => {}\n".format(strftime('%x %X'), text.replace('\n', '\\n'), rank))
    return rank[-1][1]

def stickerize(category):
    """Choose a sticker according to your category.

    :param text: The desired category.
    :return (string) The chosen sticker.
    """
    if category not in CHOOSE:
        return None
    else:
        i = int(1.201**(randint(0, 16)-pi)) % len(CHOOSE[category]) # Some fun integer mapping
        return CHOOSE[category][i]

class Post:
    def react(self, name):
        picker = Soup(GET('https://mbasic.facebook.com/reactions/picker/?ft_id={}'.format(self.sid), **REQARGS).text, 'html5lib')
        try:
            action_url = picker.find(text=name).findParents('td')[1].find('a').attrs['href']
        except AttributeError:
            return False
        else:
            s = GET('https://mbasic.facebook.com' + action_url, **REQARGS, allow_redirects=False)
            return 302 == s.status_code

    def comment(self, text="", sticker=None):
        form = self.s.strong.findParent(id="m_story_permalink_view").find('form')
        action_url = form.attrs['action']
        data = {'fb_dtsg': form.find(attrs={'name': "fb_dtsg"}).attrs['value']}

        if sticker:
            data['sticker_id'] = sticker
        if text:
            data['comment_text'] = text

        POST('https://mbasic.facebook.com' + action_url, **REQARGS, data=data)

    def __init__(self, sid, uid):
        self.sid = sid
        self.uid = uid
        s = self.s = Soup(GET('https://mbasic.facebook.com/story.php?story_fbid={}&id={}'.format(sid, uid), **REQARGS).text, 'html5lib')

        try:
            self.contents = '\n'.join(map(str, list(s.strong.findParent(id="m_story_permalink_view").find('p').strings)))
        except:
            self.contents = ""

        try:
            self.contents += '\n'.join(map(str, list(s.strong.findParent(id="m_story_permalink_view").find('div', attrs={'style': 'font-size:24px;font-weight:300;line-height:1.2;display:inline'}).strings)))
        except:
            pass

        try:
            h = ''.join(map(str, s.strong.findParent('h3').strings))
        except AttributeError:
            self.type = 'P'
        else:
            if "分享了" in h and "貼文" in h:
                self.type = 'S'
            elif "分享了" in h and ("相片" in h or "影片" in h):
                self.type = 'SP'
            else:
                self.type = 'M'

