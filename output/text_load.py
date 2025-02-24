from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import TextLoader


def loading_text(target_file: str) -> List[Document]:
    loader = TextLoader("./assets/" + target_file)
    return loader.load()
