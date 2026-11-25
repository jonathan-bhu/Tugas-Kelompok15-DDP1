import streamlit as st
from datetime import datetime

# ================= 1. PAGE CONFIG =================
st.set_page_config(
    page_title="FASILKOM SPACE — Campus Intelligence Platform",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= 2. STATE & DATA INITIALIZATION =================
if "page" not in st.session_state:
    st.session_state.page = "OVERVIEW"

if "ruang_kelas" not in st.session_state:
    st.session_state.ruang_kelas = {
        "D.401": {"building": "BUILDING D", "floor": "FLOOR 04", "capacity": 45, "status": "AVAILABLE", "source": "SIAK-NG Schedule • Free until 13:00"},
        "A.2301": {"building": "BUILDING A", "floor": "FLOOR 03", "capacity": 40, "status": "AVAILABLE", "source": "SIAK-NG Schedule • Free until 14:00"},
        "A.2302": {"building": "BUILDING A", "floor": "FLOOR 03", "capacity": 40, "status": "OCCUPIED", "source": "DDP1 Lecture (10:00 - 12:00)"},
        "B.2401": {"building": "BUILDING B", "floor": "FLOOR 04", "capacity": 50, "status": "AVAILABLE", "source": "SIAK-NG Schedule • Verified clear"},
        "B.2402": {"building": "BUILDING B", "floor": "FLOOR 04", "capacity": 45, "status": "OCCUPIED", "source": "Student report • Organization meeting"},
        "D.403": {"building": "BUILDING D", "floor": "FLOOR 04", "capacity": 60, "status": "AVAILABLE", "source": "SIAK-NG Schedule • Open study space"},
    }

if "area_umum" not in st.session_state:
    st.session_state.area_umum = {
        "KANTIN PACIL": {
            "category": "CANTEEN / CROWD MONITORING",
            "status": "MODERATE",
            "occupancy": 56,
            "note": "Several tables open along the west wing.",
            "updated": "2 mins ago • Crowdsourced"
        },
        "STUDENT LOUNGE": {
            "category": "STUDENT AREA / LIVE REPORT",
            "status": "FULL",
            "occupancy": 92,
            "note": "High density. Only isolated single seats remaining.",
            "updated": "6 mins ago • Crowdsourced"
        },
    }

def set_page(target: str):
    st.session_state.page = target

# Hitung telemetri real-time
cls_available = sum(1 for r in st.session_state.ruang_kelas.values() if r["status"] == "AVAILABLE")
cls_occupied = sum(1 for r in st.session_state.ruang_kelas.values() if r["status"] == "OCCUPIED")
pub_available = sum(1 for a in st.session_state.area_umum.values() if a["status"] == "AVAILABLE")
pub_moderate = sum(1 for a in st.session_state.area_umum.values() if a["status"] == "MODERATE")
pub_full = sum(1 for a in st.session_state.area_umum.values() if a["status"] == "FULL")

total_available = cls_available + pub_available
total_moderate = pub_moderate
total_occupied = cls_occupied + pub_full

active_nav_key = {
    "OVERVIEW": "nav_overview",
    "DIRECTORY": "nav_directory",
    "PUBLIC AREAS": "nav_public",
    "AI VISION": "nav_ai",
}[st.session_state.page]

# ================= 3. OBSIDIAN TECH CSS =================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {{
    --obsidian: #080B12;
    --graphite: #111827;
    --midnight: #1B2940;
    --royal: #2856A6;
    --crimson: #C43249;
    --cyan: #35C9E8;
    --ice: #E8EDF5;
    --steel: #8290A5;
    --border-subtle: rgba(130, 144, 165, 0.22);
}}

/* Clean Chrome */
[data-testid="stSidebar"], [data-testid="collapsedControl"], #MainMenu, footer {{
    display: none !important;
}}
header[data-testid="stHeader"] {{
    background: transparent !important;
    height: 0px !important;
}}
.block-container {{
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1220px !important;
}}

/* Base Obsidian Surface */
.stApp {{
    background-color: var(--obsidian) !important;
    background-image: radial-gradient(circle at 82% 0%, rgba(27, 41, 64, 0.35) 0%, transparent 45%) !important;
    color: var(--ice) !important;
    font-family: 'Inter', sans-serif !important;
}}

