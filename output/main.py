from dotenv import load_dotenv
from embeddings import create_vectorstore, embedding_document
from rag import create_rag_chain
from split import split_text
from langchain_core.output_parsers import StrOutputParser

from text_load import loading_text


load_dotenv()


def main():
    print("Start...!")

    documents = loading_text("note_1.txt")

    docs = split_text(docs=documents)
    print(f"{len(docs)}")

    embedding_document(docs)

    vectorstore = create_vectorstore()
    chain = create_rag_chain(retriever=vectorstore.as_retriever())

    print(chain.invoke({"input": "行動経済学とはなんですか？"}))


if __name__ == "__main__":
    main()
