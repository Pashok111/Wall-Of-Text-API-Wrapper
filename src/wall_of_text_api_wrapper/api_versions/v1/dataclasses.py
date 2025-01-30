from typing import List
from datetime import datetime

from dataclasses import dataclass


@dataclass
class TextCreateV1:
    text: str
    username: str = "Anonymous"
    parent_id: int = -1

    def __post_init__(self):
        errors = []
        if not isinstance(self.text, str):
            errors.append("Text must be of type <str>")
        if not isinstance(self.username, str):
            errors.append("Username must be of type <str>")
        if not isinstance(self.parent_id, int):
            errors.append("Parent_id must be of type <int>")

        if errors:
            errors = "\n\nThe following errors occurred:\n" + "\n".join(errors)
            raise ValueError(errors)

        self.text = self.text.strip()
        self.username = self.username.strip()

        if not self.text:
            errors.append("Text cannot be empty")
        if not self.username:
            errors.append("Username cannot be empty")
        if len(self.username) < 3:
            errors.append("Username must be at least 3 characters long")

        if errors:
            errors = "\n\nThe following errors occurred:\n" + "\n".join(errors)
            raise ValueError(errors)


@dataclass
class TextResponseV1:
    username: str
    text: str
    parent_id: int
    id: int
    utc_created_at: datetime
    comment_depth: int
    comments: List["TextResponseV1"]

    def __post_init__(self):
        self.utc_created_at = datetime.fromtimestamp(self.utc_created_at)# noqa
        self.comments = [
            TextResponseV1(**comment) for comment in self.comments  # noqa
        ]

    def __str__(self):
        _depth = "  " * self.comment_depth
        _comments = "\n".join(
            [_depth + "Comments:\n"] +
            [str(i) for i in self.comments]
        ) if self.comments else ""
        return (f"{_depth}Text ID: {self.id}\n"
                f"{_depth}Parent ID: {self.parent_id}\n"
                f"{_depth}Username: {self.username}\n"
                f"{_depth}Text: {self.text}\n"
                f"{_depth}Create at (UTC): {self.utc_created_at}\n"
                + _comments)
