from abc import ABC
from pathlib import Path

class RepoSource(ABC):
    pass


class RepoFromText(RepoSource):
    def __init__(self, content: str, ext: str):
        self.content = content
        self.ext = ext


class RepoFromUrl(RepoSource):
    def __init__(self, url: str):
        self.url = url


class RepoFromPath(RepoSource):
    def __init__(self, path: Path):
        self.path = path
