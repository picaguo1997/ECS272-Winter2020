from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse

class CGTN(NewsSource):

    def __init__(self, seed_url, crawler):
        super().__init__('CGTN', seed_url, crawler)

    def filter_links(self, links):
        # return set(filter(lambda l:
                    # ('hd' not in l)
                    # , links))
        return set(links)

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

            headline = sll.css_first('.news-title')

            main_article = sll.css('.text.en > p')

            timestamp = sll.css_first('.date')

            try:
                headline = headline.text(deep=True, separator='').strip()
                timestamp = timestamp.text(deep=True, separator='').strip()
                timestamp = timestamp.encode('ascii', 'ignore').decode('utf-8')
            except:
                headline=''
                timestamp=''
                main_article=''

            story = {}
            story['content'] = []
            story['headline'] = headline
            story['time-stamp'] = timestamp # 2020-03-11 16:24:48
            story['url'] = URL
            story['journal'] = self.journal

            for paragraph in main_article:
                line = paragraph.text(deep=True, separator='')
                line = line.strip()
                line = line.encode('ascii', 'ignore').decode('utf-8')
                if line:
                    story['content'].append(line)

            articles.append(story)

        self.output = articles
