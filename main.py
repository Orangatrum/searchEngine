from datetime import datetime
import requests
import streamlit as st

st.set_page_config(page_title="Search Anything", page_icon="🔍")

st.markdown(
    """
    <div style="padding-bottom: 16px;">
        <span style="font-size: 56px; font-weight: 800; color: #3b82f6; display: block;">
            Search Anything
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sidebar Filters
with st.sidebar:
    st.header("Search Filters")

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
    domains_input = st.text_input("Include Domains (comma-separated)", placeholder="e.g. github.com, arxiv.org")

query = st.text_input("Enter your query:")
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

    # Format dates to ISO strings for Exa API
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
            st.markdown(f"**URL:** [{url}]({url})")
            if pub_date:
                st.caption(f"Published: {pub_date}")
            st.markdown("### Summary")
            st.markdown(summary)