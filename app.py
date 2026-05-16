import streamlit as st
import time
from research_pipeline import run_research_pipeline

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · Multi-Agent AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0f;
    color: #e8e4d9;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e30;
}
[data-testid="stSidebar"] * { color: #e8e4d9 !important; }

/* ── Main background ── */
.stApp { background: #0a0a0f; }
.main .block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 1100px; }

/* ── Hero header ── */
.hero-wrap {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 2px;
    background: linear-gradient(90deg, transparent, #e8c547, transparent);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #f5f0e8;
    margin: 0;
    line-height: 1;
}
.hero-title span { color: #e8c547; }
.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #6b6b7a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.6rem;
}

/* ── Pipeline status bar ── */
.pipeline-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin: 2rem auto 1.5rem;
    max-width: 700px;
}
.pipe-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    flex: 1;
    position: relative;
}
.pipe-node:not(:last-child)::after {
    content: '';
    position: absolute;
    top: 18px;
    left: 60%;
    width: 80%;
    height: 1px;
    background: #1e1e30;
    z-index: 0;
}
.pipe-node.active:not(:last-child)::after { background: #e8c547; }
.pipe-dot {
    width: 36px; height: 36px;
    border-radius: 50%;
    border: 2px solid #1e1e30;
    background: #0f0f18;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    z-index: 1;
    transition: all 0.4s;
}
.pipe-node.active .pipe-dot  { border-color: #e8c547; background: #1e1a05; box-shadow: 0 0 12px #e8c54740; }
.pipe-node.done   .pipe-dot  { border-color: #4caf82; background: #051a0f; box-shadow: 0 0 10px #4caf8240; }
.pipe-node.error  .pipe-dot  { border-color: #e85447; background: #1a0505; }
.pipe-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2px;
    color: #3a3a4a;
    text-transform: uppercase;
}
.pipe-node.active .pipe-label { color: #e8c547; }
.pipe-node.done   .pipe-label { color: #4caf82; }

/* ── Input box ── */
.stTextInput > div > div > input {
    background: #0f0f18 !important;
    border: 1px solid #2a2a3d !important;
    border-radius: 6px !important;
    color: #f5f0e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e8c547 !important;
    box-shadow: 0 0 0 2px #e8c54725 !important;
}
.stTextInput label { color: #6b6b7a !important; font-size: 0.72rem !important; letter-spacing: 2px !important; text-transform: uppercase !important; }

/* ── Buttons ── */
.stButton > button {
    background: #e8c547 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { background: #f5d84a !important; transform: translateY(-1px); box-shadow: 0 4px 20px #e8c54730 !important; }

/* ── Cards / output blocks ── */
.output-card {
    background: #0f0f18;
    border: 1px solid #1e1e30;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.output-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
}
.card-search::before  { background: #5b8cf5; }
.card-reader::before  { background: #a855f7; }
.card-writer::before  { background: #e8c547; }
.card-critic::before  { background: #4caf82; }

.card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.8rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid #1e1e30;
}
.card-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
}
.badge-search { background: #0d1a3a; color: #5b8cf5; border: 1px solid #1a2d5a; }
.badge-reader { background: #1a0d3a; color: #a855f7; border: 1px solid #2d1a5a; }
.badge-writer { background: #1e1a05; color: #e8c547; border: 1px solid #3a3205; }
.badge-critic { background: #051a0f; color: #4caf82; border: 1px solid #0a3a1e; }

.card-content {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.8;
    color: #b8b4ab;
    white-space: pre-wrap;
    max-height: 320px;
    overflow-y: auto;
}
.card-content::-webkit-scrollbar { width: 4px; }
.card-content::-webkit-scrollbar-track { background: transparent; }
.card-content::-webkit-scrollbar-thumb { background: #2a2a3d; border-radius: 4px; }

/* ── Critic score highlight ── */
.score-big {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #4caf82;
    text-align: center;
    padding: 1rem 0 0.5rem;
}

/* ── Running spinner ── */
.running-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.7rem;
    color: #e8c547;
    letter-spacing: 2px;
    text-transform: uppercase;
    animation: pulse 1.2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Section divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1e30, transparent);
    margin: 2rem 0;
}

/* ── Report full display ── */
.report-full {
    background: #0f0f18;
    border: 1px solid #2a2a3d;
    border-radius: 10px;
    padding: 2rem 2.4rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.83rem;
    line-height: 1.9;
    color: #d8d4cb;
    white-space: pre-wrap;
}

/* ── Sidebar API section ── */
.api-label {
    font-size: 0.65rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4a4a5a;
    margin-bottom: 4px;
    margin-top: 1rem;
}

/* ── Toast / success ── */
.success-banner {
    background: linear-gradient(135deg, #051a0f, #0a2a1a);
    border: 1px solid #4caf82;
    border-radius: 8px;
    padding: 1rem 1.4rem;
    text-align: center;
    color: #4caf82;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}

/* ── Streamlit overrides ── */
.stSpinner > div { border-top-color: #e8c547 !important; }
div[data-testid="stStatusWidget"] { display: none; }
footer { display: none !important; }
#MainMenu { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "pipeline_status" not in st.session_state:
    st.session_state.pipeline_status = {}  # step -> "idle"|"running"|"done"|"error"
if "running" not in st.session_state:
    st.session_state.running = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.5rem">
        <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;color:#f5f0e8">
            🧠 ResearchMind
        </div>
        <div style="font-size:0.62rem;letter-spacing:3px;color:#4a4a5a;text-transform:uppercase;margin-top:4px">
            Multi-Agent AI System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="api-label">🔑 Tavily API Key</div>', unsafe_allow_html=True)
    tavily_key = st.text_input(
        "Tavily", label_visibility="collapsed",
        value=st.session_state.get("tavily_key", ""),
        type="password", placeholder="tvly-..."
    )

    st.markdown('<div class="api-label">🔑 Google (Gemini) API Key</div>', unsafe_allow_html=True)
    google_key = st.text_input(
        "Google", label_visibility="collapsed",
        value=st.session_state.get("google_key", ""),
        type="password", placeholder="AIza..."
    )

    if tavily_key:
        st.session_state.tavily_key = tavily_key
    if google_key:
        st.session_state.google_key = google_key

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.68rem;color:#3a3a4a;line-height:1.8">
        <div style="color:#5a5a6a;margin-bottom:6px;letter-spacing:2px;font-size:0.6rem;text-transform:uppercase">Pipeline</div>
        🔵 Search Agent — Tavily<br>
        🟣 Reader Agent — Scraper<br>
        🟡 Writer Chain — Gemini<br>
        🟢 Critic Chain — Gemini
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("🗑 Clear Results", use_container_width=True):
        st.session_state.results = {}
        st.session_state.pipeline_status = {}
        st.session_state.running = False
        st.rerun()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <h1 class="hero-title">Research<span>Mind</span></h1>
    <p class="hero-sub">4-Agent AI Research Pipeline · Powered by Gemini + Tavily</p>
</div>
""", unsafe_allow_html=True)

# ── Pipeline visual bar ───────────────────────────────────────────────────────
def pipeline_bar(statuses: dict):
    steps = [
        ("search",  "🔵", "Search"),
        ("reader",  "🟣", "Reader"),
        ("writer",  "🟡", "Writer"),
        ("critic",  "🟢", "Critic"),
    ]
    nodes = ""
    for key, icon, label in steps:
        s = statuses.get(key, "idle")
        cls = "active" if s == "running" else ("done" if s == "done" else ("error" if s == "error" else ""))
        dot_icon = "✓" if s == "done" else ("✕" if s == "error" else ("⟳" if s == "running" else icon))
        nodes += f"""
        <div class="pipe-node {cls}">
            <div class="pipe-dot">{dot_icon}</div>
            <div class="pipe-label">{label}</div>
        </div>"""
    st.markdown(f'<div class="pipeline-bar">{nodes}</div>', unsafe_allow_html=True)

pipeline_bar(st.session_state.pipeline_status)

# ── Topic input ───────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Latest breakthroughs in quantum computing 2025",
        label_visibility="collapsed"
    )
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        run_btn = st.button("⚡  LAUNCH PIPELINE", use_container_width=True, disabled=st.session_state.running)

# ── Validation & Run ──────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    elif not st.session_state.get("tavily_key"):
        st.warning("Add your Tavily API key in the sidebar.")
    elif not st.session_state.get("google_key"):
        st.warning("Add your Google API key in the sidebar.")
    else:
        st.session_state.running = True
        st.session_state.results = {}
        st.session_state.pipeline_status = {}
        st.session_state.current_topic = topic
        st.rerun()

# ── Live pipeline execution ───────────────────────────────────────────────────
if st.session_state.running:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    results_placeholder = st.empty()

    with results_placeholder.container():
        pipeline_bar(st.session_state.pipeline_status)

        try:
            for step, status, data in run_research_pipeline(
                st.session_state.current_topic,
                st.session_state.tavily_key,
                st.session_state.google_key,
            ):
                if step == "complete":
                    st.session_state.results = data
                    st.session_state.running = False
                    st.session_state.pipeline_status = {
                        "search": "done", "reader": "done",
                        "writer": "done", "critic": "done"
                    }
                    break

                st.session_state.pipeline_status[step] = status

                if status == "done":
                    st.session_state.results[step] = data

                results_placeholder.empty()
                with results_placeholder.container():
                    pipeline_bar(st.session_state.pipeline_status)
                    _render_results(st.session_state.results, st.session_state.pipeline_status)

        except Exception as e:
            st.session_state.running = False
            st.error(f"Pipeline error: {str(e)}")

    st.rerun()

# ── Render function ───────────────────────────────────────────────────────────
def _render_results(results: dict, statuses: dict):

    CARDS = [
        ("search",  "SEARCH AGENT",  "badge-search", "card-search",  "🔵",
         "Web search results gathered by Tavily"),
        ("reader",  "READER AGENT",  "badge-reader", "card-reader",  "🟣",
         "Deep content scraped from top URL"),
        ("writer",  "WRITER CHAIN",  "badge-writer", "card-writer",  "🟡",
         "Structured research report"),
        ("critic",  "CRITIC CHAIN",  "badge-critic", "card-critic",  "🟢",
         "Expert evaluation & score"),
    ]

    for key, title, badge_cls, card_cls, icon, desc in CARDS:
        s = statuses.get(key, "idle")
        if s == "idle":
            continue

        if s == "running":
            st.markdown(f"""
            <div class="output-card {card_cls}">
                <div class="card-header">
                    <span class="card-badge {badge_cls}">{title}</span>
                    <span class="running-tag">⟳ PROCESSING</span>
                </div>
                <div style="color:#3a3a4a;font-size:0.78rem">{desc}…</div>
            </div>
            """, unsafe_allow_html=True)

        elif s == "done" and key in results:
            content = results[key]

            # Special rendering for critic — extract score
            if key == "critic":
                score_line = ""
                for line in content.split("\n"):
                    if line.startswith("Score:"):
                        score_line = line.replace("Score:", "").strip()
                        break
                score_html = f'<div class="score-big">{score_line}</div>' if score_line else ""
                st.markdown(f"""
                <div class="output-card {card_cls}">
                    <div class="card-header">
                        <span class="card-badge {badge_cls}">{title}</span>
                        <span style="font-size:0.7rem;color:#3a3a4a;margin-left:auto">{desc}</span>
                    </div>
                    {score_html}
                    <div class="card-content">{content}</div>
                </div>
                """, unsafe_allow_html=True)

            # Writer — show full report as expandable
            elif key == "writer":
                st.markdown(f"""
                <div class="output-card {card_cls}">
                    <div class="card-header">
                        <span class="card-badge {badge_cls}">{title}</span>
                        <span style="font-size:0.7rem;color:#3a3a4a;margin-left:auto">{desc}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("📄 Read Full Report", expanded=True):
                    st.markdown(f'<div class="report-full">{content}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Download Report (.txt)",
                        data=content,
                        file_name=f"report_{st.session_state.get('current_topic','research').replace(' ','_')[:30]}.txt",
                        mime="text/plain",
                    )

            else:
                st.markdown(f"""
                <div class="output-card {card_cls}">
                    <div class="card-header">
                        <span class="card-badge {badge_cls}">{title}</span>
                        <span style="font-size:0.7rem;color:#3a3a4a;margin-left:auto">{desc}</span>
                    </div>
                    <div class="card-content">{content[:1500]}{'…' if len(content) > 1500 else ''}</div>
                </div>
                """, unsafe_allow_html=True)

        elif s == "error":
            err = results.get(key, "Unknown error")
            st.markdown(f"""
            <div class="output-card" style="border-color:#e85447">
                <div class="card-header">
                    <span class="card-badge" style="background:#1a0505;color:#e85447;border-color:#3a0a0a">{title}</span>
                    <span style="font-size:0.7rem;color:#e85447;margin-left:auto">ERROR</span>
                </div>
                <div class="card-content" style="color:#e85447">{err}</div>
            </div>
            """, unsafe_allow_html=True)


# ── Show completed results ────────────────────────────────────────────────────
if st.session_state.results and not st.session_state.running:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    all_done = all(
        st.session_state.pipeline_status.get(s) == "done"
        for s in ["search", "reader", "writer", "critic"]
    )
    if all_done:
        st.markdown("""
        <div class="success-banner">
            ✓ Research Pipeline Complete
        </div>
        """, unsafe_allow_html=True)

    _render_results(st.session_state.results, st.session_state.pipeline_status)

# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.results and not st.session_state.running:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0;color:#2a2a3a">
        <div style="font-size:3rem;margin-bottom:1rem">◈</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.75rem;letter-spacing:3px;text-transform:uppercase">
            Enter a topic and launch the pipeline
        </div>
    </div>
    """, unsafe_allow_html=True)
