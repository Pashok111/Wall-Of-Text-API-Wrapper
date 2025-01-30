import requests
from requests.exceptions import HTTPError, JSONDecodeError

from typing import List

from .dataclasses import TextCreateV1, TextResponseV1

__all__ = ["WallOfTextAPIWrapperV1", "TextCreateV1", "TextResponseV1"]
__version__ = "1.0.0"


class WallOfTextAPIWrapperV1:
    def __init__(self, api_server):
        self.api_server = api_server + "/v1"

        response = requests.get(self.api_server)
        is_welcome_text_right = False
        welcome_text_start = "This is the Wall Of Text API."

        if response.status_code == 200:

            try:
                response_json = response.json()
            except JSONDecodeError:
                error = "Invalid API server"
                raise ValueError(error)

            is_welcome_text = "welcome_text" in response_json
            if is_welcome_text:
                is_welcome_text_right = response_json[
                    "welcome_text"].startswith(welcome_text_start)

            if not is_welcome_text or not is_welcome_text_right:
                error = "Invalid API server"
                raise ValueError(error)

        elif response.status_code == 404:
            error = "Invalid API server or this endpoint does not exist"
            raise ValueError(error)

        else:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

    def create_text(
            self,
            text: str,
            username: str = "Anonymous",
            parent_id: int = -1
    ) -> TextResponseV1:
        text_create = TextCreateV1(
            text=text, username=username, parent_id=parent_id
        )

        post_data = {
            "text": text_create.text,
            "username": text_create.username,
            "parent_id": text_create.parent_id
        }
        response = requests.post(f"{self.api_server}/texts", json=post_data)

        if response.status_code == 400:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code != 201:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return TextResponseV1(**response.json())

    def get_text(
            self,
            _id: int,
            include_comments: bool = True
    ) -> TextResponseV1:
        if not isinstance(_id, int):
            error = "ID must be of type <int>"
            raise ValueError(error)
        if not isinstance(include_comments, bool):
            error = "Include_comments must be of type <bool>"
            raise ValueError(error)

        url = (f"{self.api_server}/texts/{_id}"
               f"?include_comments={int(include_comments)}")
        response = requests.get(url)

        if response.status_code == 400:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code != 200:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return TextResponseV1(**response.json())

    def get_texts(
            self,
            limit: int = 100,
            offset: int = 0,
            parent_id: int = None,
            include_comments: bool = True
    ) -> List[TextResponseV1]:
        if not parent_id:
            parent_id = -1
        errors = []
        if not isinstance(limit, int):
            errors.append("Limit must be of type <int>")
        if not isinstance(offset, int):
            errors.append("Offset must be of type <int>")
        if not isinstance(parent_id, int):
            errors.append("Parent_id must be of type <int>")
        if not isinstance(include_comments, bool):
            errors.append("Include_comments must be of type <bool>")

        if limit < 1:
            errors.append("Limit must be greater than or equal to 1")
        if limit > 1000:
            errors.append("Limit must be less than or equal to 1000")
        if offset < 0:
            errors.append("Offset must be greater than or equal to 0")

        if errors:
            errors = "\n\nThe following errors occurred:\n" + "\n".join(errors)
            raise ValueError(errors)

        url = (f"{self.api_server}/texts"
               f"?limit={limit}"
               f"&offset={offset}"
               f"&parent_id={parent_id}"
               f"&include_comments={int(include_comments)}")
        response = requests.get(url)

        if response.status_code == 400:
            error = response.json()["error"]
            raise ValueError(error)
        if response.status_code != 200:
            error = {"code": response.status_code, "response": response.json()}
            raise HTTPError(error)

        return [TextResponseV1(**text) for text in response.json()]
