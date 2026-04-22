"""Shared data loading, column constants, and aggregation helpers."""
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "grfc_clean.xlsx"

# ── Exact Excel column names ───────────────────────────────────────────────────
ISO      = "ISO Code 3"
COUNTRY  = "Countries/territories"
REGION   = "Region"
YEAR     = "Year of reference"
TOTAL    = "Total country population"
ANALYSED = "Population analysed"
P3N      = "Population in Phase 3 or above #"
P3P      = "Population in Phase 3 or above %"
P5N      = "Population Phase 5 #"
P5P      = "Population Phase 5 %"
D1       = "Primary driver"
D2       = "Secondary driver"
D3       = "Tertiary driver"

DRIVERS = ["Conflict/Insecurity", "Weather Extremes", "Economic Shocks"]
REGIONS = ["EAST AFRICA", "WEST AFRICA", "CS AFRICA", "MENA", "ASIA", "LAC"]

DRIVER_COLOR = {
    "Conflict/Insecurity": "#ff4d6d",
    "Weather Extremes":    "#4fc3d9",
    "Economic Shocks":     "#ffcf56",
}
REGION_PAL = ["#ff7a59", "#ffb877", "#ff4d6d", "#4fc3d9", "#ffcf56", "#b872ff", "#4fd9a2"]

# Preset countries for Trends tab (10 total, balanced across drivers/geography)
TREND_DEFAULTS = [
    "Sudan", "Afghanistan", "Syrian Arab Republic", "Yemen",
    "Democratic Republic of the Congo",  # conflict belt
    "Ethiopia", "Somalia", "Bangladesh", # weather belt
    "Sri Lanka", "Pakistan",             # economic belt
]

SOURCE_FOOTER = """<div class="source-footer">
  Academic project by Student for Data Science Project Lifecycle.
</div>"""

# UN 2024 world population estimate — for "1 in X" stat
WORLD_POP_2024 = 8_100_000_000


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)
    # Phase 5 is ~94% null — coerce to 0 so aggregation never crashes
    for col in [P3N, P3P, P5N, P5P, TOTAL, ANALYSED]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df[YEAR] = df[YEAR].astype(int)
    # Keep driver columns as NaN — don't fillna, so .dropna() works downstream
    return df


def filter_df(
    df: pd.DataFrame,
    year: int | None = None,
    region: str | None = None,
    driver: str | None = None,
) -> pd.DataFrame:
    d = df
    if year is not None:
        d = d[d[YEAR] == year]
    if region and region not in ("All", "all"):
        d = d[d[REGION] == region]
    if driver and driver not in ("All", "all"):
        d = d[d[D1] == driver]
    return d.copy()


def fmt_M(n: float) -> str:
    v = n / 1e6
    if v >= 100:
        return f"{v:.0f}M"
    elif v >= 10:
        return f"{v:.1f}M"
    return f"{v:.2f}M"


def driver_pill_html(driver: str) -> str:
    cls = {
        "Conflict/Insecurity": "conflict",
        "Weather Extremes":    "weather",
        "Economic Shocks":     "economic",
    }.get(driver, "")
    lbl = {
        "Conflict/Insecurity": "Conflict",
        "Weather Extremes":    "Weather",
        "Economic Shocks":     "Economic",
    }.get(driver, driver or "—")
    if not cls:
        return f"<span style='color:#8b93a1;font-size:11px;'>{lbl}</span>"
    return f'<span class="pill {cls}">{lbl}</span>'


def base_plotly_layout(**extra) -> dict:
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk, system-ui, sans-serif", color="#c3c8d1", size=12),
        hoverlabel=dict(
            bgcolor="rgba(10,14,21,0.95)",
            bordercolor="rgba(255,255,255,0.15)",
            font=dict(family="JetBrains Mono, monospace", color="#f3f5f8", size=12),
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.07)", zeroline=False,
            linecolor="rgba(255,255,255,0.07)",
            tickfont=dict(size=11, color="#8b93a1"),
            ticks="outside", ticklen=4, tickcolor="rgba(255,255,255,0.07)",
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.07)", zeroline=False,
            linecolor="rgba(0,0,0,0)",
            tickfont=dict(size=11, color="#8b93a1"),
        ),
    )
    layout.update(extra)
    return layout
