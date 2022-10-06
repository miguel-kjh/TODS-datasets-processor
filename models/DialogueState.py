from typing import List


class DialogueState:

    def __init__(self, intentions: List[str], slots: List[str] = None) -> None:
        if slots is None:
            slots = []

        self.intentions = intentions
        self.slots = slots

    def __str__(self) -> str:
        return f'{",".join(self.intentions)}({self.slots})'

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'DialogueState') -> bool:
        return self.intentions == other.intentions #and self.slots == other.slots

    def __ne__(self, other: 'DialogueState') -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))
