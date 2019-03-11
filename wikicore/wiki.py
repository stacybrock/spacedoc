from git import Repo

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
