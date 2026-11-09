"""Renderer-agnostic document model for the Macrova project report."""

from dataclasses import dataclass, field
from typing import List, Sequence


@dataclass
class Block:
    kind: str
    text: str = ""
    items: List[str] = field(default_factory=list)
    rows: List[Sequence[str]] = field(default_factory=list)
    header: Sequence[str] = field(default_factory=list)
    caption: str = ""
    path: str = ""
    width: float = 0.0
    key: str = ""
    meta: dict = field(default_factory=dict)


class Doc:
    """Ordered list of blocks plus the contents, figure and table registers."""

    def __init__(self):
        self.blocks: List[Block] = []
        self.toc = []          # (level, label, key)
        self.figures = []      # (label, caption, key)
        self.tables = []       # (label, caption, key)
        self.chapter = 0
        self.chapter_title = ""
        self.prefix = "0"
        self._fig = {}
        self._tab = {}
        self._seq = {}

    # ------------------------------------------------------------- headings
    def chapter_heading(self, number, title, key=None):
        key = key or f"ch{number}"
        self.blocks.append(Block("chapter", text=title, key=key, meta={"number": number}))
        self.toc.append((0, f"CHAPTER {number}: {title.upper()}", key))
        self.chapter = number
        self.chapter_title = title.upper()
        self.prefix = str(number)
        return key

    def prefix_numbering(self, label):
        """Start a fresh figure and table sequence under a non-numeric label (e.g. A)."""
        self.prefix = label

    def part_heading(self, title, key=None):
        key = key or title.lower().replace(" ", "-")
        self.blocks.append(Block("part", text=title, key=key))
        self.toc.append((0, title.upper(), key))
        return key

    def h2(self, number, title, key=None):
        key = key or f"s{number}"
        self.blocks.append(Block("h2", text=f"{number}  {title}", key=key))
        self.toc.append((1, f"{number} {title}", key))
        return key

    def h3(self, number, title, key=None):
        key = key or f"s{number}"
        self.blocks.append(Block("h3", text=f"{number}  {title}", key=key))
        self.toc.append((2, f"{number} {title}", key))
        return key

    # ------------------------------------------------------------------ text
    def p(self, text=""):
        self.blocks.append(Block("p", text=text))

    def bullets(self, items):
        self.blocks.append(Block("bullets", items=list(items)))

    def numbered(self, items):
        self.blocks.append(Block("numbered", items=list(items)))

    def note(self, text):
        self.blocks.append(Block("note", text=text))

    def code(self, caption, text):
        self.blocks.append(Block("code", text=text, caption=caption))

    def pagebreak(self):
        self.blocks.append(Block("pagebreak"))

    def spacer(self, height=10):
        self.blocks.append(Block("spacer", meta={"h": height}))

    # ---------------------------------------------------------------- tables
    def table(self, caption, header, rows, widths=None, font_size=8.6):
        n = self._seq.get(("tab", self.prefix), 0) + 1
        self._seq[("tab", self.prefix)] = n
        label = f"{self.prefix}.{n}"
        self.blocks.append(Block("table", caption=caption, header=list(header),
                                 rows=[list(r) for r in rows],
                                 meta={"widths": widths, "font": font_size, "label": label}))
        self.tables.append((label, caption, f"tab{label}"))
        return label

    # --------------------------------------------------------------- figures
    def figure(self, path, caption, width=6.1):
        n = self._seq.get(("fig", self.prefix), 0) + 1
        self._seq[("fig", self.prefix)] = n
        label = f"{self.prefix}.{n}"
        self.blocks.append(Block("figure", path=path, caption=caption, width=width,
                                 meta={"label": label}))
        self.figures.append((label, caption, f"fig{label}"))
        return label
