
from feedparsers.feedparser import FeedParser, FeedItem
from bs4 import BeautifulSoup

class LivejournalParser(FeedParser):
    def __init__(self):
        super().__init__()

    def id(self):
        return "livejournal"

    def get_index(self, page_url):
        soup = BeautifulSoup(download_url(page_url))

    def get_article(self, page_url):
        pass

