"""Tab 1 — Overview · Hunger Atlas Global Food Crisis Dashboard."""

import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import (
    load_data, filter_df, fmt_M, driver_pill_html, base_plotly_layout,
    P3N, P3P, P5N, COUNTRY, REGION, YEAR, ISO, D1,
    DRIVERS, DRIVER_COLOR, SOURCE_FOOTER, WORLD_POP_2024,
)

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hunger Atlas · Overview",
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
    st.markdown('<div class="eyebrow" style="margin-bottom:6px;">01 · Overview</div>', unsafe_allow_html=True)
    st.markdown('<span class="live-badge">● Live · GRFC 2025</span>', unsafe_allow_html=True)
    st.markdown("---")
    year_opts = ["All years"] + [str(y) for y in all_years]
    year_sel  = st.selectbox("Year", year_opts, index=year_opts.index("2024"), key="ov_year")
    year      = None if year_sel == "All years" else int(year_sel)
    region = st.selectbox(
        "Region",
        ["All", "EAST AFRICA", "WEST AFRICA", "CS AFRICA", "MENA", "ASIA", "LAC"],
        key="ov_region",
    )
    driver = st.selectbox("Primary Driver", ["All"] + DRIVERS, key="ov_driver")
    if year == 2025:
        st.markdown('<div class="note-2025">2025 MYU — partial (41 countries)</div>', unsafe_allow_html=True)

# ── Filtered data ──────────────────────────────────────────────────────────────
dfp    = filter_df(df, region=region, driver=driver)

# ── Filtered data ──────────────────────────────────────────────────────────────
dfp    = filter_df(df, region=region, driver=driver)
dfp_yr = filter_df(dfp, year=year)  # year=None returns all years
df_2016 = filter_df(df, year=2016, region=region, driver=driver)

# For "All years", use 2024 for the hero stats (summing across years is misleading)
if year is None:
    dfp_hero = filter_df(dfp, year=2024)
else:
    dfp_hero = dfp_yr

total_n   = dfp_hero[P3N].sum()
base_2016 = df_2016[P3N].sum()
delta_pct = int(round((total_n - base_2016) / base_2016 * 100)) if base_2016 > 0 else 0
countries = int(dfp_hero[COUNTRY].nunique())
p5_total  = dfp_hero[P5N].sum()

year_label = year_sel  # for display in hero text

crisis_2024 = df[df[YEAR] == 2024][P3N].sum()
one_in      = round(WORLD_POP_2024 / crisis_2024) if crisis_2024 > 0 else "?"

# ── Hero ───────────────────────────────────────────────────────────────────────
c_left, c_right = st.columns([1.55, 1], gap="large")
with c_left:
    st.markdown(f"""
<div class="glass-card e3">
  <div class="eyebrow">OVERVIEW · {year_label} SNAPSHOT</div>
  <h1 class="hero-h1">The <em>Global Food Crisis</em> is rapidly worsening.</h1>
  <div style="font-family:'Instrument Serif',Georgia,serif;font-size:62px;line-height:1;
              margin:0 0 14px;letter-spacing:-0.03em;color:#ffe3b5;">
    1 <span style="font-size:26px;color:#8b93a1;font-style:italic;">in</span> {one_in}
  </div>
  <p class="deck">Since 2016, the population facing <b>acute food insecurity</b> has nearly tripled -
  from 105&nbsp;million people to a record 295&nbsp;million in 2024.
  {'Hero figures show 2024 — the last year with full country coverage (2025 is a partial mid-year update).' if year is None else f'Showing {year_label} data across {countries} countries.'}</p>
</div>""", unsafe_allow_html=True)

