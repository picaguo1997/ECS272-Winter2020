from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse

class Xinhua(NewsSource):

    def __init__(self, seed_url, crawler):
        super().__init__('Xinhua', seed_url, crawler)

    def filter_links(self, links):
        return set(filter(lambda l:
                            ('video' not in l) and
                            ('photo' not in l) and
                            ('index' not in l) and
                            ('special' not in l)
                            , links))

    def scrape(self):
        super().scrape()
        articles = []

        for i, URL in enumerate(self.links):
            try:
                headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=URL, headers=headers)
                r = urllib.request.urlopen(req)
            except:
                print('Skipping:',URL)
                continue
            sll = HTMLParser(r.read())

            print(i+1,'/',len(self.links),URL)

            headline = sll.css_first('.Btitle')
            # if not headline:
                # headline = sll.css_first('.w980.wb_10.clear > h1')
            main_article = sll.css('.content > p')
            # if not main_article:
                # main_article = sll.css('.wb_12.clear > p')
            timestamp = sll.css_first('.time')
            # if not timestamp:
                # timestamp = sll.css_first('.w980.wb_10.clear > div')

            headline = headline.text(deep=True, separator='').strip()
            timestamp = timestamp.text(deep=True, separator='')

            story = {}
            story['content'] = []
            story['headline'] = headline
            story['time-stamp'] = timestamp # 2020-03-11 16:24:48
            story['url'] = URL
            story['journal'] = self.journal

            for paragraph in main_article:
                line = paragraph.text(deep=True, separator='')
                line = line.strip()
                # line = line.encode('ascii', 'ignore').decode('utf-8')
                story['content'].append(line)

            articles.append(story)

        self.output = articles
