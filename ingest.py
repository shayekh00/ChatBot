# ingest.py
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS   # swap for Chroma, PGVector, etc.

DOCS_PATH = "docs/"          # put txt / pdf / md files here
INDEX_PATH = "faiss_index/"  # where FAISS files live

loader = DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

embeddings = OpenAIEmbeddings()
vectordb = FAISS.from_documents(documents, embeddings)
vectordb.save_local(INDEX_PATH)
print("✅ Vector store built.")