with c_right:
    st.markdown(f"""
<div class="glass-card e3" style="height:100%;">
  <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.16em;
              color:#8b93a1;text-transform:uppercase;margin-bottom:10px;">
    People in Phase 3 or above · {'2024 (full coverage)' if year is None else year_label}
  </div>
  <div style="font-family:'Instrument Serif',Georgia,serif;font-size:68px;line-height:.92;
              letter-spacing:-0.035em;background:linear-gradient(180deg,#ffe3b5,#ff7a59);
              -webkit-background-clip:text;background-clip:text;color:transparent;display:inline-block;">
    {total_n/1e6:.0f}<span style="font-size:20px;font-style:italic;
      -webkit-text-fill-color:#8b93a1;background:none;">million</span>
  </div>
  <div style="font-size:13px;color:#c3c8d1;margin-top:14px;line-height:1.5;">
    Phase 3+ on the IPC scale means households face crisis, emergency or famine-level food insecurity.
  </div>
  <div style="margin-top:16px;">
    <span class="live-badge">● Live · GRFC 2025</span>
    <span style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#5a6270;margin-left:10px;">
      529 obs · 10y · 74 countries
    </span>
  </div>
</div>""", unsafe_allow_html=True)

# ── KPI strip ─────────────────────────────────────────────────────────────────
k1, k2, k3, = st.columns(3, gap="medium")
kpi_data = [
    (k1, "Change since 2016",  f"{'+' if delta_pct >= 0 else ''}{delta_pct}%", False, "01",
         "Nearly three times the 2016 baseline."),
    (k2, "Countries reporting", str(countries), False, "02", "Across seven world regions."),
    (k3, "Phase 5 · Famine",   fmt_M(p5_total) if p5_total > 0 else "< 0.01M", True,  "03",
         "Catastrophic hunger — tripled since 2020."),
]
for col_w, label, value, is_accent, idx, note in kpi_data:
    with col_w:
        st.markdown(f"""
<div class="kpi-card">
  <div class="kpi-tag"><span>{label}</span><span class="kpi-idx">{idx}</span></div>
  <div class="kpi-val {'accent' if is_accent else ''}">{value}</div>
  <div class="kpi-note">{note}</div>
</div>""", unsafe_allow_html=True)

st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

# ── FIG 01 · Stacked area trend ────────────────────────────────────────────────
st.markdown("""
<div class="glass-card" style="margin-top:6px;">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">A decade of deepening crisis</h2>
    <span class="fig-label">FIG 01 / STACKED AREA · 2016 — 2025</span>
  </div>
  <p class="section-cap">Phase 3+ population has grown in every region. The sharpest escalation comes from
  <em>conflict-driven hunger</em>. Hover for annual detail.</p>
</div>""", unsafe_allow_html=True)

trend_grp = (
    dfp.groupby([YEAR, D1])[P3N]
    .sum()
    .reset_index()
    .rename(columns={YEAR: "year", D1: "driver", P3N: "p3n"})
)
fig_trend = go.Figure()
DRIVER_FILL = {
    "Conflict/Insecurity": "rgba(255,77,109,0.67)",
    "Weather Extremes":    "rgba(79,195,217,0.67)",
    "Economic Shocks":     "rgba(255,207,86,0.67)",
}
for d in DRIVERS:
    sub = trend_grp[trend_grp["driver"] == d].set_index("year").reindex(all_years, fill_value=0)
    fig_trend.add_trace(go.Scatter(
        x=all_years, y=sub["p3n"].values / 1e6,
        name=d.split("/")[0], mode="lines", stackgroup="one",
        line=dict(color=DRIVER_COLOR[d], width=1.2),
        fillcolor=DRIVER_FILL[d],
        hovertemplate=f"<b>{d}</b><br>%{{x}}: %{{y:.1f}}M<extra></extra>",
    ))

