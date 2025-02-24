from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


DIR_NAME = "my-notion-note"

embeddings = OpenAIEmbeddings()


def embedding_document(docs: List[Document]) -> None:
    vectorstores = FAISS.from_documents(docs, embeddings)
    vectorstores.save_local(DIR_NAME)


def create_vectorstore() -> FAISS:
    return FAISS.load_local(DIR_NAME, embeddings, allow_dangerous_deserialization=True)
