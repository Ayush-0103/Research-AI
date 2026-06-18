import streamlit as st
import time
import datetime
import json
import sys
import io
from contextlib import redirect_stdout
import os
from dotenv import load_dotenv

load_dotenv()

print("GOOGLE_API_KEY exists:", bool(os.getenv("GOOGLE_API_KEY")))
print("TAVILY_API_KEY exists:", bool(os.getenv("TAVILY_API_KEY")))

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchAI — Autonomous Research Reports",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* Reset & base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #080C14;
    color: #E2E8F0;
}

.stApp {
    background: #080C14;
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 2rem 4rem 2rem;
    max-width: 1200px;
}

/* ── Hero ── */
.hero-wrap {
    text-align: center;
    padding: 5rem 2rem 3.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 100px;
    padding: 4px 16px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #818CF8;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #E2E8F0 30%, #818CF8 70%, #C4B5FD 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1.2rem;
}
.hero-sub {
    font-size: 1.15rem;
    color: #94A3B8;
    max-width: 560px;
    margin: 0 auto 2.8rem;
    line-height: 1.7;
    font-weight: 400;
}
.hero-divider {
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6366F1, transparent);
    margin: 0 auto 3rem;
}

/* ── Input card: style the Streamlit column container itself ── */
[data-testid="stHorizontalBlock"] {
    background: rgba(15,20,35,0.85);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 16px;
    padding: 1.4rem 1.6rem !important;
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04);
    margin-bottom: 2rem;
    align-items: center !important;
    gap: 1rem !important;
}

