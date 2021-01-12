import typing
import json
from .service import Service


class User(Service):
    USER_URI = "api/security/users"

    def _user_uri(self, username):
        return f"{User.USER_URI}/{username}"

    def create(
        self,
        username: str,
        email: str,
        password: str,
        admin: bool = False,
        disableUIAcess: bool = True,
        groups: typing.List[str] = None,
    ):
        data = {
            "email": email,
            "password": password,
            "admin": admin,
            "disableUIAcess": disableUIAcess,
        }

        if groups is not None:
            data["groups"] = groups

        self.requester.put(
            self._user_uri(username), data=json.dumps(data), content_type="application/json"
        )

    def delete(self, username):
        self.requester.delete(self._user_uri(username))