from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .vector_store import store, persist
from .settings import settings

splitter = RecursiveCharacterTextSplitter(chunk_size=settings.chunk_size,
                                          chunk_overlap=settings.chunk_overlap)

def ingest(folder: str = "docs"):
    pdf_paths = Path(folder).glob("*.pdf")
    for pdf in pdf_paths:
        pages = PyPDFLoader(str(pdf)).load()
        chunks = splitter.split_documents(pages)
        store.add_documents(chunks)
        print(f"✓ indexed {pdf.name} ({len(chunks)} chunks)")
    persist()

if __name__ == "__main__":
    ingest()