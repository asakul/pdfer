
from fpdf import FPDF
import re

class PdfSaver:
    def __init__(self, filename):
        self.filename = filename
        self.pdf = FPDF()

    def _expand_tags(self, html):
        s = html
        s = re.sub(r'<br\W*>', '\n', s, flags=re.M)
        splitted = re.split(r'(<img.*>|<a .*>.*</a>)', s)
        result = []
        for sp in splitted:
            if sp.startswith("<img"):
                m = re.search(r'<img.*src="([^"]*)"', sp, re.M)
                mw = re.search(r'<img.*width="([^"]*)"', sp, re.M)
                mh = re.search(r'<img.*height="([^"]*)"', sp, re.M)
                if mw and mh:
                    result.append(("image", m.group(1), float(mw.group(1)), float(mh.group(1))))
                else:
                    result.append(("image", m.group(1)))
            else:
                stripped = re.sub(r'<[^>]*>', '', sp, flags=re.M)
                result.append(("text", stripped))
            if sp.startswith("<a "):
                img = sp.find('<img ')
                if img >= 0:
                    m = re.search(r'<img.*src="([^"]*)"', sp, re.M)
                    mw = re.search(r'<img.*width="([^"]*)"', sp, re.M)
                    mh = re.search(r'<img.*height="([^"]*)"', sp, re.M)
                    if mw and mh:
                        result.append(("image", m.group(1), float(mw.group(1)), float(mh.group(1))))
                    else:
                        result.append(("image", m.group(1)))
                else:
                    m = re.search(r'<a .*href="([^"]*)".*>(.*)</a>', sp, re.M)
                    if m:
                        result.append(("link", m.group(1), m.group(2)))

        return result 

    def _make_chapter(self, pdf, item):
        title = item.title
        s = item.html_content

        self.pdf.set_font('dejavu', '', 16)
        self.pdf.cell(0, 6, txt=title, align='C')
        self.pdf.ln(12)

        parts = self._expand_tags(s)

        self.pdf.set_font('dejavu', '', 12)
        for part in parts:
            if part[0] == "text":
                self.pdf.multi_cell(0, 5, part[1])
            elif part[0] == "image":
                try:
                    if len(part) == 2:
                        self.pdf.image(part[1])
                    else:
                        width = part[2]
                        height = part[3]

                        print(width, height, self.pdf.k, self.pdf.w, self.pdf.r_margin, self.pdf.l_margin)
                        if width / self.pdf.k > self.pdf.w - self.pdf.r_margin - self.pdf.l_margin:
                            self.pdf.image(part[1], w=self.pdf.w - self.pdf.r_margin - self.pdf.l_margin)
                        else:
                            self.pdf.image(part[1], w=width / self.pdf.k)
                except:
                    pass
            elif part[0] == "link":
                self.pdf.write(5, part[2], part[1])

    def collect_items(self, parser, raw_items, limit):
        items = []
        i = 0
        for item in raw_items:
            i += 1
            if limit and i > limit:
                break
            print("Downloading {0} / {1}".format(i, len(raw_items)))
            new_item = parser.get_article(item.link)
            new_item.timestamp = item.timestamp
            new_item.tags = item.tags
            if not new_item.title:
                new_item.title = item.title
            items.append(new_item)
        return items

    def save(self, parser, index_url, limit=None):
        self.pdf.add_font('dejavu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        items = []
        i = 0
        while index_url:
            index = parser.get_index(index_url)
            new_items = self.collect_items(parser, index[1], limit)
            i += len(new_items)
            items += new_items
            if limit:
                print("Downloaded {0} / {1}".format(i, limit))
                if i >= limit:
                    break
            else:
                print("Downloaded {0} / *".format(i))
            index_url = index[0]

        items.reverse()
        for item in items:
            self.pdf.add_page()
            self._make_chapter(self.pdf, item)

        self.pdf.output(self.filename)

