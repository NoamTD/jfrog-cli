from .requester import Requester

class Service:
    def __init__(self, requester: Requester):
        self.requester = requester