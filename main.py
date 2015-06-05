
from feedparsers.livejournal import LivejournalParser
from pdfsaver import PdfSaver
from texsaver import TexSaver
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser(description="Blog-to-pdf converter")
    parser.add_argument('-o', '--output', action='store', dest='output', help='Output pdf filename', required=True)
    parser.add_argument('-u', '--url', action='store', dest='url', help='URL of blog', required=True)
    parser.add_argument('-l', '--limit', action='store', dest='limit', help='Limit number of entries')
    parser.add_argument('-f', '--font', action='store', dest='font', help='Path to font file (should be ttf)')
    parser.add_argument('-s', '--start-time', action='store', dest='start_time', help='Start download from given time (YYYYMMDD_HHMMSS')

    args = parser.parse_args()
    limit = None
    if args.limit:
        limit = int(args.limit)

    font = None
    if args.font:
        font = args.font

    start_time = None
    if args.start_time:
        start_time = datetime.datetime.strptime(args.start_time, "%Y%m%d_%H%M%S")

    lj = LivejournalParser()
    index_url = args.url
    saver = TexSaver(args.output)
    saver.save(lj, index_url, limit, start_time)

if __name__ == "__main__":
    main()
