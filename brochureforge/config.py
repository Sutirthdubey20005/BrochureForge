"""
Configuration constants and defaults for BrochureForge.
"""

import os

# ---------------------------------------------------------------------------
# Ollama / LLM settings
# ---------------------------------------------------------------------------
OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY", "ollama")  # placeholder
DEFAULT_MODEL: str = os.getenv("BROCHURE_MODEL", "qwen3:1.7b")

# ---------------------------------------------------------------------------
# Scraping settings
# ---------------------------------------------------------------------------
REQUEST_TIMEOUT: int = 15  # seconds
MAX_CONTENT_LENGTH: int = 2500  # chars per page before truncation
MAX_AGGREGATED_LENGTH: int = 10000  # total chars sent to the LLM
USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)
REQUEST_HEADERS: dict = {"User-Agent": USER_AGENT}

# ---------------------------------------------------------------------------
# Tone presets — each maps to a system-prompt description
# ---------------------------------------------------------------------------
TONE_PRESETS: dict[str, str] = {
    "professional": (
        "You are a corporate communications expert. Create a polished, "
        "professional company brochure for prospective customers, investors, "
        "and recruits in clean markdown. Do NOT wrap the output in code fences."
    ),
    "humorous": (
        "You are a witty, highly entertaining copywriter. Create a humorous, "
        "engaging company brochure that is fun to read, in clean markdown. "
        "Do NOT wrap the output in code fences."
    ),
    "investor": (
        "You are a venture-capital analyst. Create an analytical, "
        "growth-focused company brochure emphasizing business model, market "
        "opportunity, and culture in clean markdown. "
        "Do NOT wrap the output in code fences."
    ),
}

# ---------------------------------------------------------------------------
# PDF styling
# ---------------------------------------------------------------------------
PDF_CSS: str = """
    body {
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        line-height: 1.7;
        color: #2c3e50;
        margin: 50px 60px;
        font-size: 14px;
    }
    h1 {
        color: #1a252f;
        border-bottom: 3px solid #3498db;
        padding-bottom: 12px;
        margin-top: 30px;
    }
    h2 {
        color: #2c3e50;
        border-bottom: 1px solid #bdc3c7;
        padding-bottom: 6px;
        margin-top: 24px;
    }
    h3 { color: #34495e; margin-top: 18px; }
    p  { margin-bottom: 14px; }
    ul, ol { margin-bottom: 14px; padding-left: 28px; }
    li { margin-bottom: 4px; }
    strong { color: #1a252f; }
    a { color: #2980b9; text-decoration: none; }
    blockquote {
        border-left: 4px solid #3498db;
        margin: 16px 0;
        padding: 10px 20px;
        background: #f7f9fb;
        color: #555;
    }
"""
