from datetime import datetime

import requests
import streamlit as st
import st_tailwind as tw

st.set_page_config(page_title="Search Anything", page_icon="🔍")
tw.initialize_tailwind()

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(59, 130, 246, 0.22), transparent 28%),
                radial-gradient(circle at top right, rgba(34, 197, 94, 0.18), transparent 26%),
                radial-gradient(circle at bottom left, rgba(168, 85, 247, 0.18), transparent 30%),
                linear-gradient(135deg, #020817 0%, #0f172a 25%, #111827 55%, #0b1120 100%);
        }
        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(148, 163, 184, 0.08) 1px, transparent 1px),
                linear-gradient(90deg, rgba(148, 163, 184, 0.08) 1px, transparent 1px);
            background-size: 36px 36px;
            mask-image: radial-gradient(circle at center, black 32%, transparent 100%);
            pointer-events: none;
        }
        .search-shell {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 50%, rgba(15, 118, 110, 0.55) 100%);
            padding: 1.7rem 1.5rem 1.2rem 1.5rem;
            border-radius: 1.5rem;
            border: 1px solid rgba(148, 163, 184, 0.2);
            box-shadow: 0 20px 50px rgba(2, 6, 23, 0.55), inset 0 1px 0 rgba(255,255,255,0.06);
            margin-bottom: 1.25rem;
            position: relative;
            overflow: hidden;
        }
        .search-shell::after {
            content: "";
            position: absolute;
            inset: 0;
            background: radial-gradient(circle at 20% 20%, rgba(125, 211, 252, 0.22), transparent 35%);
            pointer-events: none;
        }
        .search-title {
            position: relative;
            z-index: 1;
            font-size: 3.2rem;
            font-weight: 800;
            letter-spacing: -0.06em;
            background: linear-gradient(90deg, #f8fafc 0%, #c4b5fd 18%, #7dd3fc 42%, #86efac 100%);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            display: block;
            margin: 0;
            text-shadow: 0 0 18px rgba(125, 211, 252, 0.25);
        }
        .search-subtitle {
            position: relative;
            z-index: 1;
            color: rgba(226, 232, 240, 0.88);
            font-size: 1rem;
            margin-top: 0.6rem;
            letter-spacing: 0.01em;
        }
        div[data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.9);
            border-right: 1px solid rgba(148, 163, 184, 0.12);
        }
        div[data-testid="stSidebarUserContent"] > div {
            padding-top: 1rem;
        }
        div[data-testid="stExpander"] > details {
            background: rgba(15, 23, 42, 0.56);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 0.9rem;
            padding: 0.2rem 0.75rem;
            margin-bottom: 0.85rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .stTextInput > div > div > input {
            background: rgba(15, 23, 42, 0.6);
            color: #f8fafc;
            border: 1px solid rgba(148, 163, 184, 0.35);
            border-radius: 0.9rem;
            padding: 0.8rem 1rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .stTextInput > div > div > input:focus {
            border-color: rgba(125, 211, 252, 0.9);
            box-shadow: 0 0 0 0.12rem rgba(125, 211, 252, 0.25);
        }
        .stButton > button {
            background: linear-gradient(135deg, #38bdf8 0%, #22c55e 100%);
            color: white;
            border: none;
            border-radius: 0.9rem;
            font-weight: 700;
            padding: 0.7rem 1.3rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            box-shadow: 0 10px 24px rgba(14, 165, 233, 0.35);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 14px 28px rgba(34, 197, 94, 0.28);
        }
        .stForm, .stSelectbox, .stCheckbox, .stDateInput {
            color: #e2e8f0;
        }
        div[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.9) 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.12);
            padding: 1rem 0.8rem;
        }
        section[data-testid="stSidebar"] > div {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 1.1rem;
            padding: 0.8rem;
            border: 1px solid rgba(148, 163, 184, 0.12);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        [data-testid="stSidebar"] .stHeader {
            background: transparent;
        }
        .sidebar-panel {
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.65));
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 1rem;
            padding: 1rem 0.9rem;
            margin-bottom: 1rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        }
        .sidebar-label {
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-size: 0.72rem;
            color: #7dd3fc;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }
        .stSelectbox > div > div,
        .stCheckbox > label,
        .stDateInput > label,
        .stTextInput > label {
            color: #e2e8f0 !important;
            font-weight: 600;
        }
        .stCheckbox > label > span {
            color: #e2e8f0;
        }
        .stSelectbox > div > div > div,
        .stDateInput > div > div,
        .stTextInput > div > div {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 0.85rem;
        }
        .stSelectbox [role="button"],
        .stDateInput input,
        .stTextInput input {
            color: #f8fafc !important;
        }
        .stCheckbox > label > div {
            background: rgba(59, 130, 246, 0.18);
            border: 1px solid rgba(125, 211, 252, 0.4);
        }
    </style>
    <div class="search-shell">
        <div class="search-title">Search Anything</div>
        <div class="search-subtitle">Knowledge, insight, and discovery — all in one intelligent search experience.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Filters
with st.sidebar:
    st.markdown('<div class="sidebar-panel"><div class="sidebar-label">Search Filters</div></div>', unsafe_allow_html=True)
    st.subheader("Refine Results")
    st.caption("Narrow your discovery by source, date, and domain.")

    enable_date_filter = st.checkbox("Filter by Publication Date")
    start_date = None
    end_date = None

    if enable_date_filter:
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")

    category = st.selectbox(
        "Category",
        options=["All", "Company", "Research Papers", "News", "GitHub", "Tweets"],
        index=0,
    )
    domains_input = st.text_input("Include Domains", placeholder="github.com, arxiv.org")

query = st.text_input("Enter your query:", placeholder="Ask anything...")
search_button = st.button("Search & Summarize", type="primary")

if "results_list" not in st.session_state:
    st.session_state.results_list = []

if search_button and query:
    payload_data = {"query": query}

    if category != "All":
        payload_data["category"] = category

    if domains_input.strip():
        domains_list = [d.strip() for d in domains_input.split(",") if d.strip()]
        payload_data["include_domains"] = domains_list

    # format dates to ISO strings for Exa API
    if enable_date_filter:
        if start_date:
            payload_data["start_published_date"] = f"{start_date.isoformat()}T00:00:00.000Z"
        if end_date:
            payload_data["end_published_date"] = f"{end_date.isoformat()}T23:59:59.999Z"

    with st.spinner("Searching..."):
        try:
            response = requests.post(
                "http://localhost:5000/api/search",
                json=payload_data,
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            results = payload.get("results", {}).get("data", [])
            st.session_state.results_list = results
        except requests.RequestException as exc:
            st.error(f"Request failed: {exc}")
            st.session_state.results_list = []

if st.session_state.results_list:
    st.subheader("Results")
    for idx, result in enumerate(st.session_state.results_list, 1):
        title = result.get("title", "Untitled Result")
        url = result.get("url", "#")
        summary = result.get("summary", "No summary available.")
        pub_date = result.get("published_date")

        with st.expander(f"{idx}. {title}", expanded=(idx == 1)):
            st.markdown(
                f"""
                <div style="padding: 0.6rem 0.8rem; border-left: 4px solid #38bdf8; background: rgba(15, 23, 42, 0.45); border-radius: 0.8rem; margin-bottom: 0.5rem;">
                    <strong>URL:</strong> <a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if pub_date:
                st.caption(f"Published: {pub_date}")
            st.markdown("### Summary")
            st.markdown(summary)
