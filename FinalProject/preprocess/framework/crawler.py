import urllib
from urllib.request import urlparse, urljoin
from selectolax.parser import HTMLParser


class Crawler(object):

    def __init__(self, keywords, max_urls=50):
        self.links = []
        self.keywords = keywords
        self.max_urls = max_urls
        self.reset()

    def reset(self):
        self.internal_urls = set()
        self.external_urls = set()
        self.total_urls_visited = 0

    def get_links(self):
        return self.internal_urls

    def crawl(self, url):
        """
        Crawls a web page and extracts all links.
        You'll find all links in `external_urls` and `internal_urls` global set variables.
        """
        self.total_urls_visited += 1
        if self.total_urls_visited <= self.max_urls:
            print("crawling", self.total_urls_visited, "/", self.max_urls)

        self.links = self.get_all_website_links_selectolax(url)

        for link in self.links:
            if self.total_urls_visited > self.max_urls:
            #if len(self.internal_urls) > self.max_urls:
                break
            self.crawl(link)



    def is_valid(self, url):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def get_all_website_links_selectolax(self, url):
        urls = set()

        domain_name = urlparse(url).netloc


        try:
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
            req = urllib.request.Request(url=url, headers=headers)
            r = urllib.request.urlopen(req)
            sll =  HTMLParser(r.read())
        except:
            return urls

        for a_tag in sll.css("a"):
            if not "href" in a_tag.attributes:
                continue
            href = a_tag.attrs["href"]
            if href == "" or href is None:
                continue

            href = urljoin(url,href)
            parsed_href = urlparse(href) # This removes the query portion (e.g. /story?id=12345) resulting in the final string being /story.
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + "?" + parsed_href.query #added query back (TODO: robust?)

            if not self.is_valid(href):
                # not a valid URL
                continue
            if href in self.internal_urls:
                # already in the set
                continue
            if domain_name not in href:
                # external link
    #             if href not in external_urls:
    #                 external_urls.add(href)
                continue

            a_tag_text = a_tag.text(deep=True, separator='', strip=False)
            #if not any(word in a_tag_text for word in self.keywords):
            if not (any(word in a_tag_text for word in self.keywords) or any(word in href for word in self.keywords)):
                #check if A tag text OR A tag href doesn't contain keyword
                continue

            urls.add(href)
            self.internal_urls.add(href)
        return urls
