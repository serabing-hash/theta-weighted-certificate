#!/usr/bin/env python3
"""Build and inspect the paper, without evaluating its mathematics.

The sole authoring input is theta_source_escape.tex.  Compilation takes place
in a temporary directory with no research files or external bibliography.
Requires pdflatex, Python 3, PyMuPDF (fitz), and Pillow.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone

import fitz
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent
STEM = "theta_source_escape"
SOURCE = ROOT / f"{STEM}.tex"
CHECKS = ROOT / "checks"
RENDERED = ROOT / "rendered"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    CHECKS.mkdir(exist_ok=True)
    RENDERED.mkdir(exist_ok=True)
    tex = SOURCE.read_text(encoding="utf-8")
    env = os.environ.copy()
    env["TZ"] = "UTC"
    env["SOURCE_DATE_EPOCH"] = "1792195200"  # 2026-10-17 00:00:00 UTC
    env["FORCE_SOURCE_DATE"] = "1"
    with tempfile.TemporaryDirectory(prefix="theta-paper-build-") as temp:
        build = Path(temp)
        shutil.copy2(SOURCE, build / SOURCE.name)
        command = [
            "pdflatex", "-interaction=nonstopmode", "-halt-on-error",
            "-no-shell-escape", "-file-line-error", SOURCE.name,
        ]
        for iteration in range(1, 4):
            result = subprocess.run(
                command, cwd=build, env=env, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
            )
            (CHECKS / f"build-pass-{iteration}.txt").write_text(
                result.stdout, encoding="utf-8"
            )
            if result.returncode:
                raise SystemExit(
                    f"pdflatex pass {iteration} failed; see checks/build-pass-{iteration}.txt"
                )
        shutil.copy2(build / f"{STEM}.pdf", ROOT / f"{STEM}.pdf")
        shutil.copy2(build / f"{STEM}.log", CHECKS / "latex-final.log")

    log = (CHECKS / "latex-final.log").read_text(encoding="utf-8", errors="replace")
    problems = {
        "overfull_boxes": re.findall(r"Overfull [^\n]*", log),
        "undefined_references_or_citations": re.findall(
            r"[^\n]*(?:undefined|Rerun to get|Label\(s\) may have changed)[^\n]*", log
        ),
        "multiply_defined_labels": re.findall(r"[^\n]*multiply defined[^\n]*", log),
    }
    pdf = ROOT / f"{STEM}.pdf"
    document = fitz.open(pdf)
    text_parts = []
    outside_page = []
    page_images = []
    for number, page in enumerate(document, 1):
        text_parts.append(f"\n--- Page {number} ---\n" + page.get_text(sort=True))
        for block in page.get_text("dict")["blocks"]:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    rectangle = fitz.Rect(span["bbox"])
                    if not (page.rect + (-1, -1, 1, 1)).contains(rectangle):
                        outside_page.append({
                            "page": number, "text": span["text"],
                            "bbox": list(rectangle),
                        })
        target = RENDERED / f"page-{number:02d}.png"
        page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(target)
        page_images.append(target)
    pdf_text = "".join(text_parts)
    (CHECKS / "pdf-text.txt").write_text(pdf_text, encoding="utf-8")

    # These sheets supplement, rather than replace, page-by-page visual review.
    for offset in range(0, len(page_images), 4):
        sheet = Image.new("RGB", (1240, 1840), "#d7dce2")
        draw = ImageDraw.Draw(sheet)
        for local, path in enumerate(page_images[offset:offset + 4]):
            with Image.open(path) as opened:
                thumbnail = opened.copy()
            thumbnail.thumbnail((590, 860), Image.Resampling.LANCZOS)
            column, row = local % 2, local // 2
            left = column * 620 + (620 - thumbnail.width) // 2
            top = row * 920 + 35
            sheet.paste(thumbnail, (left, top))
            draw.text((column * 620 + 20, row * 920 + 12),
                      f"Page {offset + local + 1}", fill="black")
        sheet.save(RENDERED / f"contact-{offset // 4 + 1:02d}.png")

    bibliography = re.findall(r"\\bibitem\{([^}]+)\}", tex)
    cites = set()
    for group in re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", tex):
        cites.update(part.strip() for part in group.split(","))
    identifiers = {
        "email_identifiers": re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", tex + pdf_text),
        "orcid_identifiers": re.findall(r"\b\d{4}-\d{4}-\d{4}-\d{3}[0-9X]\b", tex + pdf_text),
    }
    author_contact = {"email": "24ping@naver.com", "orcid": "0009-0008-7448-514X"}
    unexpected_identifiers = {
        "email": sorted(set(identifiers["email_identifiers"]) - {author_contact["email"]}),
        "orcid": sorted(set(identifiers["orcid_identifiers"]) - {author_contact["orcid"]}),
    }
    author_fields_present = all(value in tex and value in pdf_text for value in author_contact.values())
    artifact_match = re.search(
        r"https://github\.com/serabing-hash/theta-weighted-certificate/commit/[0-9a-f]{40}", tex
    )
    artifact_url = artifact_match.group(0) if artifact_match else None
    artifact_link_in_pdf = bool(artifact_url) and any(
        link.get("uri") == artifact_url for page in document for link in page.get_links()
    )
    report = {
        "scope": "Document build and structural checks only; not an analytic proof verifier.",
        "built_from_single_tex_in_isolated_directory": True,
        "latex_passes": 3,
        "shell_escape": False,
        "page_count": len(document),
        "pages_rendered": len(page_images),
        "render_scale": 1.5,
        "pdf_metadata": document.metadata,
        **problems,
        "text_spans_outside_page": outside_page,
        "inline_bibliography_keys": bibliography,
        "citations_missing_from_bibliography": sorted(cites - set(bibliography)),
        "external_authoring_inputs": re.findall(r"\\(?:input|include|bibliography)\s*\{[^}]+\}", tex),
        **identifiers,
        "expected_author_contact": author_contact,
        "unexpected_contact_identifiers": unexpected_identifiers,
        "expected_author_contact_fields_present": author_fields_present,
        "artifact_commit_url": artifact_url,
        "artifact_link_present_in_pdf": artifact_link_in_pdf,
        "numerical_theta_or_zero_evaluations_this_build": 0,
        "research_calculations_rerun_this_build": False,
        "remote_publication_verified_by_this_build": False,
        "RH_PROOF": "NOT-OBTAINED",
    }
    (CHECKS / "document-validation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    receipt = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": SOURCE.name, "source_sha256": digest(SOURCE),
        "pdf": pdf.name, "pdf_sha256": digest(pdf),
        "page_count": len(document),
        "engine": subprocess.run(["pdflatex", "--version"], text=True,
                                 stdout=subprocess.PIPE, check=True).stdout.splitlines()[0],
        "contact_fields": author_contact,
        "public_github_url": artifact_url,
        "RH_PROOF": "NOT-OBTAINED",
    }
    (CHECKS / "build-receipt.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    failures = any(problems.values()) or outside_page or any(unexpected_identifiers.values())
    failures = failures or not author_fields_present or not artifact_link_in_pdf
    failures = failures or report["citations_missing_from_bibliography"] or report["external_authoring_inputs"]
    print(json.dumps({"page_count": len(document), "structural_checks_passed": not bool(failures),
                      "visual_review": "REQUIRED_SEPARATELY", "report": str(CHECKS / "document-validation.json")}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
