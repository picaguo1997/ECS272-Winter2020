from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse

class ABCNews(NewsSource):
    
    def __init__(self, seed_url, crawler):
        super().__init__('ABC News', seed_url, crawler)
    
    
    def filter_links(self, links):
        return set(filter(lambda l: 
                          ('/alerts/' not in l) and
                          ('/video/' not in l) and
                          ('/photos/' not in l) and
                          ('/Coronavirus' not in l) and
                          ('/coronavirus?' not in l) and
                          ('preview.abcnews.go.com' not in l)
                          , links))
    
       
    def scrape(self):
        super().scrape()
        articles = []
        
        for i, URL in enumerate(self.links):
            try:
                r = urllib.request.urlopen(URL)
            
                sll = HTMLParser(r.read())
                
                print(i+1,'/',len(self.links),URL)
                
                headline = sll.css_first('meta[property="og:title"]').attributes['content']
                main_article = sll.css_first('article.story, article.Article__Content')
                timestamp = parse(sll.css_first('meta[property="lastPublishedDate"]').attributes['content'])
                
                story = {}
                story['content'] = []
                story['headline'] = headline
                story['time-stamp'] = timestamp.strftime("%m/%d/%Y, %H:%M:%S")
                story['url'] = URL
                story['journal'] = self.journal
                
                
                for paragraph in main_article.css('p'):
                    story['content'].append(paragraph.text(deep=True, separator=''))
                
                articles.append(story)
            except:
                print('Skipping:',URL)
                continue
            
        self.output = articles