events = [(2020, 150, "COVID-19"), (2022, 248, "Ukraine war"), (2023, 278, "Sudan conflict")]
fig_trend.update_layout(**base_plotly_layout(
    height=360,
    margin=dict(l=50, r=20, t=30, b=40),
    xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(size=11, color="#8b93a1"), dtick=1, tickformat="d"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(size=11, color="#8b93a1"), ticksuffix="M", rangemode="tozero"),
    showlegend=True,
    legend=dict(orientation="h", y=1.16, x=0, font=dict(size=12, color="#c3c8d1"),
                bgcolor="rgba(0,0,0,0)"),
    hovermode="x unified",
    shapes=[dict(type="line", x0=ex, x1=ex, y0=0, y1=ey, xref="x", yref="y",
                 line=dict(color="rgba(255,255,255,0.22)", width=1, dash="dot"))
            for ex, ey, _ in events],
    annotations=[dict(x=ex, y=ey, text=et, showarrow=False,
                      font=dict(family="JetBrains Mono, monospace", size=9, color="#ffe3b5"),
                      bgcolor="rgba(5,7,11,0.70)", borderpad=3, yshift=10)
                 for ex, ey, et in events],
))
st.plotly_chart(fig_trend, width="stretch", config=dict(displayModeBar=False))

# ── FIG 02 · Choropleth + FIG 03 · Donut ──────────────────────────────────────
c_map, c_donut = st.columns([1.55, 1], gap="large")

with c_map:
    st.markdown("""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Where the crisis exists</h2>
    <span class="fig-label">FIG 02 / CHOROPLETH</span>
  </div>
  <p class="section-cap">Six countries account for half the global total. Africa and South Asia
  concentrate the deepest need.</p>
</div>""", unsafe_allow_html=True)

    map_df = dfp_yr.dropna(subset=[ISO])
    fig_map = go.Figure(go.Choropleth(
        locations=map_df[ISO],
        z=map_df[P3N] / 1e6,
        text=map_df[COUNTRY],
        customdata=list(zip(
            map_df[P3P].round(1),
            map_df[D1].fillna("—"),
        )),
        hovertemplate=(
            "<b>%{text}</b><br>%{z:.2f}M in Phase 3+<br>"
            "%{customdata[0]}% of population<br>Driver: %{customdata[1]}<extra></extra>"
        ),
        colorscale=[
            [0,    "rgba(255,122,89,0.08)"],
            [0.30, "rgba(255,122,89,0.35)"],
            [0.65, "rgba(255,122,89,0.75)"],
            [1,    "rgba(255,227,181,1)"],
        ],
        marker=dict(line=dict(color="rgba(5,7,11,0.60)", width=0.4)),
        colorbar=dict(
            title=dict(text="M", font=dict(size=10, color="#8b93a1", family="JetBrains Mono, monospace")),
            tickfont=dict(size=10, color="#8b93a1"),
            thickness=6, len=0.55, outlinewidth=0,
        ),
        zmin=0, zmax=32,
    ))
    fig_map.update_layout(**base_plotly_layout(
        height=420, margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(
            bgcolor="rgba(0,0,0,0)", showframe=False,
            showcoastlines=True, coastlinecolor="rgba(255,255,255,0.10)", coastlinewidth=0.3,
            showland=True, landcolor="rgba(255,255,255,0.03)",
            showocean=True, oceancolor="rgba(0,0,0,0)", showlakes=False,
            projection=dict(type="natural earth"),
        ),
    ))
    st.plotly_chart(fig_map, width="stretch", config=dict(displayModeBar=False))

with c_donut:
    st.markdown(f"""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">What drives it</h2>
    <span class="fig-label">FIG 03 / DONUT</span>
  </div>
  <p class="section-cap">Primary cause, {year}.</p>
</div>""", unsafe_allow_html=True)

    drv_vals  = [dfp_yr[dfp_yr[D1] == d][P3N].sum() for d in DRIVERS]
    total_drv = sum(drv_vals)
    fig_donut = go.Figure(go.Pie(
        labels=["Conflict", "Weather", "Economic"],
        values=drv_vals,
        hole=0.66,
        marker=dict(
            colors=[DRIVER_COLOR[d] for d in DRIVERS],
            line=dict(color="rgba(5,7,11,0.85)", width=2),
        ),
        textinfo="percent", textposition="outside",
        textfont=dict(family="JetBrains Mono, monospace", size=11, color="#c3c8d1"),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f} people<br>%{percent}<extra></extra>",
        sort=False, direction="clockwise", rotation=-90,
    ))
    center_txt = (
        f"<span style='font-size:26px;color:#f3f5f8'>{total_drv/1e6:.0f}M</span>"
        f"<br><span style='font-size:10px;color:#8b93a1'>{year} TOTAL</span>"
    )
    fig_donut.update_layout(**base_plotly_layout(
        height=380, margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True,
        legend=dict(orientation="v", x=1.0, y=0.5, yanchor="middle",
                    font=dict(size=12, color="#c3c8d1"), bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(text=center_txt, x=0.5, y=0.5, showarrow=False)],
    ))
    st.plotly_chart(fig_donut, width="stretch", config=dict(displayModeBar=False))

