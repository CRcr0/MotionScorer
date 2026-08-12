"""Figure 5: semantic disagreement and teacher-relative correction.

The figure combines the strongest statistical summaries available from the
verified table: a teacher-relative regime heatmap, TranscendRate, and
worst-group MAE.  Real camera/BEV case cards are intentionally not fabricated;
they should be added only when the selected WOD-E2E items and rendered assets
are checked into the project.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from plotting.data import SEMANTIC_REGIMES
from plotting.style import (
    COLORS,
    METHOD_COLORS,
    add_panel_label,
    clean_axes,
    configure_matplotlib,
    save_figure,
)


def _row(name: str) -> dict[str, float | str | None]:
    return next(item for item in SEMANTIC_REGIMES if item["name"] == name)


def make_figure() -> None:
    configure_matplotlib()

    teacher = _row("Scheme-B teacher")
    heatmap_methods = [
        "Aggregated EPDMS",
        "Direct scalar",
        "Plain readout",
        "LoRA scorer",
        "nuGuidance",
    ]
    columns = [
        ("Agreement", "agreement"),
        ("Rule over-\npenalty", "over_penalty"),
        ("Rule-pass\nblind spot", "blind_spot"),
    ]

    delta_values = []
    for method in heatmap_methods:
        item = _row(method)
        delta_values.append(
            [float(item[key]) - float(teacher[key]) for _, key in columns]
        )

    fig = plt.figure(figsize=(7.25, 3.55))
    grid = fig.add_gridspec(
        2,
        2,
        width_ratios=[1.62, 1.0],
        height_ratios=[1.0, 1.0],
        wspace=0.32,
        hspace=0.50,
    )
    ax_heat = fig.add_subplot(grid[:, 0])
    ax_trans = fig.add_subplot(grid[0, 1])
    ax_worst = fig.add_subplot(grid[1, 1])

    cmap = LinearSegmentedColormap.from_list(
        "teacher_delta",
        [COLORS["blue"], COLORS["white"], COLORS["red"]],
        N=256,
    )
    image = ax_heat.imshow(delta_values, cmap=cmap, vmin=-1.2, vmax=1.2, aspect="auto")

    for row_idx, method in enumerate(heatmap_methods):
        for col_idx, value in enumerate(delta_values[row_idx]):
            text_color = COLORS["white"] if abs(value) >= 0.62 else COLORS["black"]
            ax_heat.text(
                col_idx,
                row_idx,
                f"{value:+.2f}",
                ha="center",
                va="center",
                fontsize=11.2,
                fontweight="bold",
                color=text_color,
            )

    ax_heat.set_xticks(range(len(columns)))
    ax_heat.set_xticklabels([label for label, _ in columns], fontsize=9.7, fontweight="bold")
    ax_heat.set_yticks(range(len(heatmap_methods)))
    ax_heat.set_yticklabels(heatmap_methods, fontsize=9.8)
    for tick, method in zip(ax_heat.get_yticklabels(), heatmap_methods):
        if method == "nuGuidance":
            tick.set_color(COLORS["purple"])
            tick.set_fontweight("bold")
    ax_heat.tick_params(axis="both", length=0)
    for spine in ax_heat.spines.values():
        spine.set_linewidth(1.5)
        spine.set_color(COLORS["black"])

    colorbar = fig.colorbar(
        image,
        ax=ax_heat,
        orientation="horizontal",
        fraction=0.07,
        pad=0.16,
        aspect=35,
    )
    colorbar.set_label(
        "$\\Delta$MAE relative to Scheme-B teacher  (negative is better)",
        fontsize=9.4,
        fontweight="bold",
    )
    colorbar.ax.tick_params(labelsize=8.5, width=1.2, length=3)
    colorbar.outline.set_linewidth(1.2)
    add_panel_label(ax_heat, "(a) Where does each method exceed the teacher?")

    trans_methods = ["Direct scalar", "Plain readout", "LoRA scorer", "nuGuidance"]
    trans_values = [float(_row(name)["transcend"]) for name in trans_methods]
    trans_y = list(reversed(range(len(trans_methods))))
    ax_trans.axvline(50.0, color=COLORS["black"], linewidth=1.5, linestyle="--", alpha=0.75)
    for y, method, value in zip(trans_y, trans_methods, trans_values):
        color = METHOD_COLORS[method]
        ax_trans.hlines(y, 46.0, value, color=color, linewidth=5.5, zorder=2)
        ax_trans.scatter(
            value,
            y,
            s=90 if method != "nuGuidance" else 125,
            marker="o" if method != "nuGuidance" else "D",
            color=color,
            edgecolors="white",
            linewidths=1.6,
            zorder=4,
        )
        ax_trans.text(
            value + 0.35,
            y,
            f"{value:.1f}\%",
            va="center",
            ha="left",
            fontsize=9.2,
            fontweight="bold",
            color=color,
        )
    ax_trans.set_yticks(trans_y)
    ax_trans.set_yticklabels(["Direct", "Plain", "LoRA", "nuGuidance"], fontsize=8.9)
    ax_trans.set_xlim(46.0, 63.4)
    ax_trans.set_xlabel("TranscendRate (\%)")
    ax_trans.text(
        50.15,
        3.45,
        "more often closer to human than teacher $\\rightarrow$",
        fontsize=7.9,
        fontweight="bold",
        color=COLORS["charcoal"],
        ha="left",
    )
    add_panel_label(ax_trans, "(b) Teacher-error correction")
    clean_axes(ax_trans)

    worst_methods = [
        "Aggregated EPDMS",
        "Scheme-B teacher",
        "Direct scalar",
        "Plain readout",
        "LoRA scorer",
        "nuGuidance",
    ]
    worst_values = [float(_row(name)["worst"]) for name in worst_methods]
    worst_y = list(reversed(range(len(worst_methods))))
    for y, method, value in zip(worst_y, worst_methods, worst_values):
        color = METHOD_COLORS[method]
        ax_worst.hlines(y, 2.55, value, color=color, linewidth=4.8, zorder=2)
        ax_worst.scatter(
            value,
            y,
            s=75 if method != "nuGuidance" else 108,
            marker="o" if method != "nuGuidance" else "D",
            color=color,
            edgecolors="white",
            linewidths=1.5,
            zorder=4,
        )
        ax_worst.text(
            value + 0.045,
            y,
            f"{value:.2f}",
            va="center",
            ha="left",
            fontsize=8.6,
            fontweight="bold" if method == "nuGuidance" else "semibold",
            color=color,
        )
    ax_worst.set_yticks(worst_y)
    ax_worst.set_yticklabels(["EPDMS", "Teacher", "Direct", "Plain", "LoRA", "nuGuidance"], fontsize=8.5)
    ax_worst.set_xlim(2.55, 4.55)
    ax_worst.set_xlabel("Worst-group MAE $\\downarrow$")
    add_panel_label(ax_worst, "(c) Worst-group robustness")
    clean_axes(ax_worst)

    fig.subplots_adjust(left=0.18, right=0.985, bottom=0.18, top=0.90)
    save_figure(fig, "fig_semantic_disagreement")


if __name__ == "__main__":
    make_figure()
