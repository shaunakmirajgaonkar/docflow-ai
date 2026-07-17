# Run Instructions

## 1. Prerequisites

```bash
# macOS
brew install tesseract poppler openjdk

# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y tesseract-ocr poppler-utils default-jre
```

Install [Ollama](https://ollama.com), then pull a local model:

```bash
ollama pull llama3.2:1b   # fast, good for laptops without a dedicated GPU
# or
ollama pull llama3.1      # larger, more accurate, slower on CPU-only machines
```

## 2. Python environment

```bash
git clone https://github.com/YOUR_USERNAME/docflow-ai.git
cd docflow-ai

python3.12 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configuration

```bash
cp .env.example .env
```

Edit `.env` if needed — in particular, set `OLLAMA_MODEL` to match whichever
model you pulled in step 1.

## 4. Start Ollama (in its own terminal tab, keep it running)

```bash
ollama serve
```

## 5. Start the app

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser to:

- **http://localhost:8000** — the web UI
- **http://localhost:8000/docs** — interactive API docs (Swagger)

## 6. Typical flow

1. Upload a document (PDF, image, DOCX, XLSX) — OCR runs immediately.
2. It's automatically classified, has structured fields extracted, and gets
   indexed for search.
3. Ask questions about it via the Q&A panel (RAG over your local documents).
4. Use semantic search to find relevant passages across all documents.
5. Delete documents you no longer need directly from the UI.

## Troubleshooting

- **Port 8000 already in use** — find and stop the old process:
  ```bash
  lsof -i :8000
  kill -9 <PID>
  ```
- **Processing times out** — switch to a smaller model (`llama3.2:1b`) in
  `.env`, or increase the timeout in `app/services/llm_service.py`.
- **`ModuleNotFoundError`** — make sure your venv is activated
  (`which python` should point inside `venv/bin/python`) before installing
  or running anything.
