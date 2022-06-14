import requests


class BaseRequest(object):
    response = None

    def __init__(self, url, auth=None, headers={"Content-Type": "application/json"},
                 body=None, params=None):
        self.url = url
        self.headers = headers
        self.body = body
        self.params = params
        self.auth = auth

    def raise_for_status(self):
        self.response.raise_for_status()
        return self.response

    def get(self):
        self.response = requests.get(
            url=self.url,
            headers=self.headers,
            json=self.body,
            params=self.params,
            auth=self.auth,
            timeout=None,
        )
        return self.raise_for_status()

    def post(self):
        self.response = requests.post(
            url=self.url,
            headers=self.headers,
            json=self.body,
            params=self.params,
            auth=self.auth,
        )
        return self.raise_for_status()
