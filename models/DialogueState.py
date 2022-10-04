from typing import List


class DialogueState:

    def __init__(self, intentions: List[str]) -> None:
        self.intentions = intentions

    def __str__(self) -> str:
        return f'{",".join(self.intentions)}'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'DialogueState') -> bool:
        return self.intentions == other.intentions

    def __ne__(self, other: 'DialogueState') -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))

