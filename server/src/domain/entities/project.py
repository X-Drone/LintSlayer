from pathlib import Path


class Project:
    id: int | None
    owner: str
    name: str
    repo_path: Path
    
    def __init__(self,
                 id: int | None,
                 owner: str,
                 name: str,
                 repo_path: Path
            ) -> None:
        self.id = id
        self.owner = owner
        self.name = name
        self.repo_path = repo_path
    
    @staticmethod
    def create(owner: str,
               name: str,
               repo_path: Path
            ) -> "Project":
        return Project(None,
                       owner,
                       name,
                       repo_path)
