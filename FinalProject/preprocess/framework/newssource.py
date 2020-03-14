import json

class NewsSource(object):
    
    def __init__(self, journal, seed_url, crawler):
        self.journal = journal
        
        print('Crawling for sources using seed...')
        print(seed_url)
        crawler.reset()
        crawler.crawl(seed_url)
        print('Crawling done')
        
        print('Filtering links...')
        self.links = self.filter_links(crawler.get_links())
        self.output = None
        print('Done.')

    def run(self):
        self.scrape()
        self.export(self.journal)
    
    def get_output(self):
        return self.output
    
    def get_links(self):
        return self.links
    
    def export(self, filename):
        if self.output == None:
            print('Run scrape first!')
            return
        
        with open(filename + '.json', 'w') as outfile:
            json.dump(self.output, outfile)
        
    
    def filter_links(self, links):
        return links
    
    def scrape(self):
        print('Scraping', len(self.links), 'sources on', self.journal)