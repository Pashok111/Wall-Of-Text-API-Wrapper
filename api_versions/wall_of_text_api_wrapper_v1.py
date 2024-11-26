import requests
from requests.exceptions import HTTPError
from typing import List
from dataclasses import dataclass

__all__ = ["WallOfTextAPIWrapperV1", "TextCreateV1", "TextResponseV1"]
__version__ = "1.0.0"


@dataclass
class TextCreateV1:
    text: str
    username: str = "Anonymous"


@dataclass
class TextResponseV1:
    username: str
    text: str
    id: int
    created_at_utc: str


class WallOfTextAPIWrapperV1:
    def __init__(self, api_server):
        self.api_server = api_server + "/v1"

        response = requests.get(self.api_server)
        if response.status_code != 201:
            raise HTTPError({"code": response.status_code,
                             "response": response.json()})

        welcome_text_start = "This is the Wall Of Text API."
        is_welcome_text = "welcome_text" in response.json()
        is_welcome_text_right = response.json()[
            "welcome_text"].startswith(welcome_text_start)

        if not is_welcome_text or not is_welcome_text_right:
            raise ValueError("Invalid API server")

    def create_text(self,
                    text: str = None,
                    username: str = "Anonymous",
                    text_create: TextCreateV1 = None
                    ) -> TextResponseV1:
        if text is None and text_create is None:
            raise ValueError("One of the parameters \"text\" or "
                             "\"text_create\" must be provided")

        if text_create:
            text = text_create.text
            username = text_create.username

        post_data = {"text": text, "username": username}
        response = requests.post(f"{self.api_server}/texts", json=post_data)

        if response.status_code != 201:
            raise HTTPError({"code": response.status_code,
                             "response": response.json()})

        return TextResponseV1(**response.json())

    def get_texts(self,
                  limit: int = 100,
                  offset: int = 0
                  ) -> List[TextResponseV1]:
        if limit < 1:
            raise ValueError("Limit must be greater than or equal to 1")
        if offset < 0:
            raise ValueError("Offset must be greater than or equal to 0")
        if limit > 1000:
            raise ValueError("Limit must be less than or equal to 1000")

        url = f"{self.api_server}/texts?limit={limit}&offset={offset}"
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPError({"code": response.status_code,
                             "response": response.json()})
        return [TextResponseV1(**text) for text in response.json()]
