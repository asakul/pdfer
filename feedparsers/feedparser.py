
from urllib.request import urlopen

class FeedItem:
    def __init__(self, title, html_content, timestamp, tags, link=None):
        self.title = title
        self.html_content = html_content
        self.tags = tags
        self.timestamp = timestamp
        self.link = link
        self.images = {}

    def add_image(self, url, image_data):
        self.images[url] = image_data

class FeedParser:
    def __init__(self):
        pass

    def id(self):
        pass

    def download_url(self, url):
        r = urlopen(url)
        return r.read()

    def get_index(self, page_url):
        """
        Returns: (next_page_url, [entries])
        """
        pass

    def get_article(self, page_url):
        """
        Returns: [entries]
        """
        pass