.stApp p, .stApp span, .stApp label, .stApp li {{
    color: var(--ice);
}}

/* Makara-inspired subtle top hairline (Royal Blue + Crimson) */
.makara-bar {{
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, #2856A6 0%, #2856A6 78%, #C43249 78%, #C43249 100%);
    margin-bottom: 1.25rem;
    opacity: 0.9;
}}

/* Brand Header */
.brand-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.15rem;
    letter-spacing: 0.12em;
    color: var(--ice);
    line-height: 1.2;
}}
.brand-meta {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    color: var(--steel);
    margin-top: 2px;
}}

/* System Active Status Pill */
.sys-active {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 0.42rem 0.85rem;
    background: rgba(17, 24, 39, 0.9);
    border: 1px solid rgba(53, 201, 232, 0.35);
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    color: var(--cyan);
    float: right;
}}
.sys-dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
}}

/* Top Navigation Buttons */
div[class*="st-key-nav_"] button {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    color: var(--steel) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.76rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.45rem 0.6rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}}
div[class*="st-key-nav_"] button:hover {{
    color: var(--ice) !important;
    background: rgba(27, 41, 64, 0.45) !important;
    border-color: rgba(40, 86, 166, 0.4) !important;
}}
div.st-key-{active_nav_key} button {{
    color: var(--ice) !important;
    background: var(--midnight) !important;
    border: 1px solid rgba(40, 86, 166, 0.75) !important;
    box-shadow: 0 0 14px rgba(40, 86, 166, 0.25) !important;
}}

/* Section Headers & Typography */
.eyebrow {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.16em;
    color: var(--cyan);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}}
.hero-heading {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: clamp(2rem, 3.6vw, 2.9rem);
    letter-spacing: -0.02em;
    color: var(--ice);
    line-height: 1.08;
    margin: 0;
}}
.hero-sub {{
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    color: var(--steel);
    margin-top: 0.55rem;
    letter-spacing: 0.01em;
}}
.section-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    letter-spacing: 0.16em;
    color: var(--steel);
    text-transform: uppercase;
}}

/* Control Panel KPI Cards */
.kpi-card {{
    background: var(--graphite);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    position: relative;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
.kpi-card:hover {{
    border-color: rgba(40, 86, 166, 0.65);
    box-shadow: 0 0 20px rgba(40, 86, 166, 0.14);
}}
.kpi-top {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}}
.kpi-label {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.74rem;
    letter-spacing: 0.14em;
    color: var(--steel);
}}
.kpi-value {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 2.6rem;
    line-height: 1;
    color: var(--ice);
}}
.kpi-meta {{
    font-size: 0.8rem;
    color: var(--steel);
    margin-top: 0.55rem;
}}
.indicator-bar {{
    height: 3px;
    width: 32px;
    border-radius: 2px;
}}

/* Directory Control Row Cards */
.dir-card {{
    background: var(--graphite);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.15rem 1.35rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s ease, background 0.2s ease;
}}
.dir-card:hover {{
    border-color: rgba(40, 86, 166, 0.7);
    background: #141D2E;
}}
.dir-name {{
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 1.15rem;
    letter-spacing: 0.03em;
    color: var(--ice);
}}
.dir-sub {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    color: var(--steel);
    margin-top: 3px;
}}

/* Status Tags (Restrained, Sharp) */
.tag {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    padding: 0.3rem 0.7rem;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}}
.tag-available {{
    background: rgba(53, 201, 232, 0.1);
    color: #35C9E8;
    border: 1px solid rgba(53, 201, 232, 0.38);
}}
.tag-moderate {{
    background: rgba(245, 158, 11, 0.1);
    color: #F5B041;
    border: 1px solid rgba(245, 158, 11, 0.38);
}}
.tag-occupied {{
    background: rgba(196, 50, 73, 0.14);
    color: #E55A70;
    border: 1px solid rgba(196, 50, 73, 0.45);
}}

/* Streamlit Bordered Containers -> Graphite Panels */
[data-testid="stVerticalBlockBorderWrapper"] {{
    background: var(--graphite) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    padding: 1.15rem 1.25rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}}
