from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

class Settings(BaseModel):
    github_base_url: str = os.getenv("GITHUB_BASE_URL", "https://github.com").rstrip("/")
    github_client_id: str = os.getenv("GITHUB_CLIENT_ID", "")
    github_client_secret: str = os.getenv("GITHUB_CLIENT_SECRET", "")
    github_redirect_uri: str = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/callback").rstrip("/")
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    bitbucket_client_id: str = os.getenv("BITBUCKET_CLIENT_ID", "")
    bitbucket_client_secret: str = os.getenv("BITBUCKET_CLIENT_SECRET", "")
    bitbucket_redirect_uri: str = os.getenv("BITBUCKET_REDIRECT_URI", "http://localhost:8000/auth/bitbucket/callback").rstrip("/")
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3003").rstrip("/")
    allow_pat_fallback: bool = os.getenv("ALLOW_PAT_FALLBACK", "true").lower() == "true"
    session_secret: str = os.getenv("SESSION_SECRET", "change-me")

    azure_openai_api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

settings = Settings()
