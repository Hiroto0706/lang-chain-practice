import os
from langchain_pinecone import Pinecone, PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv


load_dotenv()


embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def ingest_docs():
    loader = ReadTheDocsLoader(
        "langchain-docs/api.python.langchain.com/en/latest"
    )
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600, chunk_overlap=50
    )
    documents = text_splitter.split_documents(raw_documents)

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "http:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(
        documents, embeddings, index_name="langchain-doc-index"
    )
    print("****Loading to vectorstore done ****")


def ingest_docs2() -> None:
    from langchain_community.document_loaders import FireCrawlLoader

    langchain_documents_base_urls = [
        "https://monta-database.notion.site/f9257d2f834d416ab2e65397f17072a7",
        "https://monta-database.notion.site/188a9974e2aa4e21b7892f39083569a9",
        "https://monta-database.notion.site/057600135ae44d49ad433abcac0c5bfe"
    ]

    for url in langchain_documents_base_urls:
        print(f"FireCrawling {url=}")

        loader = FireCrawlLoader(
            url=url,
            mode="scrape",
        )

        raw_docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000, chunk_overlap=100
        )
        documents = text_splitter.split_documents(raw_docs)

        PineconeVectorStore.from_documents(
            documents, embeddings, index_name="firecrawl-index"
        )

        print(f"**** Loading {url}* to vectorestore done ****")


if __name__ == "__main__":
    # ingest_docs()
    ingest_docs2()
