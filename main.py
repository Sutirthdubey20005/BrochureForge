#!/usr/bin/env python3
"""
BrochureForge — CLI entry-point.

Run ``python main.py --help`` for usage information.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from openai import OpenAI

from brochureforge.config import DEFAULT_MODEL, OLLAMA_API_KEY, OLLAMA_BASE_URL, TONE_PRESETS
from brochureforge.generator import generate_brochure
from brochureforge.pdf_export import save_as_pdf


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="brochureforge",
        description=(
            "🛠️  BrochureForge — Generate AI-powered company brochures "
            "from any website using a local Ollama model."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            '  python main.py --company "HuggingFace" --url https://huggingface.co\n'
            '  python main.py --company "Stripe" --url https://stripe.com --tone investor --pdf\n'
            '  python main.py --company "Notion" --url https://notion.so --tone humorous --model qwen3:4b\n'
        ),
    )

    parser.add_argument(
        "--company",
        type=str,
        required=True,
        help="Name of the target company (e.g. 'HuggingFace').",
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="Primary website URL (e.g. https://huggingface.co).",
    )
    parser.add_argument(
        "--tone",
        type=str,
        default="professional",
        choices=sorted(TONE_PRESETS.keys()),
        help="Tone / style of the brochure (default: professional).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Ollama model tag to use (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Export the brochure as a styled PDF file.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save outputs (default: current directory).",
    )
    parser.add_argument(
        "--save-md",
        action="store_true",
        help="Also save the raw Markdown brochure to a .md file.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Parse CLI args, generate the brochure, and optionally export."""
    args = _build_parser().parse_args(argv)

    # ------------------------------------------------------------------
    # Initialise the Ollama-backed OpenAI client
    # ------------------------------------------------------------------
    client = OpenAI(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY)

    print()
    print("=" * 60)
    print(f"  🚀  BrochureForge — generating brochure")
    print(f"       Company : {args.company}")
    print(f"       URL     : {args.url}")
    print(f"       Tone    : {args.tone}")
    print(f"       Model   : {args.model}")
    print("=" * 60)
    print()

    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------
    try:
        brochure_md = generate_brochure(
            company_name=args.company,
            url=args.url,
            tone=args.tone,
            client=client,
            model=args.model,
        )
    except Exception as exc:
        print(f"\n❌  Brochure generation failed: {exc}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------
    print("\n" + "─" * 60)
    print("  📄  GENERATED BROCHURE")
    print("─" * 60 + "\n")
    print(brochure_md)
    print("\n" + "─" * 60 + "\n")

    out_dir = Path(args.output_dir).resolve()

    # ------------------------------------------------------------------
    # Optional: save Markdown
    # ------------------------------------------------------------------
    if args.save_md:
        import re

        safe = re.sub(r"[^\w\s-]", "", args.company.lower())
        safe = re.sub(r"[\s-]+", "_", safe)
        md_path = out_dir / f"{safe}_brochure.md"
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(brochure_md, encoding="utf-8")
        print(f"  💾  Markdown saved → {md_path}")

    # ------------------------------------------------------------------
    # Optional: export PDF
    # ------------------------------------------------------------------
    if args.pdf:
        try:
            pdf_path = save_as_pdf(args.company, brochure_md, output_dir=out_dir)
            print(f"  📕  PDF exported  → {pdf_path}")
        except Exception as exc:
            print(f"\n⚠️  PDF export failed: {exc}")
            print("     Make sure WeasyPrint and its system dependencies are installed.")
            print("     See: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html")

    print("\n✅  Done!\n")


if __name__ == "__main__":
    main()
