import streamlit as st
import requests

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

query = st.text_input("Enter your query:")
search_button = st.button("Search & Summarize", type="primary")

if "results_list" not in st.session_state:
    st.session_state.results_list = []

if search_button and query:
    with st.spinner("Searching..."):
        try:
            response = requests.post(
                "http://localhost:5000/api/search",
                json={"query": query},
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

        with st.expander(f"{idx}. {title}", expanded=(idx == 1)):
            st.markdown(f"**URL:** [{url}]({url})")
            st.markdown("### Summary")
            st.markdown(summary)


    