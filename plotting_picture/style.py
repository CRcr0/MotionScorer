"""Shared visual style for the MotionScorer experiment figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


COLORS = {
    "epdms": "#555B66",
    "teacher": "#16706A",
    "direct": "#80512F",
    "analyze": "#B35A16",
    "ensemble": "#9A3B25",
    "self_consistency": "#6E3B63",
    "plain": "#1F5A85",
    "lora": "#D06A12",
    "ours": "#5B2A86",
    "uniform": "#3F5368",
    "top": "#A3262A",
    "random": "#157A78",
    "shuffle": "#C46B17",
    "black": "#171A1F",
    "light": "#D9DEE5",
    "white": "#FFFFFF",
}


def configure_style() -> None:
    """Configure a white, grid-free, high-contrast conference-paper style."""

    mpl.use("Agg")
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 12.0,
            "font.weight": "semibold",
            "axes.titlesize": 14.0,
            "axes.titleweight": "bold",
            "axes.labelsize": 13.0,
            "axes.labelweight": "bold",
            "axes.linewidth": 2.0,
            "axes.edgecolor": COLORS["black"],
            "axes.facecolor": COLORS["white"],
            "figure.facecolor": COLORS["white"],
            "savefig.facecolor": COLORS["white"],
            "savefig.edgecolor": COLORS["white"],
            "xtick.labelsize": 10.5,
            "ytick.labelsize": 11.0,
            "xtick.major.width": 1.7,
            "ytick.major.width": 1.7,
            "xtick.major.size": 5.0,
            "ytick.major.size": 5.0,
            "legend.fontsize": 10.0,
            "legend.frameon": False,
            "lines.linewidth": 3.0,
            "lines.markersize": 8.5,
            "patch.linewidth": 1.8,
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
    ax.spines["left"].set_linewidth(2.0)
    ax.spines["bottom"].set_linewidth(2.0)
    ax.tick_params(axis="both", which="both", direction="out")


def save_figure(fig: plt.Figure, output_dir: Path, stem: str) -> None:
    """Save an editable vector PDF and a 600-dpi PNG preview."""

    output_dir.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_dir / f"{stem}.pdf",
        bbox_inches="tight",
        pad_inches=0.035,
        facecolor="white",
        transparent=False,
    )
    fig.savefig(
        output_dir / f"{stem}.png",
        dpi=600,
        bbox_inches="tight",
        pad_inches=0.035,
        facecolor="white",
        transparent=False,
    )
    plt.close(fig)
