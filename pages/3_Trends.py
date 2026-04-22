"""Tab 3 — Trends · Country trajectories, regional footprint, Phase 5 frontier."""
import streamlit as st
import plotly.graph_objects as go
 
from utils.data_loader import (
    load_data, filter_df, base_plotly_layout,
    P3N, P3P, P5N, COUNTRY, REGION, YEAR, D1,
    DRIVER_COLOR, REGIONS, TREND_DEFAULTS, REGION_PAL, SOURCE_FOOTER,
)
 
st.set_page_config(
    page_title="Hunger Atlas · Trends",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
 
df = load_data()
all_years = sorted(df[YEAR].unique())
all_countries = sorted(df[COUNTRY].dropna().unique().tolist())
 
# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="eyebrow" style="margin-bottom:6px;">03 · Trends</div>', unsafe_allow_html=True)
    st.markdown("---")
 
    # Map TREND_DEFAULTS names against actual data
    valid_defaults = [c for c in TREND_DEFAULTS if c in all_countries]
    countries_sel = st.multiselect(
        "Compare countries",
        options=all_countries,
        default=valid_defaults,
        key="tr_countries",
    )
    mode = st.radio("Metric", ["Millions (Phase 3+)", "% of population"], key="tr_mode", horizontal=True)
    st.markdown("---")
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;letter-spacing:.12em;'
        'color:#5a6270;text-transform:uppercase;">Driver legend</div>',
        unsafe_allow_html=True,
    )
    for d, c in DRIVER_COLOR.items():
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-top:6px;">'
            f'<div style="width:10px;height:10px;background:{c};border-radius:2px;flex-shrink:0;"></div>'
            f'<div style="font-size:11px;color:#8b93a1;">{d.split("/")[0]}</div></div>',
            unsafe_allow_html=True,
        )
 
# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card e3">
  <div class="eyebrow">TRENDS · 2016 — 2025</div>
  <h1 class="hero-h1">The curve that <em>won't bend.</em></h1>
  <p class="deck">Compare multiple countries side-by-side. Toggle countries in the sidebar.
  Switch between absolute counts and share of national population.</p>
</div>""", unsafe_allow_html=True)
 
use_pct = "%" in mode
 
# ── FIG 07 · Multi-line trajectories ──────────────────────────────────────────
st.markdown(f"""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Country trajectories</h2>
    <span class="fig-label">FIG 07 / MULTI-LINE</span>
  </div>
  <p class="section-cap">{'Share of national population in Phase 3+.' if use_pct else 'People in Phase 3+ (millions).'}</p>
</div>""", unsafe_allow_html=True)
 
PALETTE = ["#ff7a59","#4fc3d9","#ffcf56","#b872ff","#4fd9a2",
           "#ff4d6d","#7a9bff","#ffb877","#c9ff8a","#ffdc7d"]
 
fig_ml = go.Figure()
if countries_sel:
    for i, c in enumerate(countries_sel):
        sub = df[df[COUNTRY] == c].set_index(YEAR).reindex(all_years)
        ys  = (sub[P3P].tolist() if use_pct else (sub[P3N] / 1e6).tolist())
        col = PALETTE[i % len(PALETTE)]
        suffix = "%" if use_pct else "M"
        fig_ml.add_trace(go.Scatter(
            x=all_years, y=ys, name=c,
            mode="lines+markers",
            line=dict(color=col, width=2),
            marker=dict(size=5, color=col),
            connectgaps=False,
            hovertemplate=f"<b>{c}</b><br>%{{x}}: %{{y:.1f}}{suffix}<extra></extra>",
        ))
else:
    fig_ml.add_annotation(text="Select countries in the sidebar →",
                          x=0.5, y=0.5, showarrow=False,
                          font=dict(size=14, color="#8b93a1"))
 
fig_ml.update_layout(**base_plotly_layout(
    height=440,
    margin=dict(l=50, r=30, t=20, b=70),
    xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(size=11, color="#8b93a1"), dtick=1, tickformat="d"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(size=11, color="#8b93a1"),
               ticksuffix="%" if use_pct else "M", rangemode="tozero", showgrid=True),
    legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11, color="#c3c8d1"),
                bgcolor="rgba(0,0,0,0)"),
    hovermode="x unified",
))
st.plotly_chart(fig_ml, width="stretch", config=dict(displayModeBar=False))
 
# ── FIG 08 + 09 side by side ───────────────────────────────────────────────────
c_area, c_p5 = st.columns(2, gap="large")
 
with c_area:
    st.markdown("""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Regional footprint</h2>
    <span class="fig-label">FIG 08 / STACKED AREA</span>
  </div>
  <p class="section-cap">E. Africa and W. Africa carry the largest share.</p>
