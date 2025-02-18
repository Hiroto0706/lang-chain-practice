from langchain_pinecone import PineconeVectorStore
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


if __name__ == "__main__":
    ingest_docs()
