
from feedparsers.livejournal import LivejournalParser
from fpdf import FPDF
import re

def expand_tags(html):
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


def make_chapter(pdf, item):
    title = item.title
    s = item.html_content


    pdf.set_font('dejavu', '', 16)
    pdf.cell(0, 6, txt=title, align='C')
    pdf.ln(12)

    parts = expand_tags(s)

    pdf.set_font('dejavu', '', 12)
    for part in parts:
        if part[0] == "text":
            pdf.multi_cell(0, 5, part[1]) 
        elif part[0] == "image":
            print(part[1])
            pdf.image(part[1])

def main():
    lj = LivejournalParser()
    index = lj.get_index("http://anlazz.livejournal.com/")
    pdf = FPDF()
    pdf.add_font('dejavu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
    for item in index[1][:1]:
        new_item = lj.get_article(item.link)
        new_item.timestamp = item.timestamp
        new_item.tags = item.tags
        pdf.add_page()
        make_chapter(pdf, new_item)

    pdf.output('test.pdf')

if __name__ == "__main__":
    main()
