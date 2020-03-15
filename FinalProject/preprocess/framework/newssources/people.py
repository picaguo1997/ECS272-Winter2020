from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse

class People(NewsSource):

    def __init__(self, seed_url, crawler):
        super().__init__('People', seed_url, crawler)

    def filter_links(self, links):
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

            headline = sll.css_first('#p_title')
            if not headline:
                headline = sll.css_first('.w980.wb_10.clear > h1')
            main_article = sll.css('#p_content > p')
            if not main_article:
                main_article = sll.css('.wb_12.clear > p')
            timestamp = sll.css_first('.wb_1.clear')
            if not timestamp:
                timestamp = sll.css_first('.w980.wb_10.clear > div')

            headline = headline.text(deep=True, separator='')
            removal = ')'
            timestamp = timestamp.text(deep=True, separator='')
            timestamp = timestamp.encode('ascii', 'ignore').decode('utf-8')
            idx = timestamp.index(removal)
            timestamp = timestamp[idx+1:]

            story = {}
            story['content'] = []
            story['headline'] = headline
            story['time-stamp'] = timestamp #09:57, January 30, 2020
            story['url'] = URL
            story['journal'] = self.journal

            for paragraph in main_article:
                line = paragraph.text(deep=True, separator='')
                line = line.strip()
                line = line.encode('ascii', 'ignore').decode('utf-8')
                story['content'].append(line)

            articles.append(story)

        self.output = articles
