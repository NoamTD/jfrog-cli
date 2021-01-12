from .requester import Requester
from .system import System
from .user import User
from .storage import Storage


class Api:
    def __init__(self, host, username, password):
        artifactoryRequester = Requester(host, "artifactory", username, password)

        self.system = System(artifactoryRequester)
        self.storage = Storage(artifactoryRequester)
        self.user = User(artifactoryRequester)