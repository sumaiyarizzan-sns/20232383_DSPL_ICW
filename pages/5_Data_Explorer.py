"""Tab 5 — Data Explorer · Full filterable GRFC dataset with CSV download."""
import streamlit as st

from utils.data_loader import (
    load_data, filter_df, driver_pill_html,
    P3N, P3P, P5N, COUNTRY, REGION, YEAR, ISO, D1, D2, D3,
    DRIVERS, SOURCE_FOOTER,
)

st.set_page_config(
    page_title="Hunger Atlas · Data Explorer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

df = load_data()
all_years = sorted(df[YEAR].unique())

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="eyebrow" style="margin-bottom:6px;">05 · Data Explorer</div>',
                unsafe_allow_html=True)
    st.markdown("---")
    search     = st.text_input("Search country or region", placeholder="e.g. Sudan, ASIA…", key="de_search")
    year_opts  = ["All years"] + [str(y) for y in all_years]
    year_sel   = st.selectbox("Year", year_opts, index=year_opts.index("2024"), key="de_year")
    driver_sel = st.selectbox("Primary Driver", ["All"] + DRIVERS, key="de_driver")
    st.markdown("---")
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:10px;'
        'letter-spacing:.12em;color:#5a6270;text-transform:uppercase;margin-bottom:6px;">'
        'Dataset stats</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:11px;color:#8b93a1;line-height:1.8;">'
        '529 total observations<br>74 countries<br>10 years (2016–2025)<br>7 regions</div>',
        unsafe_allow_html=True,
    )

# ── Apply filters ──────────────────────────────────────────────────────────────
year_int = None if year_sel == "All years" else int(year_sel)
dff = filter_df(df, year=year_int, driver=driver_sel if driver_sel != "All" else None)

if search.strip():
    q   = search.strip().lower()
    dff = dff[
        dff[COUNTRY].str.lower().str.contains(q, na=False) |
        dff[REGION].str.lower().str.contains(q, na=False)
    ]

dff       = dff.sort_values(P3N, ascending=False).reset_index(drop=True)
row_count = len(dff)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card e3">
  <div class="eyebrow">DATA EXPLORER</div>
  <h1 class="hero-h1">Full dataset, <em>open</em> and filterable.</h1>
  <p class="deck">Sort, filter and download the cleaned GRFC dataset underlying every chart —
  529 observations across 10 years, 7 regions and 74 countries.</p>
</div>""", unsafe_allow_html=True)

# ── Row count + CSV download ───────────────────────────────────────────────────
c_count, c_dl = st.columns([3, 1], gap="small")
with c_count:
    note = " · 2025 MYU — partial coverage" if year_sel == "2025" else ""
    st.markdown(
        f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:11px;'
        f'color:#8b93a1;padding:10px 0;">'
        f'<span style="color:#ffb877;font-size:16px;">{row_count}</span> rows matching filters{note}</div>',
        unsafe_allow_html=True,
    )

with c_dl:
    export_cols = {
        ISO: "iso", COUNTRY: "country", REGION: "region", YEAR: "year",
        P3N: "phase3plus_n", P3P: "phase3plus_pct", P5N: "phase5_n",
        D1: "primary_driver", D2: "secondary_driver", D3: "tertiary_driver",
    }
    export_df = dff[[c for c in export_cols if c in dff.columns]].rename(columns=export_cols)
    st.download_button(
        label="⬇ Download CSV",
        data=export_df.to_csv(index=False).encode("utf-8"),
        file_name="grfc_filtered.csv",
        mime="text/csv",
        width="stretch",
    )

# ── HTML data table (capped at 200 rows for performance) ──────────────────────
display_rows = dff.head(200)
max_p3n      = display_rows[P3N].max() if len(display_rows) else 1

rows_html = ""
for _, row in display_rows.iterrows():
    p3n_val  = row[P3N]
    p3p_val  = row[P3P]
    p5n_val  = row[P5N]
    d1_val   = row[D1]
    d2_raw   = row[D2]
    d3_raw   = row[D3]
    bar_w    = int(p3n_val / max_p3n * 100) if max_p3n > 0 else 0
    pill_htm = driver_pill_html(str(d1_val) if d1_val and str(d1_val) != "nan" else "")
    d2_txt   = str(d2_raw).split("/")[0] if d2_raw and str(d2_raw) != "nan" else "—"
    d3_txt   = str(d3_raw).split("/")[0] if d3_raw and str(d3_raw) != "nan" else "—"

    rows_html += f"""
<tr>
  <td class="cname">{row[COUNTRY]}</td>
  <td style="color:#8b93a1;font-size:11px;">{row[REGION]}</td>
  <td class="num">{int(row[YEAR])}</td>
  <td class="num">{p3n_val/1e6:.2f}</td>
  <td>
    <div style="display:flex;align-items:center;gap:7px;min-width:110px;">
      <div style="flex:1;height:4px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden;">
        <div style="width:{bar_w}%;height:100%;background:linear-gradient(90deg,#ff7a59,#ffb877);border-radius:3px;"></div>
      </div>
      <div style="font-family:'JetBrains Mono',monospace;font-size:10.5px;
                  min-width:30px;text-align:right;color:#f3f5f8;">{p3p_val:.0f}%</div>
    </div>
  </td>
  <td class="num">{p5n_val/1000:.0f}</td>
  <td>{pill_htm}</td>
  <td style="color:#8b93a1;font-size:11px;">{d2_txt}</td>
  <td style="color:#8b93a1;font-size:11px;">{d3_txt}</td>
</tr>"""

if row_count > 200:
    rows_html += f"""
<tr>
  <td colspan="9" style="text-align:center;padding:14px;font-family:'JetBrains Mono',monospace;
      font-size:11px;color:#5a6270;letter-spacing:.08em;">
    Showing first 200 of {row_count} rows — narrow your filters or download the full CSV.
  </td>
</tr>"""

st.markdown(f"""
<div class="glass-card" style="padding:0;overflow:hidden;">
<div class="dtable-wrap" style="max-height:580px;overflow-y:auto;border:none;border-radius:0;">
<table class="dtable">
  <thead><tr>
    <th>Country</th><th>Region</th>
    <th class="num">Year</th><th class="num">Phase 3+ (M)</th>
    <th>% pop.</th><th class="num">Phase 5 (K)</th>
    <th>Primary driver</th><th>Secondary</th><th>Tertiary</th>
  </tr></thead>
  <tbody>{rows_html}</tbody>
</table>
</div>
</div>""", unsafe_allow_html=True)

st.markdown(
    '<div style="font-family:\'JetBrains Mono\',monospace;font-size:10.5px;color:#5a6270;'
    'margin-top:8px;display:flex;justify-content:space-between;">'
    '<span>529 observations · FSIN/GRFC 2016–2025</span>'
    '<span>DATA · CC BY-NC 4.0</span></div>',
    unsafe_allow_html=True,
)

st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)