# ── FIG 04 · Top-10 ranked bars ───────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Ten nations at the centre of the crisis</h2>
    <span class="fig-label">FIG 04 / RANKED BARS</span>
  </div>
  <p class="section-cap">Bar length = people in Phase 3+; colour = primary driver.
  Together these ten countries account for <em>nearly 70%</em> of the global crisis population.</p>
</div>""", unsafe_allow_html=True)

top10 = dfp_yr.dropna(subset=[P3N]).sort_values(P3N, ascending=False).head(10).sort_values(P3N)
fig_bars = go.Figure(go.Bar(
    orientation="h",
    x=top10[P3N] / 1e6,
    y=top10[COUNTRY],
    marker=dict(color=[DRIVER_COLOR.get(str(d), "#8b93a1") for d in top10[D1]]),
    text=(top10[P3N] / 1e6).round(1).astype(str) + "M",
    textposition="outside",
    textfont=dict(family="Instrument Serif, Georgia, serif", size=13, color="#f3f5f8"),
    hovertemplate="<b>%{y}</b><br>%{x:.2f}M people<extra></extra>",
    cliponaxis=False,
))
fig_bars.update_layout(**base_plotly_layout(
    height=380,
    margin=dict(l=220, r=80, t=8, b=30),
    xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(size=11, color="#8b93a1"), ticksuffix="M",
               range=[0, top10[P3N].max() / 1e6 * 1.30], showgrid=True),
    yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
               tickfont=dict(family="Space Grotesk, sans-serif", size=13, color="#f3f5f8"),
               automargin=True),
    bargap=0.38,
))
st.plotly_chart(fig_bars, width="stretch", config=dict(displayModeBar=False))

st.markdown("""
<div style="display:flex;gap:22px;margin-top:2px;margin-bottom:18px;
font-family:'JetBrains Mono',monospace;font-size:11px;color:#c3c8d1;letter-spacing:.04em;">
  <span><span style="display:inline-block;width:10px;height:10px;background:#ff4d6d;
  border-radius:2px;margin-right:7px;vertical-align:middle;"></span>Conflict / Insecurity</span>
  <span><span style="display:inline-block;width:10px;height:10px;background:#4fc3d9;
  border-radius:2px;margin-right:7px;vertical-align:middle;"></span>Weather Extremes</span>
  <span><span style="display:inline-block;width:10px;height:10px;background:#ffcf56;
  border-radius:2px;margin-right:7px;vertical-align:middle;"></span>Economic Shocks</span>
</div>""", unsafe_allow_html=True)

# ── Insight callout ────────────────────────────────────────────────────────────
conflict_total = dfp_yr[dfp_yr[D1] == "Conflict/Insecurity"][P3N].sum()
conflict_pct   = int(conflict_total / total_n * 100) if total_n > 0 else 0
st.markdown(f"""
<div class="insight">
  <div class="insight-lbl">Editor's insight</div>
  <p class="insight-body">Between 2016 and 2024, the number of people facing acute food insecurity
  <span class="hl">nearly tripled.</span> Conflict remains the single largest driver -
  {fmt_M(conflict_total)}, {conflict_pct}% of the total - but weather-extreme hunger has
  <span class="hl">doubled since 2020</span>, reshaping where humanitarian aid is most
  urgently needed.</p>
</div>""", unsafe_allow_html=True)

st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)