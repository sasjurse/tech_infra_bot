import json

from pydantic import BaseModel
from typing import Optional


DOCUMENTS_THAT_CAN_BE_RETRIEVED = ['document', 'requirements', 'project_plan', 'tech_summary', 'history']


def retrieve_document(document_type: str, project_id: int = 1):
    assert document_type in DOCUMENTS_THAT_CAN_BE_RETRIEVED, f'Invalid document type: {document_type}'
    path = f'../project_descriptions/{document_type} {project_id}'
    with open(path, 'r') as f:
        return f.read()


def store_document(document_type: str, document: str, project_id: int = 1):
    assert document_type in DOCUMENTS_THAT_CAN_BE_RETRIEVED, f'Invalid document type: {document_type}'
    path = f'../project_descriptions/{document_type} {project_id}'
    with open(path, 'w') as f:
        f.write(document)


class ChatEntry(BaseModel):
    role: str
    content: str
    feedback_rating: Optional[int] = None
    feedback_why: Optional[str] = None


class ChatHistory(BaseModel):
    entries: list[ChatEntry]

    def jsonl(self):
        return "\n".join(chat_entry.json() for chat_entry in self.entries)


def retrieve_history(project_id: int):
    path = f'../project_descriptions/history {project_id}.jsonl'
    with open(path, 'r') as f:
        entries = []
        for line in f:
            # when parsing the jsonl, keep in mind that the strings will contain newlines.
            # Pydantic's parse_raw struggled.
            params = json.loads(line)
            chat_entry = ChatEntry(**params)

            entries.append(chat_entry)
        return ChatHistory(entries=entries)


def add_to_history(role, content, project_id: int):
    chat_entry = ChatEntry(role=role, content=content)
    path = f'../project_descriptions/history {project_id}.jsonl'
    with open(path, 'a') as f:
        f.write(chat_entry.json() + "\n")
