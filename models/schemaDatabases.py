from typing import List


class SchemaDatabase:

    def __init__(self):
        dataset_schema = {
            "Dialogue ID": [],
            "Domain": [],
            "Task": [],
            "User Utterance": [],
            "Intention": [],
            "Atomic Intent": [],
            "Slots": [],
            "Slots Value": [],
            "Bot Response": [],
            "Action": [],
            "Atomic Action": [],
            "Type": [],
        }

        self.dataset_schema = dataset_schema

    def add_dialogue_id(self, dialogue_id: str) -> None:
        self.dataset_schema["Dialogue ID"].append(dialogue_id)

    def add_domain(self, domain: str) -> None:
        self.dataset_schema["Domain"].append(domain)

    def add_task(self, task: str) -> None:
        self.dataset_schema["Task"].append(task)

    def add_user_utterance(self, user_utterance: str) -> None:
        self.dataset_schema["User Utterance"].append(user_utterance)

    def add_intention(self, intention: str) -> None:
        self.dataset_schema["Intention"].append(intention)

    def add_atomic_intent(self, atomic_intent: str) -> None:
        self.dataset_schema["Atomic Intent"].append(atomic_intent)

    def add_slots(self, slots: List[str]) -> None:
        self.dataset_schema["Slots"].append(slots)

    def add_slots_value(self, slots_value: List[str]) -> None:
        self.dataset_schema["Slots Value"].append(slots_value)

    def add_bot_response(self, bot_response: str) -> None:
        self.dataset_schema["Bot Response"].append(bot_response)

    def add_action(self, action: str) -> None:
        self.dataset_schema["Action"].append(action)

    def add_atomic_action(self, atomic_action: str) -> None:
        self.dataset_schema["Atomic Action"].append(atomic_action)

    def add_type(self, type: str) -> None:
        self.dataset_schema["Type"].append(type)

    def get_dataset_schema(self) -> dict:
        return self.dataset_schema
