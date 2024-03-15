import json

from pydantic import BaseModel
from typing import Optional


# This is just to create a rudimentary option for testing multiple files at once. The files no need to be
# created in advance or there will likely be a crash
PROJECT_VERSION = 1


def retrieve_requirements():
    path = f'../project_descriptions/requirements {PROJECT_VERSION}'
    with open(path, 'r') as f:
        return f.read()


def store_requirements(requirements: str):
    path = f'../project_descriptions/requirements {PROJECT_VERSION}'
    with open(path, 'w') as f:
        f.write(requirements)


def retrieve_plan():
    path = f'../project_descriptions/version {PROJECT_VERSION}'
    with open(path, 'r') as f:
        return f.read()


def store_plan(plan: str):
    path = f'../project_descriptions/version {PROJECT_VERSION}'
    with open(path, 'w') as f:
        f.write(plan)


class ChatEntry(BaseModel):
    role: str
    content: str
    feedback_rating: Optional[int] = None
    feedback_why: Optional[str] = None


class ChatHistory(BaseModel):
    entries: list[ChatEntry]

    def jsonl(self):
        return "\n".join(chat_entry.json() for chat_entry in self.entries)


def retrieve_history():
    path = f'../project_descriptions/history {PROJECT_VERSION}.jsonl'
    with open(path, 'r') as f:
        entries = []
        for line in f:
            # when parsing the jsonl, keep in mind that the strings will contain newlines.
            # Pydantic's parse_raw struggled.
            params = json.loads(line)
            chat_entry = ChatEntry(**params)

            entries.append(chat_entry)
        return ChatHistory(entries=entries)


def add_to_history(role, content):
    chat_entry = ChatEntry(role=role, content=content)
    path = f'../project_descriptions/history {PROJECT_VERSION}.jsonl'
    with open(path, 'a') as f:
        f.write(chat_entry.json() + "\n")
