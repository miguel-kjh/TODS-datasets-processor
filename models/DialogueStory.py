from typing import List
from models.DialogueInteraction import DialogueInteraction
from models.DialogueState import DialogueState


class DialogueStory:

    def __init__(self, id: str, domain: str):
        self.dialogue_story = []
        self._domain = domain
        self.id = id

    @property
    def domain(self) -> str:
        return self._domain

    @domain.setter
    def domain(self, domain: str):
        self._domain = domain

    def add_interaction(self, dialogue_interaction: DialogueInteraction) -> None:
        self.dialogue_story.append(dialogue_interaction)

    def add_intentions_actions(self, intention: List[str], actions: List[str], slots: List[str]) -> None:
        state = DialogueState(intention, slots)
        dialogue_interaction = DialogueInteraction(state, actions)
        self.dialogue_story.append(dialogue_interaction)

    def add_story(self, story: List):
        self.dialogue_story += story

    def get_interactions(self) -> List:
        return self.dialogue_story

    def get_intentions(self) -> List:
        return [interaction.get_intentions() for interaction in self.dialogue_story]

    def get_actions(self) -> List:
        return [interaction.actions for interaction in self.dialogue_story]
                
    def get_id(self) -> str:
        return self.id

    def __len__(self) -> int:
        return len(self.dialogue_story)

    def __str__(self) -> str:
        return f"{self.id}: {self.dialogue_story}\n"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        return self.dialogue_story == other.dialogue_story

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(str(self))
