"""Simple User model and serialization helpers.

This module provides a minimal `User` class used to hold a player's name
and a high score. It includes `to_dict`/`from_dict` helpers to serialize to
and from plain dictionaries suitable for JSON storage under `data/`.

"""


class User:
    def __init__(self, name: str, high_score: int):
        self.name = name
        self.high_score = high_score

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "high_score": self.high_score
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(data["name"], data["high_score"])