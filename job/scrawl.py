import re
import pdb
import pprint
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
from ssave import *

URL = 'http://www.imsdb.com/scripts/'

class Crawl:

    def data(self, title):
        url = URL+title+'.html'
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, url, "xx", "xx")
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(url)
        urllib2.install_opener(opener)
        response = urllib2.urlopen(url)
        response = response.read()
        soup = BeautifulSoup(response)
        return soup

    def place_person(self, soup):
        meta = {}
        for tag in self.bold(soup):
            text = self.between_lines(tag)[0]
            if self.place(text):
                typ = 'place'
            else:
                typ = 'person'
            meta[self.clean(text)] = typ
        return meta

    def conv_scene(self, soup, meta):
        script = []
        for text in self.alltext(soup):
            if self.skip(text):
                continue
            if self.clean(text) == 'FADE TO BLACK.':
                # Script ends
                break
            if meta.has_key(self.clean(text)):
                typ = meta[self.clean(text)]
            elif self.scene(text):
                typ = 'scene'
            else:
                typ = 'conversation'
            s = { 'typ': typ,
                  #'dat': self.clean(text)}
                  'dat': text}
            script.append(s)
        return script

    def find_scenes(self, script):
        fscript = []
        for data in script:
            if data['typ']== 'conversation':
                try:
                    c, s = re.search('(.*)\r\n\r\n(.*)', data['dat']).groups()
                    fscript.append({'typ': 'conversation', 'dat': self.clean(c)})
                    fscript.append({'typ': 'scene', 'dat': self.clean(s)})
                    continue
                except Exception, e:
                    continue
            fscript.append({ 'typ': data['typ'], 'dat': self.clean(data['dat'])})
        return fscript

    def skip(self, text):
        if text.strip() == '\n' or text.strip() == '' or text.strip() == '.':
            return True
        return False

    def place(self, text):
        try:
	    #return re.search('^(.*)(\w| )\r\n$', text).groups()
            return re.search('^(\w)', text).groups()
        except Exception, e:
            return None

    def scene(self, text):
        try:
            return re.search('^\r\n(.*)',text).groups()
        except Exception, e:
            return None

    def clean(self, text):
        text = re.sub("\d+", "", text)
        text = re.sub("\r|\n", "", text)
        return text.strip()
    
    def bold(self, soup):
        return soup.findAll('html')[1].findAll('b')

    def alltext(self, soup):
        return soup.findAll('html')[1].findAll('b', text=True)

    def between_lines(self, tag):
        return tag.findAll(text=True)

def main():
    c = Crawl()
    titles = [ 'Pariah' ]
    for title in titles:
        resp = c.data(title)
        meta = c.place_person(resp)
        script = c.conv_scene(resp, meta)
        fscript = c.find_scenes(script)
        # Call save to db
        corpus_save(fscript, title)
        #pprint.pprint(fscript)

main()
