from typing import List


class SchemaDatabase:

    def __init__(self):
        dataset_schema = {
            "Dialogue ID": [],
            "Domain": [],
            "Task": [],
            "User Utterance": [],
            "Intent": [],
            "Domain_Intent": [],
            "Atomic_Intent": [],
            "Domain_Atomic_Intent": [],
            "Slots": [],
            "Slots Value": [],
            "Bot Response": [],
            "Action": [],
            "Domain_Action": [],
            "Atomic_Action": [],
            "Domain_Atomic_Action": [],
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
        self.dataset_schema["Intent"].append(intention)

    def add_atomic_intent(self, atomic_intent: str) -> None:
        self.dataset_schema["Atomic_Intent"].append(atomic_intent)

    def add_slots(self, slots: List[str]) -> None:
        self.dataset_schema["Slots"].append(slots)

    def add_slots_value(self, slots_value: List[str]) -> None:
        self.dataset_schema["Slots Value"].append(slots_value)

    def add_bot_response(self, bot_response: str) -> None:
        self.dataset_schema["Bot Response"].append(bot_response)

    def add_action(self, action: str) -> None:
        self.dataset_schema["Action"].append(action)

    def add_atomic_action(self, atomic_action: str) -> None:
        self.dataset_schema["Atomic_Action"].append(atomic_action)

    def add_domain_intent(self, domain_intent: str) -> None:
        self.dataset_schema["Domain_Intent"].append(domain_intent)

    def add_domain_atomic_intent(self, domain_atomic_intent: str) -> None:
        self.dataset_schema["Domain_Atomic_Intent"].append(domain_atomic_intent)

    def add_domain_action(self, domain_action: str) -> None:
        self.dataset_schema["Domain_Action"].append(domain_action)

    def add_domain_atomic_action(self, domain_atomic_action: str) -> None:
        self.dataset_schema["Domain_Atomic_Action"].append(domain_atomic_action)

    def add_type(self, type: str) -> None:
        self.dataset_schema["Type"].append(type)

    def get_dataset_schema(self) -> dict:
        return self.dataset_schema
