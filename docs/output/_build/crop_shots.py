"""Trim the browser chrome and the empty canvas margins from the raw screenshots."""

import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
OUT = os.path.join(ASSETS, "shots")
PAGE_TOP = 91      # first row below the browser chrome
PAD_X = 26
PAD_Y = 16


def content_top(grey):
    """First row after the white application header that follows the browser chrome."""
    white = (grey > 254).mean(axis=1)
    y = PAGE_TOP
    while y < grey.shape[0] and white[y] > 0.90:
        y += 1
    return y


def crop(path):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    grey = a[:, : w - 26].mean(axis=2)

    top = content_top(grey)
    canvas = a[top + 2, : w - 26]
    modal = (canvas // 4 * 4)
    values, counts = np.unique(modal, axis=0, return_counts=True)
    bg = values[counts.argmax()]

    body = a[top:, : w - 26]
    mask = np.abs(body - bg).max(axis=2) > 6
    cols = mask.sum(axis=0)
    rows = mask.sum(axis=1)
    keep_x = np.where(cols > 4)[0]
    keep_y = np.where(rows > 4)[0]
    if keep_x.size == 0 or keep_y.size == 0:
        return im

    x0 = max(0, int(keep_x.min()) - PAD_X)
    x1 = min(w - 26, int(keep_x.max()) + PAD_X)
    y0 = max(0, top - 4)
    y1 = min(h, top + int(keep_y.max()) + PAD_Y)
    return im.crop((x0, y0, x1, y1))


def main():
    os.makedirs(OUT, exist_ok=True)
    files = [n for n in os.listdir(ASSETS) if n[0].isdigit() and n.endswith(".png")]
    files.sort(key=lambda n: int(n.split("-")[0]))
    for name in files:
        n = int(name.split("-")[0])
        im = crop(os.path.join(ASSETS, name))
        im.save(os.path.join(OUT, f"shot-{n}.png"))
        print(f"{name:44s} -> shot-{n}.png  {im.size}")


if __name__ == "__main__":
    sys.exit(main())
