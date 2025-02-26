from dotenv import load_dotenv
from embeddings import clean_up_vectorstore, create_vectorstore, embedding_document
from rag import create_rag_chain
from split import split_text
from langchain_core.output_parsers import StrOutputParser

from text_load import loading_notion_db, loading_text


load_dotenv()


def main(username: str = "test"):
    print("Start...!")

    # documents = loading_text("note_1.txt")
    documents = loading_notion_db()
    print(f"documents {documents}")

    docs = split_text(documents, 2000, 200)
    print(f"text length {len(docs)}")

    # embedding_document(username, docs)

    # vectorstore = create_vectorstore(username)
    # chain = create_rag_chain(retriever=vectorstore.as_retriever())

    # print(
    #     chain.invoke(
    #         {
    #             "input": "行動経済学の理解度をチェックするための確認問題を10問生成してください。それぞれの問題は4択の選択形式の問題であること。最終的なアウトプットはJSON形式でquestion, options, answer, explanationの4つで構成されること。問題の難易度は難しいでお願いします"
    #         }
    #     )["answer"]
    # )

    # clean_up_vectorstore(username)


if __name__ == "__main__":
    main(username="monta")
