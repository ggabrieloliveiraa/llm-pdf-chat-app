from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from pathlib import Path
from .settings import settings
import faiss

INDEX_PATH = Path("store.faiss")

_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",  # campo exigido nas versões ≥ 0.1.3
    google_api_key=settings.google_api_key,
)

def _create_empty() -> FAISS:
    """Create an empty FAISS index with the correct vector dimension."""
    # One quick call to grab the embedding dimension (costs a single token)
    dim = len(_embeddings.embed_query("dimension probe"))
    index = faiss.IndexFlatL2(dim)  # Flat (exact) index
    return FAISS(embedding_function=_embeddings,
                 index=index,
                 docstore=InMemoryDocstore({}),
                 index_to_docstore_id={})


def load_or_create(index_path: Path = INDEX_PATH):
    if index_path.exists():
        return FAISS.load_local(index_path, _embeddings, allow_dangerous_deserialization=True)
    return _create_empty()

store = load_or_create()


def persist():
    store.save_local(INDEX_PATH)