</div>""", unsafe_allow_html=True)
 
    region_labels = {
        "EAST AFRICA": "E. Africa", "WEST AFRICA": "W. Africa",
        "CS AFRICA": "C&S Africa", "ASIA": "Asia",
        "MENA": "MENA", "LAC": "Americas",
    }
    fig_ra = go.Figure()
    for i, reg in enumerate(REGIONS):
        ys = [df[(df[YEAR] == y) & (df[REGION] == reg)][P3N].sum() / 1e6 for y in all_years]
        col = REGION_PAL[i]
        fig_ra.add_trace(go.Scatter(
            x=all_years, y=ys, name=region_labels.get(reg, reg),
            mode="lines", stackgroup="r",
            line=dict(color=col, width=0.8),
            fillcolor=f"rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},0.69)",
            hovertemplate=f"<b>{region_labels.get(reg, reg)}</b><br>%{{x}}: %{{y:.1f}}M<extra></extra>",
        ))
    fig_ra.update_layout(**base_plotly_layout(
        height=340,
        margin=dict(l=50, r=20, t=10, b=70),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                   tickfont=dict(size=11, color="#8b93a1"), dtick=1, tickformat="d"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                   tickfont=dict(size=11, color="#8b93a1"), ticksuffix="M"),
        legend=dict(orientation="h", y=-0.26, x=0, font=dict(size=10, color="#c3c8d1"),
                    bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
    ))
    st.plotly_chart(fig_ra, width="stretch", config=dict(displayModeBar=False))
 
with c_p5:
    st.markdown("""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Phase 5 · Famine</h2>
    <span class="fig-label">FIG 09 / AREA</span>
  </div>
  <p class="section-cap">Phase 5 represents catastrophic hunger - the most severe classification on the IPC scale.
  Only 34 country-years have ever recorded it.
  Gaps = no reported famine that year.</p>
</div>""", unsafe_allow_html=True)
 
    p5_by_year = {y: df[df[YEAR] == y][P5N].sum() for y in all_years}
    p5_ys = [v / 1e6 if v > 0 else None for v in p5_by_year.values()]
    annotations_p5 = []
    if 2023 in p5_by_year and p5_by_year[2023] > 0:
        annotations_p5.append(dict(
            x=2023, y=p5_by_year[2023] / 1e6, text="Sudan + Gaza",
            font=dict(family="JetBrains Mono, monospace", size=9, color="#ffe3b5"),
            arrowcolor="rgba(255,255,255,0.3)", ax=-30, ay=-30,
        ))
    if 2022 in p5_by_year and p5_by_year[2022] > 0:
        annotations_p5.append(dict(
            x=2022, y=p5_by_year[2022] / 1e6, text="Tigray",
            font=dict(family="JetBrains Mono, monospace", size=9, color="#ffe3b5"),
            arrowcolor="rgba(255,255,255,0.3)", ax=-20, ay=-30,
        ))
 
    fig_p5 = go.Figure(go.Scatter(
        x=all_years, y=p5_ys,
        mode="lines+markers",
        line=dict(color="#ff4d6d", width=2.5),
        fill="tozeroy", fillcolor="rgba(255,77,109,0.18)",
        marker=dict(size=6, color="#ff4d6d", line=dict(color="rgba(5,7,11,0.9)", width=1.5)),
        connectgaps=False,
        hovertemplate="<b>%{x}</b><br>%{y:.2f}M in Phase 5<extra></extra>",
    ))
    fig_p5.update_layout(**base_plotly_layout(
        height=340,
        margin=dict(l=50, r=20, t=30, b=40),
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                   tickfont=dict(size=11, color="#8b93a1"), dtick=1, tickformat="d"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                   tickfont=dict(size=11, color="#8b93a1"), ticksuffix="M", rangemode="tozero"),
        annotations=annotations_p5,
    ))
    st.plotly_chart(fig_p5, width="stretch", config=dict(displayModeBar=False))
 
st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)
