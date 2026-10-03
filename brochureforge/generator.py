"""
Brochure generation and Markdown output for BrochureForge.

Calls the local Ollama model to produce a styled Markdown brochure
from aggregated website content.
"""

from __future__ import annotations

from openai import OpenAI

from brochureforge.agent import aggregate_company_content
from brochureforge.config import TONE_PRESETS


def _resolve_tone(tone: str) -> str:
    """Return the system prompt for *tone*, falling back to 'professional'."""
    key = tone.lower().strip()
    if key not in TONE_PRESETS:
        print(f"  ⚠  Unknown tone '{tone}' — falling back to 'professional'.")
        key = "professional"
    return TONE_PRESETS[key]


def generate_brochure(
    company_name: str,
    url: str,
    tone: str,
    client: OpenAI,
    model: str,
) -> str:
    """Generate a Markdown brochure for *company_name*.

    Pipeline steps:
      1. Scrape & aggregate website content (landing + sub-pages).
      2. Send aggregated content to the local LLM with the chosen tone.
      3. Return the raw Markdown string.

    Parameters
    ----------
    company_name:
        Human-readable company name (used in the prompt).
    url:
        Company website URL.
    tone:
        One of ``professional``, ``humorous``, ``investor``.
    client:
        Ollama-backed OpenAI client.
    model:
        Model tag (e.g. ``qwen3:1.7b``).

    Returns
    -------
    str
        The generated brochure in Markdown format.
    """
    print(f"  📝 Generating {tone} brochure for {company_name} …")

    system_prompt = _resolve_tone(tone)
    website_data = aggregate_company_content(url, client, model)

    user_prompt = (
        f"Please create a company brochure for **{company_name}**.\n\n"
        f"Below is the scraped website data to base the brochure on:\n\n"
        f"{website_data}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or ""

    # Strip code fences if the model accidentally wraps the brochure
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        stripped = "\n".join(lines[1:])
    if stripped.endswith("```"):
        lines = stripped.split("\n")
        stripped = "\n".join(lines[:-1])

    return stripped.strip()
