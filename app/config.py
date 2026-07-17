import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./docflow.db")
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")

    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", "tesseract")
    TIKA_SERVER_JAR: str = os.getenv("TIKA_SERVER_JAR", "")

    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.1")

    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))


settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CHROMA_DIR, exist_ok=True)
