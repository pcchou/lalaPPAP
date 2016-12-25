from bs4 import BeautifulSoup as Soup
from env import REQARGS
from requests import get as GET, post as POST

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
            self.contents = '\n'.join(map(str, s.strong.findParent(id="m_story_permalink_view").find('p').strings))
        except:
            self.contents = ""

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

