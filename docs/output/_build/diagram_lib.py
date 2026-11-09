"""Small drawing helpers used to render Macrova report diagrams as PNG."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.path import Path

# Palette matching the existing Macrova figure set
TEAL = "#1a9c8a"
TEAL_DARK = "#0f5f55"
TEAL_LIGHT = "#e6f7f5"
BLUE = "#3a83f7"
BLUE_LIGHT = "#eaf1fe"
ORANGE = "#f0a13c"
ORANGE_LIGHT = "#fdf3e3"
GREY = "#5b6b74"
GREY_LIGHT = "#f4f7f9"
BORDER = "#c9d6dd"
INK = "#12333c"

FONT = "DejaVu Sans"

plt.rcParams.update(
    {
        "font.family": FONT,
        "font.size": 11,
        "text.color": INK,
    }
)


def canvas(w=12.8, h=7.3, dpi=118, bg="#fbfdfd"):
    fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100 * h / w)
    ax.axis("off")
    return fig, ax


def save(fig, path):
    fig.savefig(path, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def box(
    ax,
    x,
    y,
    w,
    h,
    title,
    lines=(),
    accent=TEAL,
    fill="#ffffff",
    title_size=12.5,
    body_size=10.4,
    radius=1.2,
    align="center",
    lw=1.1,
    title_color=None,
    shadow=True,
):
    """Rounded box with a coloured top rule, bold title and body text."""
    if shadow:
        sh = mpatches.FancyBboxPatch(
            (x + 0.45, y - 0.55),
            w,
            h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            linewidth=0,
            facecolor="#dfe9ec",
            zorder=1,
        )
        ax.add_patch(sh)
    patch = mpatches.FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        linewidth=lw,
        edgecolor=BORDER,
        facecolor=fill,
        zorder=2,
    )
    ax.add_patch(patch)
    # accent rule on top
    ax.plot(
        [x + 1.0, x + w - 1.0],
        [y + h - 1.05, y + h - 1.05],
        color=accent,
        lw=3.0,
        solid_capstyle="round",
        zorder=3,
    )
    tx = x + w / 2 if align == "center" else x + 1.5
    ty = y + h - 3.4
    ax.text(
        tx,
        ty,
        title,
        ha=align if align != "center" else "center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=title_color or INK,
        zorder=4,
    )
    if lines:
        body = "\n".join(lines)
        ax.text(
            tx,
            ty - 3.0,
            body,
            ha=align if align != "center" else "center",
            va="top",
            fontsize=body_size,
            color=GREY,
            linespacing=1.42,
            zorder=4,
        )
    return (x, y, w, h)


def ellipse(ax, cx, cy, w, h, title, lines=(), accent=TEAL, fill="#ffffff", body_size=9.6):
    e = mpatches.Ellipse((cx, cy), w, h, facecolor=fill, edgecolor=BORDER, lw=1.1, zorder=2)
    ax.add_patch(e)
    ax.plot(
        [cx - w * 0.16, cx + w * 0.16],
        [cy + h / 2 - 0.62, cy + h / 2 - 0.62],
        color=accent,
        lw=2.6,
        solid_capstyle="round",
        zorder=3,
    )
    ax.text(cx, cy + h / 2 - 2.5, title, ha="center", va="top", fontsize=10.4,
            fontweight="bold", color=INK, zorder=4)
    if lines:
        ax.text(cx, cy + h / 2 - 5.6, "\n".join(lines), ha="center", va="top",
                fontsize=body_size, color=GREY, linespacing=1.35, zorder=4)
    return (cx - w / 2, cy - h / 2, w, h)


def arrow(ax, p1, p2, label=None, color=TEAL, lw=1.6, style="-|>", rad=0.0,
          ls="-", label_dx=0.0, label_dy=0.85, label_size=9.6, label_bg=None,
          zorder=1.5):
    props = dict(arrowstyle=style, color=color, lw=lw, linestyle=ls,
                 shrinkA=2, shrinkB=2, mutation_scale=14)
    if rad:
        patch = mpatches.FancyArrowPatch(p1, p2, connectionstyle=f"arc3,rad={rad}",
                                         zorder=zorder, **props)
    else:
        patch = mpatches.FancyArrowPatch(p1, p2, zorder=zorder, **props)
    ax.add_patch(patch)
    if label:
        mx, my = (p1[0] + p2[0]) / 2 + label_dx, (p1[1] + p2[1]) / 2 + label_dy
        ax.text(
            mx,
            my,
            label,
            ha="center",
            va="center",
            fontsize=label_size,
            color=GREY,
            zorder=zorder + 1,
            bbox=dict(boxstyle="round,pad=0.22", fc=label_bg or "#fbfdfd", ec="none", alpha=0.95),
        )


def poly_arrow(ax, points, label=None, color=TEAL, lw=1.6, label_at=None,
               label_size=9.6, ls="-"):
    """Orthogonal connector drawn through a list of points."""
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ax.plot(xs[:-1] + [xs[-1]], ys[:-1] + [ys[-1]], color=color, lw=lw, ls=ls,
            solid_capstyle="round", zorder=1.5)
    arrow(ax, points[-2], points[-1], color=color, lw=lw)
    if label:
        lx, ly = label_at if label_at else points[len(points) // 2]
        ax.text(lx, ly, label, ha="center", va="center", fontsize=label_size, color=GREY,
                bbox=dict(boxstyle="round,pad=0.22", fc="#fbfdfd", ec="none"),
                zorder=3)


def swimlane(ax, x, y, w, h, title, fill=GREY_LIGHT, accent=TEAL):
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=1.2", linewidth=1.0,
                 edgecolor=BORDER, facecolor=fill, zorder=0.6))
    ax.add_patch(mpatches.Rectangle((x, y + h - 4.4), w, 4.4, facecolor="#ffffff",
                 edgecolor=BORDER, lw=1.0, zorder=0.7))
    ax.text(x + w / 2, y + h - 2.2, title, ha="center", va="center", fontsize=10.6,
            fontweight="bold", color=INK, zorder=0.9)


def note(ax, x, y, w, text, accent=ORANGE, size=9.4, fill=ORANGE_LIGHT):
    lines = text.count("\n") + 1
    h = 3.2 + lines * 2.1
    ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=0.9", linewidth=1.0,
                 edgecolor="#f0c48a", facecolor=fill, zorder=2))
    ax.text(x + 1.4, y + h / 2, text, ha="left", va="center", fontsize=size,
            color="#7a4b12", linespacing=1.4, zorder=3)
    return h


def title(ax, text, sub=None, color=INK):
    ax.text(0, 100 * 0 + 0.0, "", ha="left")
