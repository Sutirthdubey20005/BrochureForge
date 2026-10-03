"""
PDF export for BrochureForge.

Converts a Markdown brochure string into a professionally styled PDF
using the ``markdown`` library (Markdown → HTML) and ``weasyprint``
(HTML → PDF).
"""

from __future__ import annotations

import re
from pathlib import Path

import markdown
from weasyprint import HTML

from brochureforge.config import PDF_CSS


def _sanitize_filename(name: str) -> str:
    """Convert *name* into a safe, lowercase, underscore-separated filename."""
    name = name.strip().lower()
    name = re.sub(r"[^\w\s-]", "", name)
    return re.sub(r"[\s-]+", "_", name)


def save_as_pdf(
    company_name: str,
    markdown_content: str,
    output_dir: str | Path = ".",
) -> Path:
    """Render *markdown_content* as a styled PDF and write it to disk.

    Parameters
    ----------
    company_name:
        Used for both the document ``<title>`` and the output filename.
    markdown_content:
        The brochure text in Markdown.
    output_dir:
        Directory to save the PDF into (defaults to the current directory).

    Returns
    -------
    pathlib.Path
        Absolute path of the generated PDF file.
    """
    html_body = markdown.markdown(
        markdown_content,
        extensions=["tables", "fenced_code", "smarty"],
    )

    html_doc = f"""\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{company_name} — Company Brochure</title>
    <style>{PDF_CSS}</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    safe_name = _sanitize_filename(company_name)
    out_path = Path(output_dir).resolve() / f"{safe_name}_brochure.pdf"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    HTML(string=html_doc).write_pdf(str(out_path))
    return out_path