[data-testid="stVerticalBlockBorderWrapper"]:hover {{
    border-color: rgba(40, 86, 166, 0.65) !important;
    box-shadow: 0 0 18px rgba(40, 86, 166, 0.14) !important;
}}

/* Solid Cobalt Blue Primary Buttons */
div[class*="st-key-btn_"] button {{
    background-color: var(--royal) !important;
    color: var(--ice) !important;
    border: 1px solid #3567BD !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.5rem 1rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}}
div[class*="st-key-btn_"] button:hover {{
    background-color: #3164BE !important;
    box-shadow: 0 0 16px rgba(40, 86, 166, 0.55) !important;
}}

/* Ghost / Link Buttons (VIEW ALL ↗) */
div[class*="st-key-link_"] button {{
    background: transparent !important;
    color: var(--cyan) !important;
    border: 1px solid rgba(53, 201, 232, 0.35) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.74rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.35rem 0.75rem !important;
    float: right;
}}
div[class*="st-key-link_"] button:hover {{
    background: rgba(53, 201, 232, 0.1) !important;
    box-shadow: 0 0 12px rgba(53, 201, 232, 0.25) !important;
}}

/* AI Vision Banner & Tactical Grid Canvas */
.ai-banner {{
    background: linear-gradient(135deg, #111827 0%, #131F35 100%);
    border: 1px solid rgba(53, 201, 232, 0.32);
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
}}
.ai-viewport {{
    position: relative;
    min-height: 300px;
    background-color: #090E18;
    background-image:
        linear-gradient(rgba(53, 201, 232, 0.08) 1px, transparent 1px),
        linear-gradient(90deg, rgba(53, 201, 232, 0.08) 1px, transparent 1px);
    background-size: 28px 28px;
    border: 1px solid rgba(53, 201, 232, 0.35);
    border-radius: 8px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.hud-box {{
    border: 1px dashed rgba(53, 201, 232, 0.55);
    background: rgba(53, 201, 232, 0.05);
    border-radius: 6px;
    padding: 1.4rem;
    text-align: center;
    margin: 1.5rem auto;
    max-width: 440px;
}}

/* Telemetry Occupancy Bar */
.occ-track {{
    width: 100%;
    height: 7px;
    background: var(--midnight);
    border-radius: 4px;
    overflow: hidden;
    margin: 0.75rem 0;
}}
.occ-fill {{
    height: 100%;
    border-radius: 4px;
}}

/* Dark Inputs & Controls */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {{
    background-color: var(--graphite) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--ice) !important;
}}
input {{
    color: var(--ice) !important;
}}
[data-testid="stFileUploaderDropzone"] {{
    background-color: #0B101C !important;
    border: 1px dashed rgba(53, 201, 232, 0.4) !important;
    border-radius: 8px !important;
}}

/* Footer */
.sys-footer {{
    margin-top: 3.5rem;
    padding-top: 1.25rem;
    border-top: 1px solid var(--border-subtle);
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    color: var(--steel);
}}
</style>
""", unsafe_allow_html=True)

# ================= 4. TOP COMMAND BAR =================
st.markdown('<div class="makara-bar"></div>', unsafe_allow_html=True)

h_brand, h_nav1, h_nav2, h_nav3, h_nav4, h_status = st.columns([2.4, 1.0, 1.05, 1.25, 1.05, 1.75])
with h_brand:
    st.markdown("""
<div class="brand-title">FASILKOM SPACE</div>
<div class="brand-meta">INTELLIGENCE PLATFORM / 001</div>
""", unsafe_allow_html=True)
with h_nav1:
    st.button("OVERVIEW", key="nav_overview", on_click=set_page, args=("OVERVIEW",))
with h_nav2:
    st.button("DIRECTORY", key="nav_directory", on_click=set_page, args=("DIRECTORY",))
with h_nav3:
    st.button("PUBLIC AREAS", key="nav_public", on_click=set_page, args=("PUBLIC AREAS",))
with h_nav4:
    st.button("AI VISION", key="nav_ai", on_click=set_page, args=("AI VISION",))
with h_status:
    st.markdown("""
<div class="sys-active">
<span class="sys-dot"></span>SYSTEM ACTIVE
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border:none; border-top:1px solid rgba(130,144,165,0.18); margin:0.9rem 0 2rem 0;'>", unsafe_allow_html=True)

# ================= PAGE 1: CAMPUS OVERVIEW =================
if st.session_state.page == "OVERVIEW":
    st.markdown("""
<div class="eyebrow">CAMPUS OVERVIEW</div>
<h1 class="hero-heading">Space Intelligence.</h1>
<div class="hero-sub">Monitor. Discover. Navigate.</div>
""", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # 3 Telemetry KPI Cards
    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown(f"""
<div class="kpi-card">
<div class="kpi-top">
<span class="kpi-label">AVAILABLE</span>
<span class="indicator-bar" style="background:#35C9E8;"></span>
</div>
<div class="kpi-value">{total_available:02d}</div>
<div class="kpi-meta">Spaces open for study or sessions</div>
</div>
""", unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
<div class="kpi-card">
<div class="kpi-top">
<span class="kpi-label">MODERATE</span>
<span class="indicator-bar" style="background:#F5B041;"></span>
</div>
<div class="kpi-value">{total_moderate:02d}</div>
<div class="kpi-meta">Public areas with partial capacity</div>
</div>
""", unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
<div class="kpi-card">
<div class="kpi-top">
<span class="kpi-label">OCCUPIED</span>
<span class="indicator-bar" style="background:#C43249;"></span>
</div>
<div class="kpi-value">{total_occupied:02d}</div>
<div class="kpi-meta">Active classes or full public zones</div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    st.write("")

    # Space Directory Preview Header
    d_left, d_right = st.columns([4, 1])
    with d_left:
        st.markdown('<div class="section-label" style="padding-top:0.5rem;">SPACE DIRECTORY // LIVE FEED</div>', unsafe_allow_html=True)
    with d_right:
        st.button("VIEW ALL ↗", key="link_view_all", on_click=set_page, args=("DIRECTORY",))

    # Highlighted Directory Rows (Matching Art Direction)
    r_d401 = st.session_state.ruang_kelas["D.401"]
    tag_d401 = "tag-available" if r_d401["status"] == "AVAILABLE" else "tag-occupied"
    kantin = st.session_state.area_umum["KANTIN PACIL"]
    lounge = st.session_state.area_umum["STUDENT LOUNGE"]
    pub_tag = {"AVAILABLE": "tag-available", "MODERATE": "tag-moderate", "FULL": "tag-occupied"}

    st.markdown(f"""
<div class="dir-card">
<div>
<div class="dir-name">ROOM D.401</div>
<div class="dir-sub">{r_d401['building']} / {r_d401['floor']} · CAP {r_d401['capacity']}</div>
</div>
<span class="tag {tag_d401}">● {r_d401['status']}</span>
</div>

<div class="dir-card">
<div>
<div class="dir-name">KANTIN PACIL</div>
<div class="dir-sub">{kantin['category']} · {kantin['occupancy']}% DENSITY</div>
</div>
<span class="tag {pub_tag[kantin['status']]}">● {kantin['status']}</span>
</div>

<div class="dir-card">
<div>
<div class="dir-name">STUDENT LOUNGE</div>
<div class="dir-sub">{lounge['category']} · {lounge['occupancy']}% DENSITY</div>
</div>
<span class="tag {pub_tag[lounge['status']]}">● {lounge['status']}</span>
</div>
""", unsafe_allow_html=True)

    # AI Vision System Banner
    st.markdown("""
<div class="ai-banner">
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
<div>
<div class="eyebrow" style="margin-bottom:4px;">AI VISION SYSTEM</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.25rem; font-weight:700; color:#E8EDF5;">
YOLOv8 DETECTION MODULE
</div>
<div style="font-size:0.88rem; color:#8290A5; margin-top:4px;">
Real-time occupancy analysis / Prototype environment
</div>
</div>
<span class="tag tag-available">● ACTIVE</span>
</div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    _, ai_cta = st.columns([4, 1.3])
    with ai_cta:
        st.button("LAUNCH AI MODULE ↗", key="link_launch_ai", on_click=set_page, args=("AI VISION",))

# ================= PAGE 2: SPACE DIRECTORY (CLASSROOMS) =================
elif st.session_state.page == "DIRECTORY":
    st.markdown("""
<div class="eyebrow">SPACE DIRECTORY // CLASSROOMS</div>
<h1 class="hero-heading">Room Control Panel.</h1>
<div class="hero-sub">Static SIAK-NG schedule synchronized with real-time student verification.</div>
""", unsafe_allow_html=True)

    st.write("")

    f1, f2, f3 = st.columns([2.2, 1.4, 1.2])
    with f1:
        query = st.text_input("Search Room ID", placeholder="e.g. D.401, A.2301, B.2402")
    with f2:
        building_filter = st.selectbox("Building", ["ALL BUILDINGS", "BUILDING A", "BUILDING B", "BUILDING D"])
    with f3:
        st.write("")
        st.write("")
        only_avail = st.toggle("Available only", value=False)

    st.write("")

    filtered = {}
    for code, info in st.session_state.ruang_kelas.items():
        if query and query.lower() not in code.lower() and query.lower() not in info["building"].lower():
            continue
        if building_filter != "ALL BUILDINGS" and info["building"] != building_filter:
            continue
        if only_avail and info["status"] != "AVAILABLE":
            continue
        filtered[code] = info

    if not filtered:
        st.info("No spaces match the active filter criteria.")
    else:
        cols = st.columns(3)
        for idx, (code, info) in enumerate(filtered.items()):
            with cols[idx % 3]:
                with st.container(border=True):
                    tag_cls = "tag-available" if info["status"] == "AVAILABLE" else "tag-occupied"
                    st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.8rem;">
<span class="dir-sub" style="margin:0;">{info['building']} / {info['floor']}</span>
<span class="tag {tag_cls}">● {info['status']}</span>
</div>
<div class="dir-name" style="font-size:1.35rem; margin-bottom:0.25rem;">ROOM {code}</div>
<div style="font-size:0.82rem; color:#8290A5; margin-bottom:0.85rem; min-height:38px;">
Capacity {info['capacity']} · {info['source']}
</div>
""", unsafe_allow_html=True)

                    btn_label = "Report as Occupied" if info["status"] == "AVAILABLE" else "Report as Available"
                    if st.button(btn_label, key=f"btn_room_{code}"):
                        new_status = "OCCUPIED" if info["status"] == "AVAILABLE" else "AVAILABLE"
                        now_str = datetime.now().strftime("%H:%M")
                        st.session_state.ruang_kelas[code]["status"] = new_status
                        st.session_state.ruang_kelas[code]["source"] = f"Verified by student at {now_str}"
                        st.toast(f"ROOM {code} updated to {new_status}", icon="✅")
                        st.rerun()

# ================= PAGE 3: PUBLIC AREAS =================
elif st.session_state.page == "PUBLIC AREAS":
    st.markdown("""
<div class="eyebrow">PUBLIC ZONES // CROWD TELEMETRY</div>
<h1 class="hero-heading">Canteen & Lounge.</h1>
<div class="hero-sub">Live crowd density reports submitted by Fasilkom UI students.</div>
""", unsafe_allow_html=True)

    st.write("")
    p_cols = st.columns(2)

    color_map = {
        "AVAILABLE": ("tag-available", "#35C9E8"),
        "MODERATE": ("tag-moderate", "#F5B041"),
        "FULL": ("tag-occupied", "#C43249"),
    }

    for idx, (name, info) in enumerate(st.session_state.area_umum.items()):
        with p_cols[idx]:
            with st.container(border=True):
                t_cls, bar_color = color_map[info["status"]]
                st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
<span class="dir-sub" style="margin:0;">{info['category']}</span>
<span class="tag {t_cls}">● {info['status']}</span>
</div>
<div class="dir-name" style="font-size:1.45rem;">{name}</div>
<div class="occ-track">
<div class="occ-fill" style="width:{info['occupancy']}%; background:{bar_color};"></div>
</div>
<div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:0.74rem; color:#8290A5; margin-bottom:0.8rem;">
<span>OCCUPANCY ESTIMATE</span>
<span style="color:#E8EDF5;">{info['occupancy']}%</span>
</div>
<div style="font-size:0.88rem; color:#E8EDF5; margin-bottom:0.35rem;">{info['note']}</div>
<div class="dir-sub" style="margin-bottom:1rem;">LAST SYNC // {info['updated'].upper()}</div>
""", unsafe_allow_html=True)

                selected = st.radio(
                    f"Update status for {name}",
                    ["AVAILABLE", "MODERATE", "FULL"],
                    index=["AVAILABLE", "MODERATE", "FULL"].index(info["status"]),
                    horizontal=True,
                    key=f"rad_{name}"
                )

                if st.button(f"Submit {name.title()} Telemetry", key=f"btn_pub_{name}"):
                    now_str = datetime.now().strftime("%H:%M")
                    presets = {
                        "AVAILABLE": (22, "Low density. Plenty of open tables available."),
                        "MODERATE": (58, "Moderate traffic. Several tables still available."),
                        "FULL": (92, "Near peak capacity. Difficult to find seating.")
                    }
                    occ, note = presets[selected]
                    st.session_state.area_umum[name].update({
                        "status": selected,
                        "occupancy": occ,
                        "note": note,
                        "updated": f"{now_str} • Crowdsourced"
                    })
                    st.toast(f"{name} status updated to {selected}", icon="📡")
                    st.rerun()

# ================= PAGE 4: AI VISION COMMAND CENTER =================
elif st.session_state.page == "AI VISION":
    st.markdown("""
<div class="eyebrow">COMPUTER VISION // YOLOv8 MODULE</div>
<h1 class="hero-heading">AI Vision Monitoring.</h1>
<div class="hero-sub">Automated person detection pipeline for real-time crowd density classification.</div>
""", unsafe_allow_html=True)

    st.write("")
    v_left, v_right = st.columns([2.1, 1])

    with v_left:
        st.markdown("""
<div class="ai-viewport">
<div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#35C9E8;">
<span>CAM_01 // KANTIN_PACIL_FEED</span>
<span>GRID OVERLAY: ON</span>
</div>
<div class="hud-box">
<div style="font-family:'JetBrains Mono',monospace; font-size:0.76rem; color:#35C9E8; letter-spacing:0.14em; margin-bottom:0.5rem;">
[ AWAITING VISUAL INPUT ]
</div>
<div style="font-size:0.88rem; color:#8290A5;">
Upload a snapshot or video frame below to run YOLOv8 bounding-box detection and compute live crowd status.
</div>
</div>
<div style="display:flex; justify-content:space-between; font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#8290A5;">
<span>MODEL: YOLOv8n (READY)</span>
<span>CLASS FILTER: PERSON [0]</span>
<span>RES: AUTO</span>
</div>
</div>
""", unsafe_allow_html=True)

        st.write("")
        st.file_uploader(
            "Input Surveillance Frame / Simulation Video (Activates on YOLOv8 Integration)",
            type=["jpg", "jpeg", "png", "mp4"],
            disabled=True
        )

    with v_right:
        with st.container(border=True):
            st.markdown("""
<div class="section-label" style="margin-bottom:1rem;">INFERENCE TELEMETRY</div>
<div style="margin-bottom:1.1rem;">
<div class="dir-sub">DETECTED SUBJECTS</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:2.4rem; font-weight:700; color:#35C9E8; line-height:1.1;">--</div>
</div>
<div style="margin-bottom:1.1rem;">
<div class="dir-sub">COMPUTED STATUS</div>
<div style="font-family:'Space Grotesk',sans-serif; font-size:1.25rem; font-weight:600; color:#E8EDF5; margin-top:4px;">STANDBY</div>
</div>
<div style="border-top:1px solid rgba(130,144,165,0.2); padding-top:0.9rem; font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:#8290A5; line-height:1.8;">
THRESHOLD: <10 AVAILABLE<br>
THRESHOLD: 10-25 MODERATE<br>
THRESHOLD: >25 FULL<br>
ENGINE: ULTRALYTICS + OPENCV
</div>
""", unsafe_allow_html=True)

# ================= 5. FOOTER =================
st.markdown("""
<div class="sys-footer">
<span>FASILKOM SPACE · CAMPUS INTELLIGENCE SYSTEM</span>
<span>KELOMPOK 15 · DDP1 FASILKOM UI</span>
</div>
""", unsafe_allow_html=True)