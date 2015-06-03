
from feedparsers.feedparser import FeedParser, FeedItem
from bs4 import BeautifulSoup
import re

class LivejournalParser(FeedParser):
    def __init__(self):
        super().__init__()

    def id(self):
        return "livejournal"

    def get_index(self, page_url):
        result = []
        soup = BeautifulSoup(self.download_url(page_url))
        entries = soup.find_all(attrs={'lj-screenable' : 'social:widgets:parse'})
        for entry in entries:
            header = entry.find(class_='subj-link')
            header_text = header.string.strip()
            href = header['href']
            tags_list = []
            try:
                tags = entry.find(class_='ljtags')
                tags_hrefs = tags.find_all('a')
                for tag_href in tags_hrefs:
                    tags_list.append(tag_href.string.lower())
            except:
                pass

            timestamp = None
            abbr = entry.find(class_='updated')
            if abbr:
                timestamp = abbr['title']

            item = FeedItem(header_text, None, timestamp, tags_list, href)
            result.append(item)

        nav = None
        try:
            nav = soup.find(class_='page-nav').find(class_='prev').find('a')['href']
        except AttributeError as e:
            pass

        return (nav, result)


    def get_article(self, page_url):
        soup = BeautifulSoup(self.download_url(page_url))
        h1 = soup.find('h1')
        header = h1.string.strip()
        article = soup.find('article', class_='entry-content')

        s = str(article)
        item = FeedItem(header, s, None, None, page_url)

        return item

