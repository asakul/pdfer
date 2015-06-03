
from feedparsers.livejournal import LivejournalParser
from pdfsaver import PdfSaver

def main():
    lj = LivejournalParser()
    index_url = "http://anlazz.livejournal.com/"
    saver = PdfSaver("test.pdf")
    saver.save(lj, index_url)

if __name__ == "__main__":
    main()
