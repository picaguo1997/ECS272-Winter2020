from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse

class FoxNews(NewsSource):
    
    def __init__(self, seed_url, crawler):
        super().__init__('FoxNews', seed_url, crawler)
        
    def filter_links(self, links):
        return set(filter(lambda l: 
                          ('/category/' not in l) and
                          ('.print' not in l)
                          
                          , links))
    
    
    def scrape(self):
        super().scrape()
        articles = []
        
        for i, URL in enumerate(self.links):
            r = urllib.request.urlopen(URL) 
            sll = HTMLParser(r.read())
            
            print(i+1,'/',len(self.links),URL)
            
            headline = sll.css_first('meta[name="dc.title"]').attributes['content']
            timestamp = parse(sll.css_first('meta[name="dcterms.created"]').attributes['content'])
            main_article = sll.css_first('.article-body')
            
            story = {}
            story['content'] = []
            story['headline'] = headline
            story['time-stamp'] = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
            story['url'] = URL
            story['journal'] = self.journal
            
            
            for paragraph in main_article.css('p'):
                story['content'].append(paragraph.text(deep=True, separator=''))
            
            articles.append(story)
            
        self.output = articles