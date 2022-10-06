
from typing import List
from models.DialogueState import DialogueState


class DialogueInteraction:

    """
    This is a node and edge in a dialogue graph

    The node is the state of the dialogue
    The edge is the action taken by the bot

    The edge is a list of actions because the bot can take multiple actions in a single turn

    """

    def __init__(self, state: DialogueState, actions: List[str]) -> None:
        self._state = state
        self._actions = actions

    @property
    def state(self) -> DialogueState:
        return self._state

    @property
    def actions(self) -> List[str]:
        return self._actions

    @actions.setter
    def actions(self, actions: List[str]):
        self._actions = actions
    
    def get_intentions(self) -> List[str]:
        return self._state.intentions

    def get_slots_names(self) -> List[str]:
        return [slot.name for slot in self._state.slots]

    def get_slots_values(self) -> List[str]:
        return [slot.value for slot in self._state.slots]

    def __str__(self) -> str:
        return str(self._state) + " ==> " + ",".join(self._actions)

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: 'DialogueInteraction') -> bool:
        return self._state == other._state and self._actions == other._actions
    
    def __ne__(self, other: 'DialogueInteraction') -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))
