"""Tab 6 — About · Dashboard context, dataset description, and developer info."""

import streamlit as st

st.set_page_config(
    page_title="Hunger Atlas · About",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card e3">
  <div class="eyebrow">ABOUT · HUNGER ATLAS</div>
  <h1 class="hero-h1">About this <em>dashboard</em></h1>
  <p class="deck">Overview, data sources, and key insights behind the analysis.</p>
</div>""", unsafe_allow_html=True)

# ── About the Dashboard ───────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">💬 Dashboard</h2>
  <p style="color:#c3c8d1;font-size:13px;line-height:1.8;">
    This dashboard explores the <b>global food crisis</b> using data from the
    Global Report on Food Crises (GRFC). It highlights trends in food insecurity
    and shows how different factors impact populations across countries.
  </p>
  <p style="color:#c3c8d1;font-size:13px;line-height:1.8;">
    Users can interact with the data to identify patterns, compare regions,
    and understand the main drivers of food insecurity over time.
  </p>
</div>""", unsafe_allow_html=True)

# ── Key Features ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">🔍 Key Features</h2>
  <div style="color:#c3c8d1;font-size:13px;line-height:1.9;">
    <p><b style="color:#ff7a59;">Overview</b> — Key indicators and global trends.</p>
    <p><b style="color:#ff7a59;">Geography</b> — Regional comparison and country-level insights.</p>
    <p><b style="color:#ff7a59;">Trends</b> — Time-based analysis of food insecurity.</p>
    <p><b style="color:#ff7a59;">Drivers</b> — Impact of conflict, climate, and economic shocks.</p>
    <p><b style="color:#ff7a59;">Data Explorer</b> — Explore and filter the dataset.</p>
  </div>
</div>""", unsafe_allow_html=True)

# ── Data Source ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">📦 Data Source</h2>
  <div style="color:#c3c8d1;font-size:13px;line-height:1.9;">
    <p><b>Dataset:</b> Global Report on Food Crises (GRFC)</p>
    <p><b>Source:</b> Food Security Information Network (FSIN)</p>
    <p><b>Coverage:</b> 74 countries (2016–2025)</p>
    <p>
      Data has been cleaned and prepared to ensure consistency and accuracy
      for analysis and visualization.
    </p>
  </div>
</div>""", unsafe_allow_html=True)

# ── Dataset Column Descriptions ───────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">🧾 Dataset Overview</h2>
  <div style="color:#c3c8d1;font-size:12px;line-height:1.9;font-family:'JetBrains Mono',monospace;">
    <p><b>Country</b> — Country name</p>
    <p><b>Region</b> — Geographic region</p>
    <p><b>Year</b> — Reporting year</p>
    <p><b>Population (Phase 3+)</b> — People facing food crisis</p>
    <p><b>Food insecurity (%)</b> — Percentage affected</p>
    <p><b>Drivers</b> — Main causes (conflict, climate, economic)</p>
  </div>
</div>""", unsafe_allow_html=True)

# ── About the Developer ──────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">👤 About the Developer</h2>
  <div style="color:#c3c8d1;font-size:13px;line-height:1.9;">
    <p>
I am <b style="color:#f3f5f8;">Sumaiya Rizan</b>, a Business Data Analytics student at the 
University of Westminster. I have a strong interest in data visualization 
and using analytics to turn complex data into meaningful insights. This project reflects 
my ability to design interactive dashboards and communicate data clearly.
</p>
  </div>
</div>""", unsafe_allow_html=True)

# ── Technology Stack ─────────────────────────────────────────────────────────
st.markdown("""
<div class="glass-card">
  <h2 class="section-h2">🛠️ Technology Stack</h2>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:10px;">
    <span class="pill conflict" style="font-size:12px;padding:6px 14px;">Streamlit</span>
    <span class="pill weather" style="font-size:12px;padding:6px 14px;">Plotly</span>
    <span class="pill economic" style="font-size:12px;padding:6px 14px;">Pandas</span>
    <span style="display:inline-block;padding:6px 14px;background:rgba(255,255,255,0.08);
           border:1px solid rgba(255,255,255,0.12);border-radius:20px;
           font-size:12px;color:#c3c8d1;">Python</span>
    <span style="display:inline-block;padding:6px 14px;background:rgba(255,255,255,0.08);
           border:1px solid rgba(255,255,255,0.12);border-radius:20px;
           font-size:12px;color:#c3c8d1;">GitHub</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── Source footer ─────────────────────────────────────────────────────────────
from utils.data_loader import SOURCE_FOOTER
st.markdown(SOURCE_FOOTER, unsafe_allow_html=True)
