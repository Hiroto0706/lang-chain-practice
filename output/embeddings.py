import os
import shutil
from typing import List
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


INDEX_NAME = "vectorestore/%s-reading-note"

embeddings = OpenAIEmbeddings()


def embedding_document(username: str, docs: List[Document]) -> None:
    vectorstores = FAISS.from_documents(docs, embeddings)
    vectorstores.save_local(INDEX_NAME % username)


def create_vectorstore(username: str) -> FAISS:
    return FAISS.load_local(
        INDEX_NAME % username, embeddings, allow_dangerous_deserialization=True
    )


def clean_up_vectorstore(username: str):
    index_dir = INDEX_NAME % username
    if os.path.exists(index_dir) and os.path.isdir(index_dir):
        shutil.rmtree(index_dir)
        print(f"Vectorstore directory {index_dir} has been removed")
    else:
        print(f"Vectorstore directory {index_dir} does not exist.")
