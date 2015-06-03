
from fpdf import FPDF
import re

class PdfSaver:
    def __init__(self, filename):
        self.filename = filename
        self.pdf = FPDF()

    def _expand_tags(self, html):
        s = html
        s = re.sub(r'<br\W*>', '\n', s, flags=re.M)
        splitted = re.split(r'(<img.*>)', s)
        result = []
        for sp in splitted:
            if sp.startswith("<img"):
                m = re.search(r'<img.*src="([^"]*)"', sp, re.M)
                result.append(("image", m.group(1)))
            else:
                stripped = re.sub(r'<[^>]*>', '', sp, flags=re.M)
                result.append(("text", stripped))

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
                    self.pdf.image(part[1])
                except:
                    pass

    def save(self, parser, index_url):
        index = parser.get_index(index_url)
        self.pdf.add_font('dejavu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        for item in index[1]:
            new_item = parser.get_article(item.link)
            new_item.timestamp = item.timestamp
            new_item.tags = item.tags
            self.pdf.add_page()
            self._make_chapter(self.pdf, new_item)

        self.pdf.output(self.filename)

