<p align="center">
  <h1 align="center">🛠️ BrochureForge</h1>
  <p align="center">
    <strong>AI-Powered Company Brochure Generator — 100% Local & Private</strong>
  </p>
  <p align="center">
    Crawl any company website • Let a local LLM pick the best pages • Generate a polished marketing brochure • Export to PDF
  </p>
  <p align="center">
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-features">Features</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-license">License</a>
  </p>
</p>

---

## 📖 Overview

**BrochureForge** is a fully local, agentic AI pipeline that turns any company website into a professional marketing brochure — no API keys, no cloud costs, no data leaving your machine.

It works in four intelligent stages:

1. **🕷️ Scrape** — Crawls the target website and discovers all links.
2. **🤖 Filter** — A local LLM (Qwen via Ollama) analyses the links and selects the most relevant ones (About, Careers, Pricing, Products…).
3. **📦 Aggregate** — Fetches and cleans text from the landing page + selected sub-pages.
4. **✍️ Generate** — The LLM produces a structured Markdown brochure in your chosen tone.
5. **📕 Export** *(optional)* — Converts the Markdown to a beautifully styled PDF.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **🏠 Fully Local** | Runs entirely on your machine via [Ollama](https://ollama.com) — zero cloud dependency |
| **🤖 Agentic Link Selection** | The LLM intelligently decides which pages matter for a brochure |
| **🎨 Custom Tone** | Choose `professional`, `humorous`, or `investor` tone via CLI flag |
| **📕 PDF Export** | One-click PDF generation with professional styling via WeasyPrint |
| **💾 Markdown Save** | Optionally save the raw `.md` file alongside the PDF |
| **⚙️ Configurable** | Swap models, tweak prompts, adjust scraping limits — all from `config.py` or env vars |
| **🛡️ Robust** | Graceful error handling for network failures, malformed JSON, and LLM quirks |

---

## 🏗️ Architecture

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│  CLI / User  │────▶│   Scraper     │────▶│    Agent     │────▶│  Generator   │────▶│   PDF    │
│  (main.py)   │     │ (scraper.py)  │     │  (agent.py)  │     │(generator.py)│     │(pdf_exp.)│
│              │     │               │     │              │     │              │     │          │
│ --company    │     │ fetch_links() │     │ select_      │     │ generate_    │     │ save_as  │
│ --url        │     │ fetch_page_   │     │ relevant_    │     │ brochure()   │     │ _pdf()   │
│ --tone       │     │ text()        │     │ links()      │     │              │     │          │
│ --pdf        │     │               │     │ aggregate_   │     │              │     │          │
│              │     │               │     │ company_     │     │              │     │          │
│              │     │               │     │ content()    │     │              │     │          │
└──────────────┘     └───────────────┘     └──────┬───────┘     └──────────────┘     └──────────┘
                                                  │
                                           ┌──────▼───────┐
                                           │   Ollama     │
                                           │  (local LLM) │
                                           │  Qwen 3 1.7B │
                                           └──────────────┘
```

---

## 📂 Project Structure

```
BrochureForge/
├── main.py                     # CLI entry-point
├── brochureforge/
│   ├── __init__.py             # Package metadata & version
│   ├── config.py               # All constants, defaults, and styling
│   ├── scraper.py              # Web scraping (links + page text)
│   ├── agent.py                # LLM-powered link selection & aggregation
│   ├── generator.py            # Brochure generation via LLM
│   └── pdf_export.py           # Markdown → HTML → PDF conversion
├── requirements.txt            # Python dependencies
├── .gitignore
├── LICENSE                     # MIT
└── README.md                   # You are here
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| **Python 3.10+** | Runtime | [python.org](https://www.python.org/downloads/) |
| **Ollama** | Local LLM server | [ollama.com/download](https://ollama.com/download) |
| **GTK3** *(PDF only)* | WeasyPrint system dep | See [WeasyPrint docs](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html) |

### 1 — Install Ollama & Pull the Model

```bash
# Install Ollama (follow instructions at https://ollama.com/download)

# Pull the default Qwen model
ollama pull qwen3:1.7b

# Verify it's running
ollama list
```

### 2 — Clone & Install Dependencies

```bash
git clone https://github.com/YOUR_USERNAME/BrochureForge.git
cd BrochureForge

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.venv\Scripts\activate           # Windows

# Install Python packages
pip install -r requirements.txt
```

### 3 — Run It!

```bash
python main.py --company "HuggingFace" --url "https://huggingface.co"
```

---

## 📋 Usage

### Basic — Generate a Professional Brochure

```bash
python main.py --company "Stripe" --url "https://stripe.com"
```

### With Tone Selection

```bash
python main.py --company "Notion" --url "https://notion.so" --tone humorous
```

### Export as PDF

```bash
python main.py --company "GitHub" --url "https://github.com" --pdf
```

### Save Markdown + PDF to a Specific Directory

```bash
python main.py \
  --company "Tesla" \
  --url "https://tesla.com" \
  --tone investor \
  --pdf \
  --save-md \
  --output-dir ./output
```

### Use a Different Ollama Model

```bash
python main.py \
  --company "OpenAI" \
  --url "https://openai.com" \
  --model qwen3:4b
```

### Full Help

```bash
python main.py --help
```

```
usage: brochureforge [-h] --company COMPANY --url URL
                     [--tone {humorous,investor,professional}]
                     [--model MODEL] [--pdf] [--output-dir OUTPUT_DIR]
                     [--save-md]

🛠️  BrochureForge — Generate AI-powered company brochures from any
website using a local Ollama model.

options:
  -h, --help            show this help message and exit
  --company COMPANY     Name of the target company
  --url URL             Primary website URL
  --tone {humorous,investor,professional}
                        Tone / style of the brochure (default: professional)
  --model MODEL         Ollama model tag to use (default: qwen3:1.7b)
  --pdf                 Export the brochure as a styled PDF file
  --output-dir DIR      Directory to save outputs (default: .)
  --save-md             Also save the raw Markdown brochure to a .md file

Examples:
  python main.py --company "HuggingFace" --url https://huggingface.co
  python main.py --company "Stripe" --url https://stripe.com --tone investor --pdf
  python main.py --company "Notion" --url https://notion.so --tone humorous --model qwen3:4b
```

---

## ⚙️ Configuration

All defaults live in [`brochureforge/config.py`](brochureforge/config.py) and can be overridden with environment variables:

| Env Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1` | Ollama API endpoint |
| `OLLAMA_API_KEY` | `ollama` | API key (placeholder for Ollama) |
| `BROCHURE_MODEL` | `qwen3:1.7b` | Default model tag |

---

## 🧰 Tech Stack

| Component | Library / Tool |
|-----------|----------------|
| **LLM Serving** | [Ollama](https://ollama.com) |
| **LLM Model** | [Qwen 3 1.7B](https://ollama.com/library/qwen3:1.7b) (swappable) |
| **LLM Client** | [openai](https://pypi.org/project/openai/) (OpenAI-compatible) |
| **Web Scraping** | [requests](https://pypi.org/project/requests/) + [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) |
| **Markdown → HTML** | [markdown](https://pypi.org/project/Markdown/) |
| **HTML → PDF** | [WeasyPrint](https://pypi.org/project/weasyprint/) |
| **CLI** | [argparse](https://docs.python.org/3/library/argparse.html) (stdlib) |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ and local LLMs
</p>
