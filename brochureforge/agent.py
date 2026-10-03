"""
AI agent logic for BrochureForge.

Uses a local Ollama-served model (OpenAI-compatible API) to:
  1. Analyse scraped links and select the most relevant ones.
  2. Aggregate page contents for downstream brochure generation.
"""

from __future__ import annotations

import json
from urllib.parse import urljoin

from openai import OpenAI

from brochureforge.config import MAX_AGGREGATED_LENGTH
from brochureforge.scraper import fetch_links, fetch_page_text

# ---------------------------------------------------------------------------
# System prompt for the link-selection step
# ---------------------------------------------------------------------------
LINK_SELECTION_SYSTEM_PROMPT: str = """\
You are provided with a list of links found on a webpage.
Decide which links are most relevant to include in a company brochure,
such as About pages, Company pages, Careers/Jobs, Pricing, or Products.

Respond **strictly** in JSON — no commentary, no code fences:
{
    "links": [
        {"type": "about page", "url": "https://full.url/about"},
        {"type": "careers page", "url": "https://full.url/careers"}
    ]
}

Exclude Terms of Service, Privacy policies, email/mailto links, and
social-media share buttons.
"""


def _build_links_user_prompt(url: str) -> str:
    """Build the user message listing all discovered links."""
    links = fetch_links(url)
    if not links:
        return f"No links were found on {url}."
    header = f"Here is the list of links found on {url}:\n\n"
    return header + "\n".join(links)


def select_relevant_links(
    url: str,
    client: OpenAI,
    model: str,
) -> list[dict[str, str]]:
    """Ask the local LLM to pick the most brochure-relevant links.

    Parameters
    ----------
    url:
        Landing page whose links were scraped.
    client:
        An :class:`openai.OpenAI` instance pointed at the Ollama server.
    model:
        Model tag to use (e.g. ``qwen3:1.7b``).

    Returns
    -------
    list[dict]
        Each dict has ``"type"`` and ``"url"`` keys.
    """
    print(f"  🔗 Analysing links on {url} via {model} …")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": LINK_SELECTION_SYSTEM_PROMPT},
                {"role": "user", "content": _build_links_user_prompt(url)},
            ],
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content or "{}"

        # Attempt to strip markdown code fences if the model wraps them
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[1:])
        if cleaned.endswith("```"):
            cleaned = "\n".join(cleaned.split("\n")[:-1])

        data = json.loads(cleaned)
        return data.get("links", [])
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"  ⚠  Failed to parse link-selection JSON: {exc}")
        return []
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠  LLM link-selection error: {exc}")
        return []


def aggregate_company_content(
    url: str,
    client: OpenAI,
    model: str,
) -> str:
    """Crawl the landing page **and** all LLM-selected sub-pages.

    The resulting text blob is truncated to
    :data:`~brochureforge.config.MAX_AGGREGATED_LENGTH` characters so it
    fits within typical context windows.

    Parameters
    ----------
    url:
        Company landing page.
    client:
        Ollama-backed OpenAI client.
    model:
        Model tag.

    Returns
    -------
    str
        Aggregated, truncated page text suitable for prompting.
    """
    landing_text = fetch_page_text(url)
    relevant = select_relevant_links(url, client, model)

    parts: list[str] = [
        "## Landing Page\n",
        landing_text,
        "\n## Relevant Sub-Pages\n",
    ]

    for link_info in relevant:
        raw_url = link_info.get("url")
        if not raw_url:
            continue
        full_url = urljoin(url, raw_url)
        link_type = link_info.get("type", "unknown")
        parts.append(f"\n### {link_type} — {full_url}\n")
        parts.append(fetch_page_text(full_url))

    aggregated = "".join(parts)
    return aggregated[:MAX_AGGREGATED_LENGTH]
