from ebooklib import epub
from core.config import constants
import itertools
import re


class Bookbinder:
    def __init__(self):
        self.chapterList = []
        self.no_per_volume = 200
        self.toc = []
        self.filterFileName = "[#%<>&{{}}\/?*$:@+`|=;]"

        self.book = epub.EpubBook()
        self.book.set_language("en")
        self._page_id = map("{:04}".format, itertools.count(1))


    def add_chapter(self, title, para):
        fileName = re.sub(self.filterFileName, "", title)
        fileName = fileName.replace("’", "'")

        c = epub.EpubHtml(
            file_name=f"chapter{next(self._page_id)}.xhtml",
            title=fileName,
            lang="hr",
            content=f"<h2>{title}</h2>\n\n{para}",
            direction=self.book.direction,
        )
        self.book.add_item(c)
        self.chapterList.append(c)
        self.book.spine.append(c)


    def make_intro_page(self, title: str, authors: list[str], url: str, coverimg):
        if len(authors) > 1:
            authors = ",".join(i for i in authors)
        elif len(authors) == 1:
            authors = authors[0]

        intro_html = '<div style="%s">' % ";".join(
            [
                "display: flex",
                "text-align: center",
                "flex-direction: column",
                "justify-content: space-between",
                "align-items: center",
            ]
        )

        intro_html += """
            <div>
                <h1>%s</h1>
                <h3>%s</h3>
            </div>
        """ % (
            title or "N/A",
            authors or "N/A",
        )

        if coverimg != None:
            intro_html += '<img id="cover" src="%s" style="%s">' % (
                "cover-img.jpg",
                "; ".join(
                    [
                        "height: 30vh",
                        "object-fit: contain",
                        "object-position: center center",
                    ]
                ),
            )

        intro_html += """
        <div>
            <br>
            <a href="%s">source</a><br>
            <i>Scraped by <b>eboo</b></i>
        </div>""" % (
            url
        )

        intro_html += "</div>"

        return epub.EpubHtml(
            uid="intro", file_name="intro.xhtml", title="Intro", content=intro_html
        )


    def create_book(self, title: str, source_url: str, authors: list[str] = [], img=None):
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self.book.set_title(title)

        intro_page = self.make_intro_page(title, authors, source_url, img)

        if img != None:
            self.book.set_cover("cover-img.jpg", img, create_page=False)

        splitter = [
            self.chapterList[i : i + self.no_per_volume]
            for i in range(0, len(self.chapterList), self.no_per_volume)
        ]

        for i in splitter:
            volume_no = splitter.index(i)
            self.toc.append(
                (
                    epub.Section(f"Volume {volume_no+1}"),
                    tuple(splitter[volume_no]),
                )
            )

        if len(authors) > 1:
            for j in authors:
                self.book.add_author(j)
        elif len(authors) <= 1:
            self.book.add_author(authors[0])

        self.book.add_item(intro_page)

        self.book.toc = tuple(self.toc)
        self.book.spine = [intro_page, "nav"] + self.chapterList

        epub_path = f"{title}.epub"
        epub.write_epub(epub_path, self.book)

        return epub_path
