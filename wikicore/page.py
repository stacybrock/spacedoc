import io
import markdown
import os
import re
import yaml

class WikiPage():
    wiki = None

    def __init__(self, pageblob):
        self.path = pageblob.path
        self.fullpath = pageblob.abspath

        if re.search(r'\.md$', self.path, re.IGNORECASE):
            self.docformat = 'markdown'
        elif re.search(r'\.txt$', self.path, re.IGNORECASE):
            self.docformat = 'text'

        with io.BytesIO(pageblob.data_stream.read()) as f:
            self.raw = f.read().decode('utf-8')

        self.frontmatter = None
        match = re.match(r'(---\n.+\n)---.*$', self.raw, re.MULTILINE)
        if match:
            self.frontmatter = match[1]

        self.tags = None
        if self.frontmatter is not None:
            yamlparts = yaml.load(self.frontmatter)
            self.tags = yamlparts['tags']

        self.content = re.sub(r'^---\n(.+)\n---\n', '', self.raw, re.MULTILINE)

    def __str__(self):
        return f"<WikiPage {self.path}>, tags=[{self.tags}]"

    def to_html(self):
        content = self.content

        wikilinks = re.findall(r'(\[\[.*?\]\])', content)
        for wikilink in wikilinks:
            rawlink = re.search(r'\[\[(.*?)\]\]', wikilink)[1]
            linkparts = rawlink.split('|')
            if len(linkparts) == 2:
                (linkpath, linktext) = linkparts
            elif len(linkparts) == 1:
                (linkpath, linktext) = (linkparts[0], linkparts[0])
            else:
                continue
            if linkpath is None or linktext is None:
                continue

            if self.docformat == 'markdown':
                content = re.sub(
                    re.escape(wikilink),
                    f"[{linktext}]({self.wiki.base_path}/{linkpath})",
                    content)

        html = ''
        if self.docformat == 'markdown':
            html = markdown.markdown(content,
                                     extensions=['fenced_code', 'sane_lists'])
        return html
