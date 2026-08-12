"""Shared visual style for MotionScorer paper figures.

The style intentionally mirrors the clean visual language of recent top-tier
vision and autonomous-driving papers: compact small multiples, strong black
axes, deep muted colors, direct effect annotations, pure white backgrounds,
and no decorative grids.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = ROOT / "figures"

COLORS = {
    "purple": "#5B2A86",
    "blue": "#1F4E79",
    "teal": "#0B6668",
    "orange": "#A55312",
    "red": "#9B2C2C",
    "brown": "#7A4E2D",
    "charcoal": "#343A40",
    "gray": "#6B7280",
    "mid_gray": "#A3AAB5",
    "light_gray": "#D8DDE5",
    "pale_gray": "#F3F4F6",
    "pale_blue": "#EDF4FA",
    "pale_purple": "#F3EEF8",
    "black": "#111111",
    "white": "#FFFFFF",
}

METHOD_COLORS = {
    "Direct scalar": COLORS["brown"],
    "Analyze-then-score": "#8A6547",
    "Prompt ensemble": COLORS["gray"],
    "Self-consistency": COLORS["mid_gray"],
    "Plain readout": COLORS["blue"],
    "LoRA scorer": COLORS["orange"],
    "nuGuidance": COLORS["purple"],
    "Aggregated EPDMS": COLORS["charcoal"],
    "Scheme-B teacher": COLORS["teal"],
}


def configure_matplotlib() -> None:
    """Configure large, high-contrast, grid-free publication defaults."""

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 10.5,
            "font.weight": "semibold",
            "axes.labelsize": 11.5,
            "axes.labelweight": "bold",
            "axes.titlesize": 12.0,
            "axes.titleweight": "bold",
            "axes.linewidth": 1.8,
            "axes.edgecolor": COLORS["black"],
            "axes.facecolor": COLORS["white"],
            "figure.facecolor": COLORS["white"],
            "savefig.facecolor": COLORS["white"],
            "savefig.edgecolor": COLORS["white"],
            "xtick.labelsize": 9.7,
            "ytick.labelsize": 9.7,
            "xtick.major.width": 1.5,
            "ytick.major.width": 1.5,
            "xtick.major.size": 4.2,
            "ytick.major.size": 4.2,
            "legend.fontsize": 9.3,
            "legend.frameon": False,
            "lines.linewidth": 2.8,
            "lines.markersize": 8.5,
            "patch.linewidth": 1.5,
            "mathtext.fontset": "dejavuserif",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def clean_axes(ax: plt.Axes, *, keep_left: bool = True) -> None:
    """Apply the shared white-background, no-grid axis treatment."""

    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_linewidth(1.8)
    ax.spines["left"].set_visible(keep_left)
    if keep_left:
        ax.spines["left"].set_linewidth(1.8)
    ax.tick_params(axis="both", which="both", direction="out")


def add_panel_label(ax: plt.Axes, label: str) -> None:
    """Add a bold panel label in a consistent location."""

    ax.text(
        -0.04,
        1.075,
        label,
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=12.5,
        fontweight="bold",
        color=COLORS["black"],
    )


def save_figure(fig: plt.Figure, stem: str) -> None:
    """Export an editable vector PDF and a tightly cropped 600-dpi PNG."""

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        FIGURE_DIR / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
        transparent=False,
    )
    fig.savefig(
        FIGURE_DIR / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.025,
        facecolor="white",
        transparent=False,
    )
    plt.close(fig)
