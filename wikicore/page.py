import io
import markdown
import re
import yaml

class WikiPage():
    def __init__(self, pageblob):
        self.path = pageblob.path

        if re.search(r'\.md$', self.path, re.IGNORECASE):
            self.docformat = 'markdown'
        elif re.search(r'\.adoc$', self.path, re.IGNORECASE):
            self.docformat = 'asciidoc'
        elif re.search(r'\.txt$', self.path, re.IGNORECASE):
            self.docformat = 'text'

        with io.BytesIO(pageblob.data_stream.read()) as f:
            self.raw = f.read().decode('utf-8')

        self.frontmatter = None
        match = re.match(r'(---\n.+\n---).*$', self.raw, re.MULTILINE)
        if match:
            self.frontmatter = match[1]

        self.tags = None
        if self.frontmatter is not None:
            yamlparts = yaml.load(self.frontmatter)
            self.tags = yamlparts['tags']

        self.content = re.sub(r'^---\n(.+)\n---\n', '', self.raw, re.MULTILINE)

    def __str__(self):
        return f"<WikiPage {self.path}> [{self.tags}]"

    def render_html(self, linkroot=None):
        if linkroot is None:
            linkroot = ''

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
                content = re.sub(re.escape(wikilink), \
                                 f"[{linktext}]({linkroot}/{linkpath})", content)
        # print(content)
        if self.docformat == 'markdown':
            return markdown.markdown(content)
