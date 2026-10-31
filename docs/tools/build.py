#!/usr/bin/env python3
"""Build the Macrova project report.

    python3 build.py [output.pdf]

Three passes are required because the table of contents, the list of figures and
the list of tables change the length of the front matter, which changes the page
labels of everything that follows.

    pass 1  empty entry lists              -> collect heading / figure / table counts
    pass 2  entry lists from pass 1        -> collect exact page labels for that layout
    pass 3  entry lists from pass 2        -> final document (identical layout to pass 2)

Pass 2 and pass 3 have byte-identical front matter lengths because their entry
lists are identical, so the labels collected in pass 2 are correct for pass 3.
"""

from __future__ import annotations

import os
import sys
import tempfile

import theme as T

import content_appendix as APX
import content_ch1 as CH1
import content_ch23 as CH23
import content_ch4 as CH4
import content_ch5 as CH5
import content_ch6 as CH6
import content_ch7 as CH7
import content_ch8 as CH8
import content_front as FRONT


def story(toc_entries, lof_entries, lot_entries):
    T.CTX.reset()
    st = []
    st += FRONT.cover()
    st += FRONT.certificate()
    st += FRONT.declaration()
    st += FRONT.acknowledgement()
    st += FRONT.abstract()
    st += FRONT.toc(toc_entries)
    st += FRONT.lof(lof_entries)
    st += FRONT.lot(lot_entries)
    st += FRONT.abbreviations()
    st += CH1.build()
    st += CH23.chapter2()
    st += CH23.chapter3()
    st += CH4.build()
    st += CH5.build()
    st += CH6.build()
    st += CH7.build()
    st += CH8.build()
    st += CH8.references()
    st += APX.build()
    return st


def render(path, toc_entries, lof_entries, lot_entries):
    T.build_styles()
    doc = T.ReportDoc(path)
    doc.build(story(toc_entries, lof_entries, lot_entries))
    return doc


def toc_from(headings):
    out = []
    for level, text, page in headings:
        if level in (0, 1):
            out.append((0 if level == 0 else 1, text, page))
    return out


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "report", "Macrova_Project_Report.pdf")
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="macrova-report-")

    print("[1/3] measuring headings, figures and tables ...")
    p1 = render(os.path.join(tmp, "pass1.pdf"), [], [], [])
    toc = toc_from(p1.headings)
    lof = [(lab, cap, pg) for lab, cap, pg in p1.figures]
    lot = [(lab, cap, pg) for lab, cap, pg in p1.tables]
    print(f"      {len(toc)} contents entries, {len(lof)} figures, {len(lot)} tables")

    print("[2/3] resolving page labels ...")
    p2 = render(os.path.join(tmp, "pass2.pdf"), toc, lof, lot)
    toc2 = toc_from(p2.headings)
    lof2 = [(lab, cap, pg) for lab, cap, pg in p2.figures]
    lot2 = [(lab, cap, pg) for lab, cap, pg in p2.tables]

    print("[3/3] rendering final document ...")
    p3 = render(out, toc2, lof2, lot2)

    print(f"      pages: {p3.page}")
    print(f"      output: {out}")

    # sanity report -------------------------------------------------------
    if len(toc2) != len(toc):
        print(f"      warning: contents grew from {len(toc)} to {len(toc2)} entries")
    if len(lof2) != len(lof) or len(lot2) != len(lot):
        print("      warning: figure or table count changed between passes")


if __name__ == "__main__":
    main()
