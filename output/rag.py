from langchain_core.runnables import Runnable
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.vectorstores import VectorStoreRetriever


def create_rag_chain(retriever: VectorStoreRetriever) -> Runnable:
    # https://smith.langchain.com/hub/langchain-ai/retrieval-qa-chat?organizationId=53c75045-2148-4e85-a4a2-04c298ae5eda
    retrieval_qa_chain_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    llm = ChatOpenAI(model_name="gpt-4o-2024-05-13")

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chain_prompt)

    # リトリーブする数を8に固定
    # retriever.search_kwargs["k"] = 8

    return create_retrieval_chain(
        retriever=retriever, combine_docs_chain=combine_docs_chain
    )
