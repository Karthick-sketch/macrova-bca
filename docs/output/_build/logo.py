"""Regenerate the Macrova brand mark used on the title page and in the header."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")


def main():
    teal = "#0f8a7a"
    fig = plt.figure(figsize=(3.2, 3.2), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    for x, h in [(20, 22), (38, 42), (56, 66)]:
        ax.add_patch(Rectangle((x, 14), 12, h, color=teal, alpha=0.92, linewidth=0))
    ax.plot([18, 34, 52, 74], [30, 48, 62, 84], color=teal, linewidth=5.2,
            solid_capstyle="round", solid_joinstyle="round")
    ax.plot([66, 74, 74], [84, 84, 74], color=teal, linewidth=5.2,
            solid_capstyle="round", solid_joinstyle="round")
    fig.savefig(os.path.join(ASSETS, "macrova-logo.png"), transparent=True)
    print("wrote macrova-logo.png")


if __name__ == "__main__":
    main()
