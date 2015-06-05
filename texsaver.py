
import re
from html.parser import HTMLParser

default_beginning = r"""
\documentclass[fontsize=9pt]{scrreprt}
\usepackage{listings}
\usepackage{color}
\usepackage[unicode=true,hidelinks]{hyperref}
\usepackage{fontspec}
\usepackage{xunicode}
\usepackage{xltxtra}
\usepackage{indentfirst}
\usepackage{polyglossia}
\setmainlanguage{russian} 
\setotherlanguage{english}
\usepackage[margin=1in]{geometry}

\usepackage{array}
\newcolumntype{S}{>{\tiny}l} 

\defaultfontfeatures{Ligatures=TeX}
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}

\definecolor{comments}{rgb}{0,0.6,0}
\definecolor{source_background}{rgb}{0.98,0.98,0.98}
\setcounter{secnumdepth}{5}
\begin{document}

"""

default_title = r"""
\title{{{0}}}
\maketitle
"""

default_ending = r"""
\end{document}
"""


def attr_value(attrs, key):
    for attr in attrs:
        if attr[0] == key:
            return attr[1]

    return None


class Parser(HTMLParser):
    def __init__(self, out):
        super().__init__()
        self.text_type = ["text"]
        self.link = None
        self.current_text = ""
        self.out = out

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            w = attr_value(attrs, "width")
            if w:
                w = float(w)
            h = attr_value(attrs, "height")
            if h:
                h = float(h)
            #self.result.append(("image", attr_value(attrs, "src"), w, h))
        elif tag == "br":
            self.out.write("\n\n")
        elif tag == "div":
            self.out.write("\n\n")
        elif tag == "a":
            self.link = attr_value(attrs, "href")
            if self.link:
                self.out.write(r'\href{{{0}}}{{'.format(self.link))
        elif tag == "b":
            self.out.write("\\textbf{")

    def handle_endtag(self, tag):
        if tag == "a":
            if self.link:
                self.out.write("}")
        elif tag == "b":
            self.out.write("}")

    def handle_data(self, data):
        data = data.replace('\\', '\\\\')
        data = data.replace('_', '\\_')
        self.out.write(data)

class TexSaver:
    def __init__(self, filename):
        self.filename = filename
        self.out = open(filename, "w+")

    def _begin_document(self):
        self.out.write(default_beginning)
        self.out.write(default_title.format("Foo"))
    
    def _end_document(self):
        self.out.write(default_ending)

    def _make_chapter(self, item):
        parser = Parser(self.out)
        self.out.write('\\chapter{{{0}}}\n'.format(item.title))
        parser.feed(item.html_content)

    def collect_items(self, parser, raw_items, limit, start_time):
        items = []
        i = 0
        for item in raw_items:
            i += 1
            if limit and i > limit:
                break

            if start_time and item.timestamp < start_time:
                continue

            print("Downloading {0} / {1}".format(i, len(raw_items)))
            new_item = parser.get_article(item.link)
            new_item.timestamp = item.timestamp
            new_item.tags = item.tags
            if not new_item.title:
                new_item.title = item.title
            items.append(new_item)
        return items

    def save(self, parser, index_url, limit=None, start_time=None):
        items = []
        i = 0
        while index_url:
            index = parser.get_index(index_url)
            new_items = self.collect_items(parser, index[1], limit, start_time)
            i += len(new_items)
            items += new_items
            if limit:
                print("Downloaded {0} / {1}".format(i, limit))
                if i >= limit:
                    break

            if start_time:
                if len(new_items) == 0:
                    print("Reached starting time")
                    break

            else:
                print("Downloaded {0} / *".format(i))
            index_url = index[0]

        self._begin_document()

        items.reverse()
        for item in items:
            self._make_chapter(item)

        self._end_document()

