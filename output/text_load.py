import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader, NotionDBLoader

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")


def loading_text(target_file: str) -> List[Document]:
    loader = TextLoader("./assets/" + target_file)
    return loader.load()


def loading_notion_db() -> List[Document]:
    loader = NotionDBLoader(
        integration_token=NOTION_TOKEN,
        database_id=DATABASE_ID,
        request_timeout_sec=30
    )
    return loader.load()
