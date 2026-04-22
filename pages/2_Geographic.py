"""Tab 2 — Geography · Regional drill-down and country profiles."""

import streamlit as st
import plotly.graph_objects as go

from utils.data_loader import (
    load_data, filter_df, fmt_M, driver_pill_html, base_plotly_layout,
    P3N, P3P, P5N, COUNTRY, REGION, YEAR, ISO, D1, D2, D3,
    DRIVER_COLOR, REGIONS, SOURCE_FOOTER,
)

st.set_page_config(
    page_title="Hunger Atlas · Geography",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="eyebrow" style="margin-bottom:6px;">02 · Geography</div>', unsafe_allow_html=True)
    st.markdown("---")
    year = st.slider("Year", 2016, 2025, 2024, key="geo_year")
    if year == 2025:
        st.markdown('<div class="note-2025">2025 MYU — partial (41 countries)</div>', unsafe_allow_html=True)

# ── Data ───────────────────────────────────────────────────────────────────────
dfp_yr = filter_df(df, year=year)

# ── Hero + Regional bar ────────────────────────────────────────────────────────
c_left, c_right = st.columns([1.55, 1], gap="large")

with c_left:
    st.markdown(f"""
<div class="glass-card e3">
  <div class="eyebrow">GEOGRAPHY · REGIONAL DRILL-DOWN</div>
  <h1 class="hero-h1">Zooming <em>in</em>.</h1>
  <p class="deck">The global total only tells part of the story.
   In this tab, explore how the crisis breaks down by region, compare countries by severity,
     and select any country to view its individual profile.</p>
</div>""", unsafe_allow_html=True)

with c_right:
    st.markdown(f"""
<div class="glass-card e3">
  <div style="font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.14em;
              color:#8b93a1;text-transform:uppercase;margin-bottom:8px;">
    Regional share · {year}
  </div>
</div>""", unsafe_allow_html=True)

    reg_grp = dfp_yr.groupby(REGION)[P3N].sum().sort_values()
    fig_regbar = go.Figure(go.Bar(
        orientation="h",
        x=reg_grp.values / 1e6,
        y=reg_grp.index,
        marker=dict(color="#ff7a59"),
        text=[fmt_M(v) for v in reg_grp.values],
        textposition="outside",
        textfont=dict(family="Instrument Serif, Georgia, serif", size=12, color="#f3f5f8"),
        hovertemplate="<b>%{y}</b><br>%{x:.1f}M<extra></extra>",
        cliponaxis=False,
    ))
    fig_regbar.update_layout(**base_plotly_layout(
        height=230,
        margin=dict(l=100, r=60, t=4, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                   tickfont=dict(size=11, color="#c3c8d1"), automargin=True),
        bargap=0.4,
    ))
    st.plotly_chart(fig_regbar, width="stretch", config=dict(displayModeBar=False))

# ── Country table + Profile card ───────────────────────────────────────────────
ranked = (
    dfp_yr[dfp_yr[P3P] > 0]
    .sort_values(P3P, ascending=False)
    .head(25)
    .reset_index(drop=True)
)
max_p3n = ranked[P3N].max() if len(ranked) else 1

c_table, c_profile = st.columns([2, 1], gap="large")

with c_table:
    st.markdown(f"""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Countries ranked by crisis severity</h2>
    <span class="fig-label">FIG 05 / RANK · {year}</span>
  </div>
  <p class="section-cap">Sorted by <em>share of national population</em> in Phase 3+.
  Select a country below to load its profile.</p>
</div>""", unsafe_allow_html=True)

    country_select = st.selectbox(
        "Select country for profile →",
        options=ranked[COUNTRY].tolist(),
        index=0,
        key="geo_country",
        label_visibility="collapsed",
    )

    # Build HTML table
    rows_html = ""
    for i, row in ranked.iterrows():
        bar_w = int(row[P3N] / max_p3n * 100)
        pill  = driver_pill_html(str(row[D1]) if row[D1] and str(row[D1]) != "nan" else "")
        rows_html += f"""
<tr>
  <td class="num" style="color:#5a6270;">{str(i+1).zfill(2)}</td>
  <td class="cname">{row[COUNTRY]}</td>
  <td style="color:#8b93a1;font-size:11px;">{row[REGION]}</td>
  <td class="num">{row[P3N]/1e6:.1f}</td>
  <td>
    <div style="display:flex;align-items:center;gap:8px;min-width:130px;">
      <div style="flex:1;height:4px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;">
        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#ff7a59,#ffb877);border-radius:3px;"></div>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:11px;min-width:36px;text-align:right;color:#f3f5f8;">
        {row[P3P]:.0f}%
      </div>
    </div>
  </td>
  <td>{pill}</td>
</tr>"""

    st.markdown(f"""
<div class="dtable-wrap" style="max-height:480px;overflow-y:auto;">
<table class="dtable">
  <thead>
    <tr>
      <th style="width:26px;">#</th>
      <th>Country</th>
      <th>Region</th>
      <th class="num">Phase 3+ (M)</th>
      <th>% of pop.</th>
      <th>Driver</th>
    </tr>
  </thead>
  <tbody>{rows_html}</tbody>
</table>
</div>""", unsafe_allow_html=True)

# ── Country Profile (FIG 06) ───────────────────────────────────────────────────
with c_profile:
    st.markdown("""
<div class="glass-card">
  <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px;">
    <h2 class="section-h2">Country profile</h2>
    <span class="fig-label">FIG 06</span>
  </div>
</div>""", unsafe_allow_html=True)

    prof_rows = df[df[COUNTRY] == country_select].sort_values(YEAR)

    if len(prof_rows) > 0:
        latest = prof_rows.iloc[-1]
        first  = prof_rows.iloc[0]

        # Safe delta calculation
        if first[P3N] > 0:
            delta = int(round((latest[P3N] - first[P3N]) / first[P3N] * 100))
        else:
            delta = 0

        d1_val = str(latest[D1]) if latest[D1] and str(latest[D1]) != "nan" else "—"
        d2_val = str(latest[D2]) if latest[D2] and str(latest[D2]) != "nan" else "—"
        d3_val = str(latest[D3]) if latest[D3] and str(latest[D3]) != "nan" else "—"

        p5_display = fmt_M(latest[P5N]) if latest[P5N] > 0 else "—"
        iso_display = str(latest[ISO]) if latest[ISO] and str(latest[ISO]) != "nan" else ""

        st.markdown(f"""
<div class="glass-card e2" style="margin-top:0;">
  <h3 style="font-family:'Instrument Serif',Georgia,serif;font-weight:400;font-size:26px;
             margin:0 0 2px;letter-spacing:-0.015em;color:#f3f5f8;">{country_select}</h3>
  <div style="font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.10em;
              color:#8b93a1;text-transform:uppercase;margin-bottom:18px;">
    {latest[REGION]} · {iso_display}
  </div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:16px;
              padding-bottom:16px;border-bottom:1px solid rgba(255,255,255,0.07);">
    <div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.10em;
                  color:#8b93a1;text-transform:uppercase;margin-bottom:4px;">Phase 3+ ({int(latest[YEAR])})</div>
      <div style="font-family:'Instrument Serif',Georgia,serif;font-size:24px;color:#ffb877;">{fmt_M(latest[P3N])}</div>
    </div>
    <div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.10em;
                  color:#8b93a1;text-transform:uppercase;margin-bottom:4px;">% population</div>
      <div style="font-family:'Instrument Serif',Georgia,serif;font-size:24px;color:#f3f5f8;">{latest[P3P]:.0f}%</div>
    </div>
    <div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.10em;
                  color:#8b93a1;text-transform:uppercase;margin-bottom:4px;">Phase 5 · Famine</div>
      <div style="font-family:'Instrument Serif',Georgia,serif;font-size:24px;color:#ffb877;">{p5_display}</div>
    </div>
    <div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:9.5px;letter-spacing:.10em;
                  color:#8b93a1;text-transform:uppercase;margin-bottom:4px;">Δ since {int(first[YEAR])}</div>
      <div style="font-family:'Instrument Serif',Georgia,serif;font-size:24px;color:#f3f5f8;">
        {'+' if delta >= 0 else ''}{delta}%
      </div>
    </div>
  </div>
  <div style="display:flex;gap:6px;margin-bottom:14px;">
    <div style="flex:1;padding:8px 10px;border:1px solid rgba(255,255,255,0.08);border-radius:8px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.10em;
                  color:#5a6270;text-transform:uppercase;margin-bottom:3px;">Primary</div>
      <div style="font-size:11px;color:#c3c8d1;">{d1_val.split('/')[0]}</div>
    </div>
    <div style="flex:1;padding:8px 10px;border:1px solid rgba(255,255,255,0.08);border-radius:8px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.10em;
                  color:#5a6270;text-transform:uppercase;margin-bottom:3px;">Secondary</div>
      <div style="font-size:11px;color:#c3c8d1;">{d2_val.split('/')[0] if d2_val != '—' else '—'}</div>
    </div>
    <div style="flex:1;padding:8px 10px;border:1px solid rgba(255,255,255,0.08);border-radius:8px;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:.10em;
                  color:#5a6270;text-transform:uppercase;margin-bottom:3px;">Tertiary</div>
      <div style="font-size:11px;color:#c3c8d1;">{d3_val.split('/')[0] if d3_val != '—' else '—'}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # Sparkline chart
        fig_spark = go.Figure(go.Scatter(
            x=prof_rows[YEAR].tolist(),
            y=(prof_rows[P3N] / 1e6).tolist(),
            mode="lines+markers",
            line=dict(color="#ff7a59", width=2),
            marker=dict(size=4, color="#ff7a59"),
            fill="tozeroy", fillcolor="rgba(255,122,89,0.14)",
            connectgaps=False,
            hovertemplate="%{x}: %{y:.1f}M<extra></extra>",
        ))
        fig_spark.update_layout(**base_plotly_layout(
            height=130,
            margin=dict(l=32, r=10, t=6, b=22),
            xaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                       tickfont=dict(size=9, color="#8b93a1"), showgrid=False,
                       dtick=2, tickformat="d"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.07)", zeroline=False,
                       tickfont=dict(size=9, color="#8b93a1"), ticksuffix="M",
                       rangemode="tozero", nticks=3),
            showlegend=False,
        ))
        st.plotly_chart(fig_spark, width="stretch", config=dict(displayModeBar=False))

        note_txt = (
            f"Observed in {len(prof_rows)} of the last 10 years. "
            f"Crisis population has {'grown' if delta >= 0 else 'fallen'} "
            f"{abs(delta)}% since {int(first[YEAR])}."
        )
        st.markdown(
            f'<p style="font-family:\'Instrument Serif\',Georgia,serif;font-style:italic;'
            f'font-size:13px;color:#c3c8d1;line-height:1.5;margin:6px 0 0;">{note_txt}</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("""
<div class="glass-card e2" style="margin-top:0;">
  <p style="color:#8b93a1;font-size:13px;">No data available for selected country.</p>
</div>""", unsafe_allow_html=True)

st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)
