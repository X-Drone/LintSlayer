__version__ = "1.0.0"
__author__ = "X-Drone"


from app.service_container import ServiceContainer
from core import settings

from .analysers import get_all_analysers
from .auth_client import AuthClient
from .repo_manager import RepoManager
from ..persist.uow import UnitOfWork
from ..persist import db

auth_client = AuthClient(settings.auth_url) # get url from settings
repo_manager = RepoManager() # get path from settings
uow = UnitOfWork(db.getSession)

container = ServiceContainer(uow, repo_manager, auth_client, get_all_analysers())


__all__ = [
    "__version__",
    "__author__",
    "container",
]
