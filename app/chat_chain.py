from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from .vector_store import store
from .settings import settings

llm = ChatGoogleGenerativeAI(
    model=settings.model_name,
    google_api_key=settings.google_api_key,
    temperature=0,
)

def make_chain():
    return ConversationalRetrievalChain.from_llm(llm, store.as_retriever())
