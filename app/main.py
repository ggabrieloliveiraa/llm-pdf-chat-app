from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from .ingest import ingest 
from .chat_chain import make_chain
from fastapi.staticfiles import StaticFiles
from typing import List, Tuple
from pydantic import BaseModel

app = FastAPI(title="LLM PDF Chat Assistant")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

chain = make_chain()

class ChatBody(BaseModel):
    question: str
    history: list | None = None   # recebe qualquer lista bruta

@app.post("/chat")
async def chat(payload: ChatBody):
    # converte para List[Tuple[str, str]]
    hist: List[Tuple[str, str]] = []
    if payload.history:
        # aceita 2 formatos:
        #   1) [["user1","bot1"], ["user2","bot2"]]
        #   2) [{"user":"…","assistant":"…"}, …]
        for item in payload.history:
            if isinstance(item, (list, tuple)) and len(item) == 2:
                hist.append(tuple(item))                      # formato 1
            elif isinstance(item, dict):
                hist.append((item.get("user", ""),            # formato 2
                             item.get("assistant", "")))

    answer = chain({"question": payload.question,
                    "chat_history": hist})["answer"]
    return {"answer": answer}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, detail="PDFs only")
    dest = Path("docs") / file.filename
    dest.write_bytes(await file.read())
    ingest("docs")
    return {"status": "indexed", "file": file.filename}

@app.get("/", response_class=HTMLResponse)
async def index():
    return Path("static/index.html").read_text()

app.mount("/", StaticFiles(directory="static", html=True), name="static")
