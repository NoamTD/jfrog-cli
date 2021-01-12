from .service import Service


class System(Service):
    def ping(self):
        OK = "OK"

        response = self.requester.get("api/system/ping")

        if response == OK:
            return True
        else:
            return False

    def version(self):
        return self.requester.get("api/system/version", response_is_json=True)