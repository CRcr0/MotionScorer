"""Shared visual style for the MotionScorer experiment figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt


COLORS = {
    "epdms": "#505762",
    "teacher": "#0E6B66",
    "direct": "#76513B",
    "analyze": "#9A5B31",
    "ensemble": "#A44A34",
    "self_consistency": "#76516F",
    "plain": "#1B5C8A",
    "lora": "#C96A18",
    "ours": "#5A2B82",
    "uniform": "#536B80",
    "top": "#9B2428",
    "random": "#2587A8",
    "shuffle": "#C36B1B",
    "accent": "#D06464",
    "black": "#16191D",
    "mid": "#7A8088",
    "light": "#D9DEE5",
    "very_light": "#F1F3F6",
    "white": "#FFFFFF",
}


def configure_style() -> None:
    """Configure a white, grid-free, high-contrast conference-paper style."""

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 13.0,
            "font.weight": "semibold",
            "axes.titlesize": 15.0,
            "axes.titleweight": "bold",
            "axes.labelsize": 14.0,
            "axes.labelweight": "bold",
            "axes.linewidth": 2.2,
            "axes.edgecolor": COLORS["black"],
            "axes.facecolor": COLORS["white"],
            "figure.facecolor": COLORS["white"],
            "savefig.facecolor": COLORS["white"],
            "savefig.edgecolor": COLORS["white"],
            "xtick.labelsize": 11.5,
            "ytick.labelsize": 11.5,
            "xtick.major.width": 1.9,
            "ytick.major.width": 1.9,
            "xtick.major.size": 5.2,
            "ytick.major.size": 5.2,
            "legend.fontsize": 10.5,
            "legend.frameon": False,
            "lines.linewidth": 3.2,
            "lines.markersize": 9.0,
            "patch.linewidth": 1.9,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "mathtext.fontset": "dejavuserif",
        }
    )


def clean_axes(ax: plt.Axes) -> None:
    """Remove chart junk while retaining strong publication axes."""

    ax.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(2.2)
    ax.spines["bottom"].set_linewidth(2.2)
    ax.tick_params(axis="both", which="both", direction="out")


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    """Save an editable vector PDF and a 600-dpi PNG preview."""

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_dir / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.018,
        facecolor="white",
        transparent=False,
    )
    fig.savefig(
        output_dir / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.018,
        facecolor="white",
        transparent=False,
    )
    plt.close(fig)
