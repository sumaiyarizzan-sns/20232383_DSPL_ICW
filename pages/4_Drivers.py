"""Tab 4 — Drivers · What forces drive the global food crisis."""
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.data_loader import (
    load_data, filter_df, fmt_M, base_plotly_layout,
    P3N, COUNTRY, REGION, YEAR, D1,
    DRIVERS, DRIVER_COLOR, REGIONS, SOURCE_FOOTER,
)

st.set_page_config(
    page_title="Hunger Atlas · Drivers",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()
all_years = sorted(df[YEAR].unique())

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="eyebrow" style="margin-bottom:6px;">04 · Drivers</div>', unsafe_allow_html=True)
    st.markdown("---")
    year = st.slider("Reference year", 2016, 2025, 2024, key="dr_year")
    if year == 2025:
        st.markdown('<div class="note-2025">2025 MYU — partial (41 countries)</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;'
        'letter-spacing:.12em;color:#5a6270;text-transform:uppercase;margin-bottom:10px;">'
        'Driver colours</div>',
        unsafe_allow_html=True,
    )

    for d, c in DRIVER_COLOR.items():
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">'
            f'<div style="width:10px;height:10px;background:{c};border-radius:2px;"></div>'
            f'<div style="font-size:11px;color:#8b93a1;">{d.split("/")[0]}</div></div>',
            unsafe_allow_html=True,
        )

dfp_yr = filter_df(df, year=year)

# ── Hero + Driver mix area ─────────────────────────────────────────────────────
c_left, c_right = st.columns([1.55, 1], gap="large")

with c_left:
    st.markdown("""
<div class="glass-card e3">
  <div class="eyebrow">DRIVERS · 2016 — 2025</div>
  <h1 class="hero-h1">Conflict, climate, and <em>collapse</em>.</h1>
  <p class="deck">Three forces drive almost every food crisis on record. Their mix is shifting:
  <b>conflict remains dominant</b>, but <b>weather extremes</b> are rising fastest.</p>
</div>
""", unsafe_allow_html=True)

with c_right:
    st.markdown("""
<div class="glass-card e3">
  <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;
              color:#8b93a1;text-transform:uppercase;margin-bottom:8px;">
    Driver mix · every year
  </div>
</div>
""", unsafe_allow_html=True)

    fig_da = go.Figure()

    for d in DRIVERS:
        ys = [df[(df[YEAR] == y) & (df[D1] == d)][P3N].sum() for y in all_years]

        fig_da.add_trace(go.Scatter(
            x=all_years,
            y=ys,
            name=d.split("/")[0],
            mode="lines",
            stackgroup="d",
            groupnorm="percent",
            line=dict(color=DRIVER_COLOR[d], width=0.5),
            fillcolor=f"rgba({int(DRIVER_COLOR[d][1:3],16)},{int(DRIVER_COLOR[d][3:5],16)},{int(DRIVER_COLOR[d][5:7],16)},0.8)",
            hovertemplate=f"<b>{d}</b><br>%{{x}}: %{{y:.0f}}%<extra></extra>",
        ))

    fig_da.update_layout(**base_plotly_layout(
        height=240,
        margin=dict(l=40, r=10, t=4, b=30),
        xaxis=dict(dtick=1, tickformat="d"),
        yaxis=dict(range=[0, 100], ticksuffix="%"),
        showlegend=False,
    ))

    st.plotly_chart(fig_da, width="stretch", config=dict(displayModeBar=False))

# ── FIG 10 · Small multiples ───────────────────────────────────────────────────
st.markdown(f"""
<div class="glass-card">
  <h2 class="section-h2">The driver changes with the region</h2>
  <span class="fig-label">FIG 10 · {year}</span>
</div>
""", unsafe_allow_html=True)

region_labels = {
    "EAST AFRICA": "E. Africa",
    "WEST AFRICA": "W. Africa",
    "CS AFRICA": "C&S Africa",
    "ASIA": "Asia",
    "MENA": "MENA",
    "LAC": "Americas",
}

driver_short = ["Conflict", "Weather", "Economic"]

fig_sm = make_subplots(rows=1, cols=6)

for i, reg in enumerate(REGIONS, start=1):
    sub = dfp_yr[dfp_yr[REGION] == reg]
    total = sub[P3N].sum() or 1

    vals = [sub[sub[D1] == d][P3N].sum() / total * 100 for d in DRIVERS]

    for d, label, v in zip(DRIVERS, driver_short, vals):
        fig_sm.add_trace(
            go.Bar(
                x=[label],
                y=[v],
                marker=dict(color=DRIVER_COLOR[d]),
                showlegend=False,
                hovertemplate=f"{reg}: %{{y:.0f}}%"
            ),
            row=1, col=i
        )

    # ✅ FIXED annotation (NO x1 domain error)
    if i == 1:
        xref_val = "x domain"
        yref_val = "y domain"
    else:
        xref_val = f"x{i} domain"
        yref_val = f"y{i} domain"

    fig_sm.add_annotation(
        text=region_labels[reg],
        x=0.5,
        y=1.15,
        xref=xref_val,
        yref=yref_val,
        showarrow=False
    )

fig_sm.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    height=300, margin=dict(l=30, r=10, t=34, b=30),
    font=dict(family="Space Grotesk, system-ui, sans-serif", color="#c3c8d1", size=11),
    bargap=0.3,
    hoverlabel=dict(bgcolor="rgba(10,14,21,0.95)", bordercolor="rgba(255,255,255,0.15)",
                    font=dict(family="JetBrains Mono, monospace", color="#f3f5f8", size=12)),
)
for i in range(1, 7):
    fig_sm.update_xaxes(tickfont=dict(size=9, color="#8b93a1"), showgrid=False,
                        zeroline=False, linecolor="rgba(255,255,255,0.07)", row=1, col=i)
    fig_sm.update_yaxes(range=[0, 100], ticksuffix="%", tickfont=dict(size=9, color="#8b93a1"),
                        showgrid=True, gridcolor="rgba(255,255,255,0.07)",
                        zeroline=False, dtick=25, row=1, col=i)
st.plotly_chart(fig_sm, width="stretch", config=dict(displayModeBar=False))


# ── Key finding — computed live ────────────────────────────────────────────────
def driver_share(yr: int) -> dict:
    sub = filter_df(df, year=yr)
    tot = sub[P3N].sum() or 1
    return {d: sub[sub[D1] == d][P3N].sum() / tot * 100 for d in DRIVERS}

share_16  = driver_share(2016)
share_now = driver_share(year)
w_delta   = share_now["Weather Extremes"] - share_16["Weather Extremes"]

st.markdown(f"""
<div class="insight">
  <div class="insight-lbl">Key finding</div>
  <p class="insight-body">
    Weather extremes have grown from
    <span class="hl">{share_16['Weather Extremes']:.0f}% in 2016</span>
    to <span class="hl">{share_now['Weather Extremes']:.0f}% in {year}</span>.
    Conflict remains at the top, but weather extremes are the fastest-growing cause of acute food insecurity in the dataset.
  </p>
</div>""", unsafe_allow_html=True)

st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)

