from .api_versions.v1.wrapper import (
    WallOfTextAPIWrapperV1, TextCreateV1, TextResponseV1
)

__all__ = [
    "WallOfTextAPIWrapperLatest", "TextCreateLatest", "TextResponseLatest",
    "WallOfTextAPIWrapperV1", "TextCreateV1", "TextResponseV1"
]
__version__ = "1.0.0"

TextCreateLatest = TextCreateV1
TextResponseLatest = TextResponseV1
WallOfTextAPIWrapperLatest = WallOfTextAPIWrapperV1
