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