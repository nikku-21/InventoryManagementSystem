"""Matplotlib charts: stock overview plus the SQC charts (Pareto, Fishbone)."""
from __future__ import annotations

from .dataframes import defects_df, products_df


def _empty(fig, message="No data yet"):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.text(0.5, 0.5, message, ha="center", va="center", fontsize=12)
    ax.axis("off")


def stock_by_category_chart(fig) -> None:
    df = products_df()
    if df.empty:
        return _empty(fig, "Add products to see stock levels")
    totals = df.groupby("Category")["Quantity"].sum().sort_values(ascending=False)
    fig.clear()
    ax = fig.add_subplot(111)
    ax.bar(totals.index, totals.values, color="#3b82f6")
    ax.set_title("Units in stock by category")
    ax.set_ylabel("Units")
    fig.tight_layout()


def pareto_chart(fig) -> None:
    """Pareto (80/20) chart of logged defects by type."""
    df = defects_df()
    if df.empty:
        return _empty(fig, "Log defects in the Defect Log tab first")
    counts = df["Type"].value_counts()
    cumulative = counts.cumsum() / counts.sum() * 100
    fig.clear()
    ax = fig.add_subplot(111)
    ax.bar(counts.index, counts.values, color="#3b82f6")
    ax.set_ylabel("Defect count")
    ax2 = ax.twinx()
    ax2.plot(counts.index, cumulative.values, color="#ef4444", marker="o")
    ax2.axhline(80, ls="--", color="grey")
    ax2.set_ylim(0, 105)
    ax2.set_ylabel("Cumulative %")
    ax.set_title("Pareto analysis of defects (80/20 rule)")
    fig.tight_layout()


DEFAULT_CAUSES = {
    "People": ["Insufficient training", "Typing mistakes"],
    "Process": ["No data validation step", "Manual stock counts"],
    "Software Code": ["Unhandled exceptions", "Missing unit tests"],
    "Infrastructure": ["No automatic backup", "Slow disk"],
}


def fishbone_chart(fig, effect="Inaccurate stock data", causes=None) -> None:
    """Ishikawa diagram: four cause categories feeding one effect."""
    causes = causes or DEFAULT_CAUSES
    fig.clear()
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 12)
    ax.set_ylim(-5, 5)
    ax.axis("off")
    ax.annotate("", xy=(9.6, 0), xytext=(0.3, 0), arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#1e3a8a"))
    ax.text(9.7, 0, effect, va="center", fontsize=11, fontweight="bold",
            bbox=dict(boxstyle="round", fc="#dbeafe", ec="#1e3a8a"))
    for i, (category, items) in enumerate(causes.items()):
        x = 3.2 if i % 2 == 0 else 7.0
        sign = 1 if i < 2 else -1
        ax.plot([x, x - 1.4], [0, sign * 3.6], color="#1e3a8a", lw=1.8)
        ax.text(x - 1.4, sign * 4.1, category, ha="center", fontweight="bold", color="#b91c1c")
        for j, item in enumerate(items):
            y = sign * (1.2 + 1.2 * j)
            ax.text(x - 0.3 - 0.4 * (y * sign) / 2.4, y, item, ha="right", va="center", fontsize=8)
    fig.tight_layout()
