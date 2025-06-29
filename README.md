# Pré-requisitos
Python 3.11

Git

# 1. clone o repositório
git clone https://github.com/seu-user/llm-pdf-chat-app.git
cd llm-pdf-chat-app

# 2. crie ambiente virtual
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. instale dependências
pip install -r requirements.txt

# 4. configure variáveis de ambiente
cp .env.example .env
# edite .env e coloque GOOGLE_API_KEY=ai-...

# 5. (opcional) coloque PDFs em docs/ e gere o índice
mkdir -p docs && cp /caminho/arquivo.pdf docs/
python app/ingest.py docs

# 6. inicie a UI Streamlit (porta 8501)
streamlit run streamlit_app.py
# → abra http://localhost:8501 no navegador

FastAPI: quer expor também o endpoint REST?
Em outro terminal:
uvicorn app.main:app --reload  # porta 8000
