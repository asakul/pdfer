
from feedparsers.livejournal import LivejournalParser
from pdfsaver import PdfSaver
import argparse

def main():
    parser = argparse.ArgumentParser(description="Blog-to-pdf converter")
    parser.add_argument('-o', '--output', action='store', dest='output', help='Output pdf filename', required=True)
    parser.add_argument('-u', '--url', action='store', dest='url', help='URL of blog', required=True)

    args = parser.parse_args()

    lj = LivejournalParser()
    index_url = args.url
    saver = PdfSaver(args.output)
    saver.save(lj, index_url)

if __name__ == "__main__":
    main()
