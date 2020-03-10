from ..newssource import NewsSource
import urllib
from selectolax.parser import HTMLParser
from dateutil.parser import parse
from bs4 import BeautifulSoup 


class WashingtonPost(NewsSource):
    
    def __init__(self, seed_url, crawler):
        super().__init__("Washington Post", seed_url, crawler)
        
    def scrape(self):
        super().scrape()
        articles = self.__wp_general_article()
        #live_data = self.__wp_live_update()
        #self.output = articles + live_data
        self.output = articles
        
    #WP's live-update article seems structured differently since it is a trail of small posts.
    def __wp_live_update(self):
        URL = "https://www.washingtonpost.com/world/asia_pacific/coronavirus-china-live-updates/2020/02/21/81d2aa50-543e-11ea-b119-4faabac6674f_story.html"
        r = urllib.request.urlopen(URL)
        soup = BeautifulSoup(r.read(), 'html.parser')

        #Seems to be the only consistent part for every article?
        main_article = soup.find('div', attrs = {'class':'article-body'})
        latest_article = soup.find('div', attrs ={'class':'teaser-content'})
        previous_articles = soup.find('div', attrs ={'class':'remainder-content'}).find('section')

        articles = []

        #The inline-story tag is "unique" to the live-update article
        for event in previous_articles.findAll('div', attrs = {'data-qa':'inline-story'}):
            story = {}
            story['time-stamp'] = event.find('div', attrs = {'class':'display-date'}).text
            story['headline'] = event.find('h2', attrs={'data-qa':'headline'}).text
            story['content'] = []
            story['journal'] = self.journal

            for para in event.find('div', attrs={'data-qa':'article-body'}).find('section').findAll('div'):
                if(para.find('p')):
                    story['content'].append(para.find('p').text)

            articles.append(story)

        return articles
    
    def __wp_general_article(self):
        articles = []
        for i, URL in enumerate(self.links):
            try:
                r = urllib.request.urlopen(URL)
            except:
                print('Skipping:',URL)
                continue 
            soup = BeautifulSoup(r.read(), 'html.parser')

            print(i+1,'/',len(self.links),URL)

            article_header = soup.find('header', attrs = {'data-qa':'main-full'})
            main_article = soup.find('div', attrs = {'class':'article-body'})
            teaser = soup.find('div', attrs ={'class':'teaser-content'}).find('section')
            body = soup.find('div', attrs ={'class':'remainder-content'}).find('section')
            timestep = soup.find('div', attrs={'class':'display-date'}).text

            story = {}
            story['content'] = []
            story['headline'] = article_header.find('h1', attrs={'data-qa':'headline'}).text
            story['time-stamp'] = timestep
            story['journal'] = self.journal

            for teaser_content in teaser.findAll('div'):
                if teaser_content.find('p'):
                     story['content'].append(teaser_content.find('p').text)

            for body_content in body.findAll('div'):
                if body_content.find('p'):
                     story['content'].append(body_content.find('p').text)

            articles.append(story)

        return articles