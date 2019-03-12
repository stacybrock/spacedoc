import re
from git import Repo
from git.exc import GitCommandError

from .page import WikiPage

class Wiki():
    def __init__(self, repo_path, base_path=None):
        if base_path is None:
            self.base_path = ''
        else:
            self.base_path = base_path
        self.repo = Repo(repo_path)

    def __del__(self):
        self.repo.__del__()

    def close(self):
        self.__del__()

    def base_path(self):
        return self.base_path

    def get_page(self, pagename):
        try:
            file_ = self.repo.heads.master.commit.tree[pagename]
        except KeyError as err:
            # TODO log error
            return None
        return WikiPage(file_)

    def search(self, term, case_insensitive=False, return_raw=False):
        try:
            if case_insensitive:
                results = self.repo.git.grep('-i', term).split('\n')
            else:
                results = self.repo.git.grep(term).split('\n')
        except GitCommandError as err:
            return []

        if return_raw:
            return results

        processed = []
        for result in results:
            matches = re.search(r"(.*?):", result)
            if matches:
                (page, context) = result.split(':', 1)
                result_link = f"<a href='{self.base_path}/{page}'>{page}</a>"
                regex = re.compile('('+re.escape(term)+')', re.IGNORECASE)
                context = re.sub(regex, r"<span class='highlight'>\1</span>",
                                 context)
                processed.append(f"{result_link} - {context}")
            else:
                processed.append(result)
        return processed

    def _linkify(self, path, string):
        return re.sub(re.escape(path),
                      f"<a href='{self.base_path}/{path}'>{path}</a>", string)
