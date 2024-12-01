from typing import List
from api_versions.wall_of_text_api_wrapper_v1 import WallOfTextAPIWrapperV1, TextCreateV1, TextResponseV1

__all__ = ["WallOfTextAPIWrapperLatest", "TextCreateLatest", "TextResponseLatest",
           "WallOfTextAPIWrapperV1", "TextCreateV1", "TextResponseV1"]
__version__ = "1.0.0"


class TextCreateLatest(TextCreateV1):
    pass


class TextResponseLatest(TextResponseV1):
    pass


class WallOfTextAPIWrapperLatest(WallOfTextAPIWrapperV1):
    def __init__(self, api_server: str):
        super().__init__(api_server)

    def create_text(self,
                    text: str = None,
                    username: str = "Anonymous",
                    text_create: TextCreateLatest = None
                    ) -> TextResponseLatest:
        original_response = super().create_text(text, username, text_create)
        return TextResponseLatest(**original_response.__dict__)

    def get_texts(self,
                  limit: int = 100,
                  offset: int = 0
                  ) -> List[TextResponseLatest]:
        original_response = super().get_texts(limit, offset)
        return [TextResponseLatest(**text.__dict__)
                for text in original_response]
