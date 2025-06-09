# retriever.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_PATH = "faiss_index/"
embeddings = OpenAIEmbeddings()
_vectordb = FAISS.load_local(
    folder_path=INDEX_PATH,
    embeddings=embeddings,
    allow_dangerous_deserialization=True  # ✅ allow if YOU built it
)

def retrieve(query: str, k: int = 4):
    """Return top-k relevant documents’ text for a query."""
    docs = _vectordb.similarity_search(query, k=k)
    return "\n\n".join([d.page_content for d in docs])
