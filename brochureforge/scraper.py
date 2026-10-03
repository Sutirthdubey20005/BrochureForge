"""
Web-scraping utilities for BrochureForge.

Provides helpers to:
  • fetch all unique links from a page
  • extract cleaned text content from a page
"""

from __future__ import annotations

from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from brochureforge.config import (
    MAX_CONTENT_LENGTH,
    REQUEST_HEADERS,
    REQUEST_TIMEOUT,
)


def fetch_links(url: str) -> list[str]:
    """Return a deduplicated list of absolute URLs found on *url*.

    Relative ``href`` values are resolved via :func:`urllib.parse.urljoin`.
    Only ``http`` / ``https`` links are kept (``mailto:``, ``javascript:``
    etc. are silently dropped).

    Parameters
    ----------
    url:
        The page to crawl for ``<a>`` tags.

    Returns
    -------
    list[str]
        Unique, fully-qualified URLs.
    """
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"  ⚠  Could not fetch links from {url}: {exc}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    seen: set[str] = set()
    links: list[str] = []

    for anchor in soup.find_all("a", href=True):
        href: str = anchor["href"].strip()
        if not href or href.startswith(("#", "mailto:", "javascript:", "tel:")):
            continue
        full_url = urljoin(url, href)
        # Keep only HTTP(S) links
        if urlparse(full_url).scheme not in ("http", "https"):
            continue
        if full_url not in seen:
            seen.add(full_url)
            links.append(full_url)

    return links


def fetch_page_text(url: str) -> str:
    """Scrape and return cleaned text content from *url*.

    Removes ``<script>``, ``<style>``, ``<nav>``, and ``<footer>`` elements
    before extracting visible text. The result is truncated to
    :data:`~brochureforge.config.MAX_CONTENT_LENGTH` characters.

    Parameters
    ----------
    url:
        The page to scrape.

    Returns
    -------
    str
        A short summary block containing the page title, URL, and body text.
    """
    try:
        response = requests.get(url, headers=REQUEST_HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        return f"\n[Could not fetch contents for {url}: {exc}]\n"

    soup = BeautifulSoup(response.text, "html.parser")

    # Strip non-content elements
    for tag in soup(["script", "style", "nav", "footer", "noscript", "svg"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
    text = soup.get_text(separator=" ", strip=True)

    return (
        f"\n--- Page Title: {title} ---\n"
        f"URL: {url}\n"
        f"Content: {text[:MAX_CONTENT_LENGTH]}\n"
    )
