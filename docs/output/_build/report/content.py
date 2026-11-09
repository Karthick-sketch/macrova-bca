"""Aggregate entry point plus a cross-reference audit."""

import re

from doc import Block
import content_a
import content_b
import content_c

FIG = r"Figure[s]?\s+"
TAB = r"Table[s]?\s+"

TAB_LEADS = [
    "The complete set of values is given in Table {n}.",
    "The same information is presented in tabular form in Table {n}.",
    "The details are set out in Table {n}.",
    "The corresponding data appear in Table {n}.",
]

SHOT_LEADS = [
    "The screen is reproduced in Figure {n}.",
    "The complete view is captured in Figure {n}.",
    "The rendered screen appears in Figure {n}.",
]

FIG_LEADS = [
    "The model is presented in Figure {n}.",
    "The arrangement described above is shown in Figure {n}.",
    "The structure is drawn in Figure {n}.",
]


def _text(doc):
    chunks = []
    for b in doc.blocks:
        if b.kind in ("p", "bullets", "numbered", "note"):
            chunks.append(b.text)
            chunks.extend(b.items)
        elif b.kind in ("table", "code"):
            chunks.append(b.caption)
    return " ".join(chunks)


def _is_referenced(text, label, word):
    for m in re.finditer(re.escape(word) + r"\s*" + re.escape(label) + r"(?![0-9])", text):
        return True
    return False


def add_cross_references(doc):
    """Insert a one-sentence lead-in before any figure or table the prose never cites."""
    text = _text(doc)
    inserts = []
    for i, b in enumerate(doc.blocks):
        if b.kind not in ("figure", "table"):
            continue
        label = b.meta.get("label")
        if not label:
            continue
        word = "Figure" if b.kind == "figure" else "Table"
        if _is_referenced(text, label, word):
            continue
        if b.kind == "figure":
            leads = SHOT_LEADS if b.path.startswith("shots/") else FIG_LEADS
        else:
            leads = TAB_LEADS
        # attach to the closest preceding paragraph so the lead reads as part of the prose
        for j in range(i - 1, -1, -1):
            if doc.blocks[j].kind == "p" and doc.blocks[j].text:
                inserts.append((j, leads[len(inserts) % len(leads)].format(n=label)))
                break
    used = set()
    for j, sentence in inserts:
        if j in used:            # never stack two lead-ins on one paragraph
            continue
        used.add(j)
        doc.blocks[j].text = doc.blocks[j].text.rstrip() + " " + sentence
    return doc


def check_references(doc):
    text = _text(doc)
    figures = {label for label, _, _ in doc.figures}
    tables = {label for label, _, _ in doc.tables}
    bad_fig = sorted({m for m in re.findall(FIG + r"(\d+\.\d+)", text)} - figures)
    bad_tab = sorted({m for m in re.findall(TAB + r"(\d+\.\d+)", text)} - tables)
    unreferenced_fig = sorted(f for f in figures if not _is_referenced(text, f, "Figure"))
    unreferenced_tab = sorted(t for t in tables if not _is_referenced(text, t, "Table"))
    return {
        "dangling_figure_refs": bad_fig,
        "dangling_table_refs": bad_tab,
        "unreferenced_figures": unreferenced_fig,
        "unreferenced_tables": unreferenced_tab,
    }


def build_all(doc):
    content_a.build(doc)
    content_b.build(doc)
    content_c.build(doc)
    add_cross_references(doc)
    return doc
