import requests
import requests.auth


class Requester:

    TOKEN_URI = "api/security/token"
    TOKEN_REVOKE_URI = f"{TOKEN_URI}/revoke"

    TOKEN_DURATION_SECONDS = "5"

    @property
    def host(self):
        return self._host

    def __init__(self, host: str, app, username: str, password: str):
        self._host = host
        self._app = app
        self.username = username
        self.password = password
        self.token_data = None

    def _url(self, uri):
        return f"{self._host}/{self._app}/{uri}"

    def _token_request(self, extra_data, type):
        data = {
            "username": self.username,
            "expires_in": Requester.TOKEN_DURATION_SECONDS,
            "refreshable": True,
        }
        data.update(extra_data)

        try:
            url = self._url(Requester.TOKEN_URI)
            auth = requests.auth.HTTPBasicAuth(self.username, self.password)

            response = requests.post(
                url,
                auth=auth,
                data=data,
                headers={"ContentType": "application/x-www-form-urlencoded"},
            )

            if response.status_code == 401:
                print("Invalid username/password")
                exit(1)

            if not response.ok:
                raise Exception(response.json())

            self.token_data = response.json()
        except Exception as err:
            raise Exception(f"authentication token {type} failed. Error: {err}")

    def _delete_token(self):
        url = self._url(Requester.TOKEN_URI)
        data = { "token": self.token_data["access_token"]}

        requests.post(url, data)

    def _create_token(self):
        data = {"username": self.username, "scope": "member-of-groups:*"}

        self._token_request(data, "create")

    def _refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "access_token": self.token_data["access_token"],
            "refresh_token": self.token_data["refresh_token"],
        }

        self._token_request(data, "update")

    def _auth_header(self):
        return {"Authorization": f"Bearer {self.token_data['access_token']}"}

    def with_token_retry(func):
        def wrapper(self, *args, **kwargs):
            if self.token_data is None:
                self._create_token()

            try:
                return func(self, *args, **kwargs)
            except:
                try:
                    self._refresh_token()
                    return func(self, *args, **kwargs)
                except Exception as err:
                    raise Exception(err.with_traceback)

        return wrapper

    @with_token_retry
    def _request(self, type: str, uri: str, response_is_json: bool, content_type, *args, **kwargs):
        request_methods = {
            "get": requests.get,
            "post": requests.post,
            "put": requests.put,
            "delete": requests.delete,
        }

        url = self._url(uri)
        headers = self._auth_header()

        if content_type:
            headers["Content-Type"] = content_type

        response = request_methods[type](url, headers=headers, *args, **kwargs)

        if not response.ok:
            raise Exception(f"request failed. error: {response.text}")

        if response_is_json:
            return response.json()
        else:
            return response.text

    def get(self, uri, response_is_json: bool = False, content_type = None, *args, **kwargs):
        return self._request("get", uri, response_is_json, content_type=content_type, *args, **kwargs)

    def put(self, uri, response_is_json: bool = False, content_type = None, *args, **kwargs):
        return self._request("put", uri, response_is_json, content_type=content_type, *args, **kwargs)

    def post(self, uri, response_is_json: bool = False, content_type = None, *args, **kwargs):
        return self._request("post", uri, response_is_json, content_type=content_type, *args, **kwargs)

    def delete(self, uri, response_is_json: bool = False, content_type = None, *args, **kwargs):
        return self._request("delete", uri, response_is_json, content_type=content_type, *args, **kwargs)

    def clean_up(self):
        self._delete_token()