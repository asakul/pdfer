
from feedparsers.livejournal import LivejournalParser
from pdfsaver import PdfSaver
import argparse

def main():
    parser = argparse.ArgumentParser(description="Blog-to-pdf converter")
    parser.add_argument('-o', '--output', action='store', dest='output', help='Output pdf filename', required=True)
    parser.add_argument('-u', '--url', action='store', dest='url', help='URL of blog', required=True)
    parser.add_argument('-l', '--limit', action='store', dest='limit', help='Limit number of entries')
    parser.add_argument('-f', '--font', action='store', dest='font', help='Path to font file (should be ttf)')

    args = parser.parse_args()
    limit = None
    if args.limit:
        limit = int(args.limit)

    font = None
    if args.font:
        font = args.font

    lj = LivejournalParser()
    index_url = args.url
    saver = PdfSaver(args.output, font)
    saver.save(lj, index_url, limit)

if __name__ == "__main__":
    main()
