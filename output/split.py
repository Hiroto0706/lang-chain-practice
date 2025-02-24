from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import CharacterTextSplitter


def split_text(
    docs: List[Document], chunk_size: int = 1000, overlap: int = 100
) -> List[Document]:
    text_spliter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return text_spliter.split_documents(documents=docs)