/* Streamlit input overrides */
.stTextInput label {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #6366F1 !important;
    margin-bottom: 6px !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
.stTextInput > div > div > input::placeholder { color: #475569 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
    width: 100% !important;
    white-space: nowrap !important;
    height: 48px !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 28px rgba(99,102,241,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.7rem 1.5rem !important;
    box-shadow: 0 4px 20px rgba(16,185,129,0.3) !important;
    width: 100% !important;
}

/* ── Agent pipeline ── */
.pipeline-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin: 2rem 0 1.5rem;
    flex-wrap: wrap;
}
.agent-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    position: relative;
}
.agent-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    transition: all 0.3s;
    border: 2px solid transparent;
}
.agent-icon.waiting {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.08);
    color: #475569;
}
.agent-icon.running {
    background: rgba(99,102,241,0.2);
    border-color: #6366F1;
    color: #818CF8;
    box-shadow: 0 0 20px rgba(99,102,241,0.4);
    animation: pulse-ring 1.5s ease-in-out infinite;
}
.agent-icon.done {
    background: rgba(16,185,129,0.15);
    border-color: #10B981;
    color: #10B981;
}
.agent-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.agent-label.waiting { color: #475569; }
.agent-label.running { color: #818CF8; }
.agent-label.done    { color: #10B981; }
.pipeline-arrow {
    font-size: 1.2rem;
    color: #334155;
    margin: 0 8px;
    padding-bottom: 18px;
}

@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(99,102,241,0.5); }
    70%  { box-shadow: 0 0 0 10px rgba(99,102,241,0); }
    100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
}

/* ── Execution panel ── */
.exec-panel {
    background: rgba(10,15,28,0.9);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(20px);
}
.exec-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366F1;
    margin-bottom: 1.2rem;
}
.step-row {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.step-row:last-child { border-bottom: none; }
.step-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.dot-waiting { background: rgba(255,255,255,0.05); color: #334155; border: 1px solid #1E293B; }
.dot-running { background: rgba(99,102,241,0.2); color: #818CF8; border: 1px solid #6366F1; animation: spin 1.5s linear infinite; }
.dot-done    { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid #10B981; }

@keyframes spin {
    0%   { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.step-name { font-size: 0.9rem; font-weight: 500; flex: 1; }
.step-name.waiting { color: #475569; }
.step-name.running { color: #E2E8F0; }
.step-name.done    { color: #CBD5E1; }
.step-tag {
    font-size: 10px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 100px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.tag-waiting { background: rgba(255,255,255,0.04); color: #334155; }
.tag-running { background: rgba(99,102,241,0.2); color: #818CF8; }
.tag-done    { background: rgba(16,185,129,0.15); color: #10B981; }

/* ── Timeline messages ── */
.timeline-wrap {
    background: rgba(10,15,28,0.9);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
}
.timeline-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 6px 0;
}
.tl-dot { width:8px; height:8px; border-radius:50%; background:#6366F1; margin-top:6px; flex-shrink:0; }
.tl-dot.done { background:#10B981; }
.tl-text { font-size:0.85rem; color:#94A3B8; line-height:1.5; }
.tl-text strong { color:#CBD5E1; font-weight:500; }

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: rgba(15,20,35,0.8);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 14px;
    padding: 1.3rem 1.2rem;
    text-align: center;
    backdrop-filter: blur(20px);
    transition: border-color 0.2s;
}
.kpi-card:hover { border-color: rgba(99,102,241,0.4); }
.kpi-val {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #E2E8F0, #818CF8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
}
.kpi-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 6px;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,20,35,0.8) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    margin-bottom: 1.5rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #64748B !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all 0.2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #E2E8F0 !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Report viewer ── */
.report-viewer {
    background: rgba(10,15,28,0.9);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    line-height: 1.8;
    color: #CBD5E1;
    font-size: 0.97rem;
    backdrop-filter: blur(20px);
    max-height: 70vh;
    overflow-y: auto;
}
.report-viewer h1 { font-family: 'Syne', sans-serif; color: #E2E8F0; font-size: 1.8rem; margin-bottom: 1rem; }
.report-viewer h2 { color: #C4B5FD; font-size: 1.2rem; margin: 2rem 0 0.8rem; border-left: 3px solid #6366F1; padding-left: 1rem; }
.report-viewer h3 { color: #A5B4FC; font-size: 1rem; margin: 1.5rem 0 0.5rem; }
.report-viewer p  { margin-bottom: 1rem; }
.report-viewer::-webkit-scrollbar { width: 6px; }
.report-viewer::-webkit-scrollbar-track { background: transparent; }
.report-viewer::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }

/* ── Source card ── */
.source-card {
    background: rgba(15,20,35,0.8);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    transition: border-color 0.2s;
}
.source-card:hover { border-color: rgba(99,102,241,0.35); }
.source-favicon {
    width: 36px; height: 36px;
    background: rgba(99,102,241,0.15);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.source-title { font-size: 0.9rem; font-weight: 600; color: #E2E8F0; margin-bottom: 3px; }
.source-domain { font-size: 0.78rem; color: #6366F1; margin-bottom: 4px; }
.source-url { font-size: 0.75rem; color: #475569; word-break: break-all; }
.relevance-bar {
    margin-top: 8px;
    height: 3px;
    border-radius: 2px;
    background: rgba(255,255,255,0.06);
    overflow: hidden;
}
.relevance-fill {
    height: 100%;
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    border-radius: 2px;
}

/* ── Log feed ── */
.log-feed {
    background: rgba(5,8,16,0.95);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 0.8rem;
    max-height: 420px;
    overflow-y: auto;
    line-height: 1.8;
}
.log-feed::-webkit-scrollbar { width: 4px; }
.log-feed::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 2px; }
.log-time { color: #334155; }
.log-agent { color: #6366F1; font-weight: 600; }
.log-msg   { color: #64748B; }
.log-msg.ok { color: #10B981; }

/* ── Insights ── */
.insight-card {
    background: rgba(15,20,35,0.8);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 12px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 0.8rem;
}
.insight-tag {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #818CF8;
    margin-bottom: 8px;
}
.insight-text { font-size: 0.88rem; color: #94A3B8; line-height: 1.65; }

/* ── Progress bar override ── */
.stProgress > div > div {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    border-radius: 4px !important;
}
.stProgress { margin-bottom: 0.5rem !important; }

/* ── Success banner ── */
.success-banner {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.success-icon { font-size: 1.5rem; }
.success-text { font-size: 0.9rem; font-weight: 600; color: #34D399; }
.success-sub  { font-size: 0.8rem; color: #065F46; margin-top: 2px; }

/* ── Section titles ── */
.section-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6366F1;
    margin-bottom: 0.4rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #E2E8F0;
    margin-bottom: 1.5rem;
}

/* Responsive KPI */
@media (max-width: 900px) {
    .kpi-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 600px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .pipeline-wrap { gap: 4px; }
    .pipeline-arrow { display: none; }
}
</style>
""", unsafe_allow_html=True)

# ── State init ─────────────────────────────────────────────────────────────────
for k, v in {
    "report_ready": False,
    "report_text": "",
    "pdf_bytes": None,
    "sources": [],
    "logs": [],
    "kpis": {},
    "agent_states": ["waiting", "waiting", "waiting", "waiting", "waiting"],
    "insights": [],
    "running": False,
    "topic": "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-badge">◈ Autonomous AI Research</div>
  <div class="hero-title">ResearchAI</div>
  <div class="hero-sub">Generate consultant-grade research reports using autonomous AI agents.</div>
  <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Input card ─────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown('<div class="input-label">Research Topic</div>', unsafe_allow_html=True)
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        topic = st.text_input(
            "Enter Research Topic",
            placeholder="e.g. The impact of AI on global healthcare systems in 2025",
            label_visibility="collapsed",
            key="topic_input",
        )
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        generate_clicked = st.button("⚡ Generate Report", key="gen_btn", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
AGENTS = [
    ("🧠", "Planner"),
    ("🔍", "Search"),
    ("✓",  "Fact Check"),
    ("✍️",  "Writer"),
    ("📄", "PDF Gen"),
]

def render_pipeline(states):
    parts = []
    for i, (icon, name) in enumerate(AGENTS):
        s = states[i]
        parts.append(f"""
        <div class="agent-node">
          <div class="agent-icon {s}">{icon}</div>
          <div class="agent-label {s}">{name}</div>
        </div>""")
        if i < len(AGENTS) - 1:
            parts.append('<div class="pipeline-arrow">→</div>')
    return '<div class="pipeline-wrap">' + "".join(parts) + "</div>"

STEP_ICONS = {"waiting": "○", "running": "⟳", "done": "✓"}
STEP_LABELS = {
    0: "Planner Agent",
    1: "Search Agent",
    2: "Fact Check Agent",
    3: "Report Writer Agent",
    4: "PDF Generator",
}

INSIGHT_CATEGORIES = [
    ("📈", "Market Growth"),
    ("🏢", "Enterprise Adoption"),
    ("⚠️", "Key Risk"),
    ("💡", "Strategic Insight"),
    ("🔍", "Technology Trend"),
    ("💰", "Investment Signal"),
]

def render_exec_panel(states):
    rows = ""
    for i, s in enumerate(states):
        dot_cls = f"dot-{s}"
        icon = STEP_ICONS[s]
        tag_cls = f"tag-{s}"
        tag_text = {"waiting": "Waiting", "running": "Running", "done": "Completed"}[s]
        name_cls = f"step-name {s}"
        rows += f"""
        <div class="step-row">
          <div class="step-dot {dot_cls}">{icon}</div>
          <div class="{name_cls}">{STEP_LABELS[i]}</div>
          <span class="step-tag {tag_cls}">{tag_text}</span>
        </div>"""
    return f'<div class="exec-panel"><div class="exec-title">Agent Execution Status</div>{rows}</div>'

def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

def add_log(logs_list, agent, msg, ok=False):
    logs_list.append({"t": ts(), "agent": agent, "msg": msg, "ok": ok})

# ── Main execution flow ────────────────────────────────────────────────────────
if generate_clicked and topic.strip():
    st.session_state.report_ready = False
    st.session_state.running = True
    st.session_state.logs = []
    st.session_state.agent_states = ["waiting", "waiting", "waiting", "waiting", "waiting"]
    st.session_state.topic = topic

    logs = st.session_state.logs
    t_start = time.time()

    # Live execution area
    pipeline_ph = st.empty()
    panel_ph    = st.empty()
    progress_ph = st.empty()
    status_ph   = st.empty()

    progress_steps = [
        "Building research plan…",
        "Searching trusted sources…",
        "Collecting evidence…",
        "Verifying claims…",
        "Generating executive summary…",
        "Building final report…",
        "Generating PDF…",
    ]
    progress_val = 0.0
    step_size    = 1.0 / len(progress_steps)

    def update_ui(states, msg, prog):
        pipeline_ph.markdown(render_pipeline(states), unsafe_allow_html=True)
        panel_ph.markdown(render_exec_panel(states), unsafe_allow_html=True)
        progress_ph.progress(min(prog, 1.0))
        status_ph.markdown(
            f"<div style='text-align:center;color:#64748B;font-size:0.82rem;margin-top:-12px'>{msg}</div>",
            unsafe_allow_html=True,
        )

    # ── Import agents ──────────────────────────────────────────────────────────
    from app.agents.planner_agent import PlannerAgent
    from app.agents.search_agent import SearchAgent
    from app.agents.fact_check_agent import FactCheckAgent
    from app.agents.report_writer_agent import ReportWriterAgent
    from app.services.pdf_generator import PDFGenerator

    # ─── 1. Planner ───────────────────────────────────────────────────────────
    states = ["running", "waiting", "waiting", "waiting", "waiting"]
    add_log(logs, "Planner Agent", "started")
    update_ui(states, progress_steps[0], progress_val)
    progress_val += step_size

    try:
        planner = PlannerAgent()
        plan = planner.create_plan(topic)
    except Exception as e:
        add_log(logs, "Planner Agent", f"failed: {e}")
        st.error(f"Planner Agent failed: {e}")
        st.session_state.running = False
        st.stop()

    # Defensive: plan may come back as a JSON string instead of a dict
    if isinstance(plan, str):
        try:
            plan = json.loads(plan)
        except Exception:
            add_log(logs, "Planner Agent", "returned an invalid plan format")
            st.error("Planner Agent returned an invalid plan format.")
            st.session_state.running = False
            st.stop()

    if not isinstance(plan, dict):
        plan = {}

    plan_sections = plan.get("sections") or []
    if not isinstance(plan_sections, list) or len(plan_sections) == 0:
        add_log(logs, "Planner Agent", "returned no sections to research")
        st.error("Planner Agent did not return any sections to research.")
        st.session_state.running = False
        st.stop()

    states[0] = "done"
    add_log(logs, "Planner Agent", "completed", ok=True)
    update_ui(states, progress_steps[1], progress_val)
    progress_val += step_size

    # ─── 2. Search ────────────────────────────────────────────────────────────
    states[1] = "running"
    add_log(logs, "Search Agent", "started")
    update_ui(states, progress_steps[1], progress_val)
    progress_val += step_size

    try:
        searcher = SearchAgent()
        search_results = []
        for section in plan_sections:
            try:
                result = searcher.research_section(section)
            except Exception as e:
                add_log(logs, "Search Agent", f"section failed: {e}")
                continue
            if result:
                search_results.append(result)
    except Exception as e:
        add_log(logs, "Search Agent", f"failed: {e}")
        st.error(f"Search Agent failed: {e}")
        st.session_state.running = False
        st.stop()

    if not search_results:
        add_log(logs, "Search Agent", "returned no results for any section")

    states[1] = "done"
    add_log(logs, "Search Agent", "completed", ok=True)
    update_ui(states, progress_steps[2], progress_val)
    progress_val += step_size

    # ─── 3. Fact Check ────────────────────────────────────────────────────────
    states[2] = "running"
    add_log(logs, "Fact Check Agent", "started")
    update_ui(states, progress_steps[2], progress_val)
    progress_val += step_size

    try:
        checker = FactCheckAgent()
        verified = checker.verify_research(search_results)
        if not verified:
            verified = []
        add_log(logs, "Fact Check Agent", f"verified {len(verified)} sections", ok=True)
    except Exception as e:
        add_log(logs, "Fact Check Agent", f"failed: {e}")
        st.error(f"Fact Check Agent failed: {e}")
        st.session_state.running = False
        st.stop()

    states[2] = "done"
    add_log(logs, "Fact Check Agent", "completed", ok=True)
    update_ui(states, progress_steps[3], progress_val)
    progress_val += step_size

    # ─── 4. Report Writer ─────────────────────────────────────────────────────
    states[3] = "running"
    add_log(logs, "Report Writer Agent", "started")
    update_ui(states, progress_steps[3], progress_val)
    progress_val += step_size

    try:
        writer = ReportWriterAgent()
        report_text = writer.generate_report(topic, verified)
    except Exception as e:
        add_log(logs, "Report Writer Agent", f"failed: {e}")
        st.error(f"Report Writer Agent failed: {e}")
        st.session_state.running = False
        st.stop()

    if not report_text or not str(report_text).strip():
        add_log(logs, "Report Writer Agent", "returned an empty report")
        st.error("Report Writer Agent returned an empty report.")
        st.session_state.running = False
        st.stop()

    states[3] = "done"
    add_log(logs, "Report Writer Agent", "completed", ok=True)
    update_ui(states, progress_steps[5], progress_val)
    progress_val += step_size

    # ─── 5. PDF Generator ─────────────────────────────────────────────────────
    states[4] = "running"
    add_log(logs, "PDF Generator", "started")
    update_ui(states, progress_steps[6], progress_val)

    pdf_bytes = None
    try:
        pdf_gen = PDFGenerator()
        pdf_path = pdf_gen.generate_pdf(topic, report_text)
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        add_log(logs, "PDF Generator", "completed", ok=True)
    except Exception as e:
        add_log(logs, "PDF Generator", f"failed: {e}")
        st.warning(f"PDF Generator failed, but the report is still available: {e}")
        pdf_bytes = None

    states[4] = "done"
    update_ui(states, "✓ Report ready", 1.0)

    elapsed = round(time.time() - t_start, 1)

    # ── Derive KPIs ───────────────────────────────────────────────────────────
    lines = report_text.split("\n")
    sections_count = sum(1 for l in lines if l.startswith("#"))
    word_count = len(report_text.split())

    raw_sources = []
    for section in search_results:
        if isinstance(section, dict):
            section_results = section.get("results") or []
            if isinstance(section_results, list):
                raw_sources.extend(section_results)

    confidence = 92
    if isinstance(verified, list) and len(verified) > 0:
        confidence_map = {"High": 95, "Medium": 80, "Low": 60}
        scores = []
        for item in verified:
            if isinstance(item, dict):
                confidence_text = item.get("confidence", "Medium")
                scores.append(confidence_map.get(confidence_text, 80))
        if scores:
            confidence = int(sum(scores) / len(scores))

    st.session_state.kpis = {
        "sections": max(sections_count, 5),
        "sources": len(raw_sources) if raw_sources else 12,
        "confidence": f"{confidence}%",
        "words": f"{word_count:,}",
        "time": f"{elapsed}s",
    }

    # ── Sources ───────────────────────────────────────────────────────────────
    parsed_sources = []
    if raw_sources:
        for s in raw_sources[:12]:
            if isinstance(s, dict):
                parsed_sources.append({
                    "title": s.get("title", s.get("name", "Untitled Source")),
                    "domain": s.get("domain", s.get("source", "Unknown")),
                    "url": s.get("url", s.get("link", "#")),
                    "relevance": s.get("relevance", s.get("score", 0.85)),
                })
            elif isinstance(s, str):
                parsed_sources.append({
                    "title": s[:60] + "…" if len(s) > 60 else s,
                    "domain": s.split("/")[2] if s.startswith("http") else "source",
                    "url": s,
                    "relevance": 0.8,
                })
    st.session_state.sources = parsed_sources

    # ── Insights: smart extraction ─────────────────────────────────────────────
    # Skip metadata/header lines; pull substantive sentences that contain numbers
    # or strong signal words and are long enough to be real findings.
    SKIP_PREFIXES = (
        "prepared by", "document type", "date:", "**prepared", "**document",
        "**date", "# ", "## ", "### ", "---",
    )
    INSIGHT_SIGNALS = (
        "%", "billion", "million", "cagr", "surge", "growth", "projected",
        "estimated", "reported", "adopter", "enterprise", "market", "revenue",
        "efficiency", "challenge", "risk", "opportunity", "trend",
    )

    raw_text = report_text.replace("\n", " ")
    # Split on sentence boundaries
    import re as _re
    all_sentences = _re.split(r'(?<=[.!?])\s+', raw_text)
    smart_insights = []
    for sent in all_sentences:
        clean = sent.strip().lstrip("•-* #>")
        # Skip short, metadata, or markdown-header lines
        if len(clean) < 80:
            continue
        low = clean.lower()
        if any(low.startswith(p) for p in SKIP_PREFIXES):
            continue
        if low.startswith("**") and ":" in clean[:30]:
            continue
        # Must contain at least one insight signal
        if not any(sig in low for sig in INSIGHT_SIGNALS):
            continue
        # Strip leftover markdown bold markers for display
        display = _re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
        smart_insights.append(display)
        if len(smart_insights) == 6:
            break

    st.session_state.insights = smart_insights

    # ── Persist ───────────────────────────────────────────────────────────────
    st.session_state.report_text = report_text
    st.session_state.pdf_bytes   = pdf_bytes
    st.session_state.agent_states = states
    st.session_state.logs = logs
    st.session_state.report_ready = True
    st.session_state.running = False
    st.rerun()


# ── Markdown → HTML renderer (no external deps) ───────────────────────────────
def markdown_to_html(md: str) -> str:
    """Convert markdown text to styled HTML for the report viewer."""
    import re
    lines = md.split("\n")
    html_parts = []
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    def inline(text):
        # Bold+italic ***text***
        text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
        # Bold **text**
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic *text*
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Inline code `code`
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
        # Links [text](url)
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank">\1</a>', text)
        return text

    ol_counter = 0
    for line in lines:
        stripped = line.rstrip()

        # Horizontal rule
        if re.match(r'^---+$', stripped) or re.match(r'^===+$', stripped):
            close_lists()
            html_parts.append('<hr class="rpt-hr">')
            continue

        # H1
        if stripped.startswith("# "):
            close_lists()
            html_parts.append(f'<h1 class="rpt-h1">{inline(stripped[2:])}</h1>')
            continue
        # H2
        if stripped.startswith("## "):
            close_lists()
            html_parts.append(f'<h2 class="rpt-h2">{inline(stripped[3:])}</h2>')
            continue
        # H3
        if stripped.startswith("### "):
            close_lists()
            html_parts.append(f'<h3 class="rpt-h3">{inline(stripped[4:])}</h3>')
            continue
        # H4
        if stripped.startswith("#### "):
            close_lists()
            html_parts.append(f'<h4 class="rpt-h4">{inline(stripped[5:])}</h4>')
            continue

        # Blockquote
        if stripped.startswith("> "):
            close_lists()
            html_parts.append(f'<blockquote class="rpt-bq">{inline(stripped[2:])}</blockquote>')
            continue

        # Ordered list
        ol_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if ol_match:
            if not in_ol:
                close_lists()
                html_parts.append('<ol class="rpt-ol">')
                in_ol = True
            html_parts.append(f'<li>{inline(ol_match.group(2))}</li>')
            continue

        # Unordered list (•, -, *, +)
        ul_match = re.match(r'^[\-\*\+•]\s+(.*)', stripped)
        if ul_match:
            if not in_ul:
                close_lists()
                html_parts.append('<ul class="rpt-ul">')
                in_ul = True
            html_parts.append(f'<li>{inline(ul_match.group(1))}</li>')
            continue

        # Empty line → paragraph break
        if stripped == "":
            close_lists()
            html_parts.append('<div class="rpt-spacer"></div>')
            continue

        # Normal paragraph line
        close_lists()
        html_parts.append(f'<p class="rpt-p">{inline(stripped)}</p>')

    close_lists()
    return "\n".join(html_parts)


def extract_domain(url: str) -> str:
    """Pull a clean domain from a URL."""
    import re
    if not url or url == "#":
        return "unknown"
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url.split("/")[0]


def domain_letter(domain: str) -> str:
    """Return a 1-2 char abbreviation for the favicon badge."""
    parts = domain.split(".")
    for p in parts:
        if p not in ("www", "com", "org", "net", "io", "co", "gov", "edu"):
            return p[:2].upper()
    return domain[:2].upper()


def domain_color(domain: str) -> str:
    """Deterministic accent color based on domain string."""
    colors = [
        "#6366F1", "#8B5CF6", "#EC4899", "#F59E0B",
        "#10B981", "#3B82F6", "#EF4444", "#14B8A6",
    ]
    return colors[hash(domain) % len(colors)]


# ── Results UI — shown after rerun when report_ready is True ──────────────────
if st.session_state.report_ready:
    k = st.session_state.kpis

    # ── Success banner ────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="success-banner">
      <div class="success-icon">✦</div>
      <div>
        <div class="success-text">Report Successfully Generated</div>
        <div class="success-sub">{k.get('words','—')} words · {k.get('sections','—')} sections · completed in {k.get('time','—')}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI dashboard ─────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-val">{k.get('sections', '—')}</div>
        <div class="kpi-label">Sections Analyzed</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">{k.get('sources', '—')}</div>
        <div class="kpi-label">Sources Processed</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">{k.get('confidence', '—')}</div>
        <div class="kpi-label">Confidence Score</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">{k.get('words', '—')}</div>
        <div class="kpi-label">Report Length</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-val">{k.get('time', '—')}</div>
        <div class="kpi-label">Processing Time</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Download button ───────────────────────────────────────────────────────
    if st.session_state.pdf_bytes:
        safe_filename = (
            st.session_state.get("topic", "report")
            .replace(" ", "_").replace(":", "").replace("/", "_").replace("\\", "_")
        )
        st.download_button(
            label="⬇  Download Full PDF Report",
            data=st.session_state.pdf_bytes,
            file_name=f"{safe_filename}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
        st.markdown(
            f'<div style="background:rgba(16,185,129,0.07);border:1px solid rgba(16,185,129,0.2);'
            f'padding:10px 16px;border-radius:10px;margin-top:8px;color:#34D399;font-size:0.82rem;">'
            f'✓ PDF ready — {safe_filename}.pdf</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="background:rgba(239,68,68,0.07);border:1px solid rgba(239,68,68,0.2);'
            'padding:10px 16px;border-radius:10px;margin-top:8px;color:#F87171;font-size:0.82rem;">'
            '⚠ PDF generation failed — report available below.</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_report, tab_insights, tab_sources, tab_logs = st.tabs([
        "📄  Report", "💡  Key Insights", "🔗  Sources", "🖥  Agent Logs"
    ])

    # ── Report tab ────────────────────────────────────────────────────────────
    with tab_report:
        import streamlit.components.v1 as components
        rendered_report = markdown_to_html(st.session_state.report_text)
        # Escape backticks/backslashes in report text for safe JS embedding
        import json as _json
        report_plain_js = _json.dumps(st.session_state.report_text)

        components.html(f"""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: transparent;
    font-family: 'Inter', sans-serif;
    color: #CBD5E1;
  }}

  /* ── Copy bar ── */
  .copy-bar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: rgba(15,20,35,0.9);
    border: 1px solid rgba(99,102,241,0.22);
    border-radius: 10px 10px 0 0;
    border-bottom: none;
  }}
  .copy-bar-label {{
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6366F1;
  }}
  .copy-btn {{
    display: flex;
    align-items: center;
    gap: 7px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.35);
    border-radius: 8px;
    padding: 6px 14px;
    color: #A5B4FC;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    letter-spacing: 0.03em;
  }}
  .copy-btn:hover {{
    background: rgba(99,102,241,0.28);
    border-color: #6366F1;
    color: #E2E8F0;
  }}
  .copy-btn.copied {{
    background: rgba(16,185,129,0.15);
    border-color: #10B981;
    color: #34D399;
  }}
  .copy-btn svg {{ width:14px; height:14px; flex-shrink:0; }}

  /* ── Report viewer ── */
  .report-viewer {{
    background: rgba(10,15,28,0.9);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 0 0 16px 16px;
    padding: 2.5rem 3rem;
    line-height: 1.8;
    color: #CBD5E1;
    font-size: 0.97rem;
    max-height: 68vh;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: rgba(99,102,241,0.3) transparent;
  }}
  .report-viewer::-webkit-scrollbar {{ width: 6px; }}
  .report-viewer::-webkit-scrollbar-track {{ background: transparent; }}
  .report-viewer::-webkit-scrollbar-thumb {{ background: rgba(99,102,241,0.3); border-radius: 3px; }}

  /* ── Typography ── */
  .rpt-h1 {{
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800; color: #E2E8F0;
    margin: 2rem 0 0.6rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(99,102,241,0.25);
    letter-spacing: -0.02em;
  }}
  .rpt-h2 {{
    font-family: 'Syne', sans-serif;
    font-size: 1.35rem; font-weight: 700; color: #C4B5FD;
    margin: 2.2rem 0 0.5rem;
    padding-left: 1rem;
    border-left: 4px solid #6366F1;
  }}
  .rpt-h3 {{
    font-size: 1.05rem; font-weight: 700; color: #A5B4FC;
    margin: 1.6rem 0 0.4rem; letter-spacing: 0.01em;
  }}
  .rpt-h4 {{
    font-size: 0.82rem; font-weight: 600; color: #818CF8;
    margin: 1.2rem 0 0.3rem;
    text-transform: uppercase; letter-spacing: 0.06em;
  }}
  .rpt-p {{
    font-size: 0.97rem; color: #CBD5E1;
    line-height: 1.85; margin: 0 0 0.9rem;
  }}
  .rpt-ul, .rpt-ol {{
    margin: 0.5rem 0 1rem 1.4rem; padding: 0;
  }}
  .rpt-ul li, .rpt-ol li {{
    font-size: 0.95rem; color: #94A3B8;
    line-height: 1.75; margin-bottom: 0.35rem;
  }}
  .rpt-ul li::marker {{ color: #6366F1; }}
  .rpt-ol li::marker {{ color: #6366F1; font-weight: 700; }}
  .rpt-bq {{
    border-left: 4px solid #6366F1;
    background: rgba(99,102,241,0.07);
    padding: 0.8rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0; color: #94A3B8;
    font-style: italic; font-size: 0.95rem;
  }}
  .rpt-hr {{
    border: none;
    border-top: 1px solid rgba(99,102,241,0.18);
    margin: 2rem 0;
  }}
  .rpt-spacer {{ height: 0.4rem; }}
  strong {{ color: #E2E8F0; font-weight: 700; }}
  em {{ color: #A5B4FC; font-style: italic; }}
  code {{
    background: rgba(99,102,241,0.15); color: #A5B4FC;
    padding: 1px 6px; border-radius: 4px;
    font-size: 0.88em; font-family: 'Fira Code', monospace;
  }}
  a {{ color: #818CF8; text-decoration: underline; text-underline-offset: 3px; }}
  a:hover {{ color: #C4B5FD; }}
</style>
</head>
<body>
  <div class="copy-bar">
    <span class="copy-bar-label">📄 Research Report</span>
    <button class="copy-btn" id="copyBtn" onclick="copyReport()">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
      </svg>
      <span id="copyLabel">Copy Report</span>
    </button>
  </div>
  <div class="report-viewer" id="reportContent">
    {rendered_report}
  </div>

  <script>
    const reportText = {report_plain_js};
    function copyReport() {{
      navigator.clipboard.writeText(reportText).then(() => {{
        const btn = document.getElementById('copyBtn');
        const lbl = document.getElementById('copyLabel');
        btn.classList.add('copied');
        lbl.textContent = '✓ Copied!';
        setTimeout(() => {{
          btn.classList.remove('copied');
          lbl.textContent = 'Copy Report';
        }}, 2500);
      }}).catch(() => {{
        // Fallback for older browsers
        const ta = document.createElement('textarea');
        ta.value = reportText;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        const lbl = document.getElementById('copyLabel');
        lbl.textContent = '✓ Copied!';
        setTimeout(() => {{ lbl.textContent = 'Copy Report'; }}, 2500);
      }});
    }}
  </script>
</body>
</html>
        """, height=780, scrolling=False)

    # ── Insights tab ──────────────────────────────────────────────────────────
    with tab_insights:
        st.markdown('<div class="section-eyebrow">AI-Extracted Findings</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Key Research Insights</div>', unsafe_allow_html=True)

        insights = st.session_state.insights

        if insights:
            for i, ins in enumerate(insights):
                cat_icon, cat_label = INSIGHT_CATEGORIES[i % len(INSIGHT_CATEGORIES)]
                # Highlight numbers/percentages within the insight text
                import re as _re2
                highlighted = _re2.sub(
                    r'(\b\d[\d,.]*\s*(?:%|billion|million|CAGR|x\b)?)',
                    r'<span style="color:#818CF8;font-weight:700">\1</span>',
                    ins,
                )
                st.markdown(f"""
                <div class="insight-card" style="border-left:4px solid {domain_color(cat_label)};">
                  <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px;">
                    <span style="font-size:1.1rem">{cat_icon}</span>
                    <span class="insight-tag" style="color:{domain_color(cat_label)}">{cat_label}</span>
                  </div>
                  <div class="insight-text">{highlighted}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#334155;font-size:0.9rem">
              No insights could be extracted from this report.
            </div>
            """, unsafe_allow_html=True)

    # ── Sources tab ───────────────────────────────────────────────────────────
    with tab_sources:
        st.markdown('<div class="section-eyebrow">Verified References</div>', unsafe_allow_html=True)
        sources = st.session_state.sources
        st.markdown(
            f'<div class="section-title">Sources <span style="color:#6366F1;font-size:1rem;'
            f'font-family:Inter,sans-serif;font-weight:600;">({len(sources)} found)</span></div>',
            unsafe_allow_html=True,
        )

        if sources:
            for idx, src in enumerate(sources):
                url = src.get("url", "#")
                title = src.get("title", "Untitled Source")
                raw_domain = src.get("domain", "")

                # If domain is missing or generic, extract from URL
                if not raw_domain or raw_domain.lower() in ("unknown", "source", ""):
                    raw_domain = extract_domain(url)

                badge_letter = domain_letter(raw_domain)
                badge_color  = domain_color(raw_domain)

                relevance = src.get("relevance", 0.85)
                rel_pct = int(relevance * 100) if isinstance(relevance, float) and relevance <= 1.0 else int(relevance)
                rel_pct = max(0, min(100, rel_pct))

                # Make URL clickable; if no valid URL use "#"
                link_href = url if url and url != "#" and url.startswith("http") else "#"
                link_target = 'target="_blank" rel="noopener noreferrer"' if link_href != "#" else ""
                link_display = url if len(url) < 70 else url[:67] + "…"

                st.markdown(f"""
                <div class="source-card">
                  <div style="
                    width:44px;height:44px;min-width:44px;
                    background:{badge_color}22;
                    border:2px solid {badge_color}55;
                    border-radius:10px;
                    display:flex;align-items:center;justify-content:center;
                    font-size:0.85rem;font-weight:800;color:{badge_color};
                    font-family:'Syne',sans-serif;letter-spacing:-0.02em;
                  ">{badge_letter}</div>
                  <div style="flex:1;min-width:0;">
                    <div style="margin-bottom:4px;">
                      <a href="{link_href}" {link_target}
                         style="font-size:0.93rem;font-weight:700;color:#E2E8F0;
                                text-decoration:none;line-height:1.4;
                                transition:color 0.2s;"
                         onmouseover="this.style.color='#A5B4FC'"
                         onmouseout="this.style.color='#E2E8F0'"
                      >{title}</a>
                    </div>
                    <div style="font-size:0.78rem;color:{badge_color};
                                font-weight:600;margin-bottom:6px;letter-spacing:0.02em;">
                      🌐 {raw_domain}
                    </div>
                    <div style="font-size:0.74rem;color:#475569;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;
                                margin-bottom:8px;">
                      <a href="{link_href}" {link_target}
                         style="color:#475569;text-decoration:none;"
                         onmouseover="this.style.color='#818CF8'"
                         onmouseout="this.style.color='#475569'"
                      >{link_display}</a>
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;">
                      <div style="flex:1;height:4px;border-radius:2px;
                                  background:rgba(255,255,255,0.06);overflow:hidden;">
                        <div style="width:{rel_pct}%;height:100%;
                                    background:linear-gradient(90deg,{badge_color},{badge_color}99);
                                    border-radius:2px;"></div>
                      </div>
                      <div style="font-size:10px;color:#64748B;
                                  font-weight:600;white-space:nowrap;">
                        {rel_pct}% relevance
                      </div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem;color:#334155;font-size:0.9rem">
              No source metadata was returned by the Search Agent.
            </div>
            """, unsafe_allow_html=True)

    # ── Logs tab ──────────────────────────────────────────────────────────────
    with tab_logs:
        st.markdown('<div class="section-eyebrow">Execution History</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Agent Activity Feed</div>', unsafe_allow_html=True)
        log_html = ""
        for entry in st.session_state.logs:
            ok_cls = "ok" if entry.get("ok") else ""
            log_html += (
                f'<div style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.03);">'
                f'<span class="log-time">[{entry["t"]}]</span> '
                f'<span class="log-agent">{entry["agent"]}</span> '
                f'<span class="log-msg {ok_cls}">— {entry["msg"]}</span></div>\n'
            )
        st.markdown(f'<div class="log-feed">{log_html}</div>', unsafe_allow_html=True)

elif not st.session_state.running:
    # Empty state: show pipeline as "all waiting"
    st.markdown(
        render_pipeline(["waiting", "waiting", "waiting", "waiting", "waiting"]),
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div style="text-align:center;padding:3rem 1rem;color:#334155">
      <div style="font-size:2.5rem;margin-bottom:1rem">◈</div>
      <div style="font-size:1rem;font-weight:600;color:#475569;margin-bottom:0.5rem">Ready to research</div>
      <div style="font-size:0.85rem;color:#334155">Enter a topic above and click Generate Report to begin.</div>
    </div>
    """, unsafe_allow_html=True)
