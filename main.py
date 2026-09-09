from exa_py import Exa
import streamlit as st
import re
import os
import sqlite3 as sql
from dotenv import load_dotenv
import json
load_dotenv() #importing Exa with the API key
@st.cache_resource
def get_db_connection():
    conn = sql.connect('queryHistory.db', check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS UQUERIES (
    query TEXT,
    results_json TEXT
    ) """) #creates a table with an unique integer and text of the query
    return conn
#database for unique search queries
connection = get_db_connection() #user's search history
cursor = connection.cursor() #used to change data

st.set_page_config(page_title="Search Anything", page_icon="🔍")

st.title("Search Anything")

# Input field and submit button
query = st.text_input("Enter your query:")
search_button = st.button("Search & Summarize", type="primary")
with st.sidebar:
    category_display = st.selectbox(
        "Filter Category", 
        ["None", "GitHub Repos", "Research Papers", "News"]
        )
            
    year_options = ['All-Time'] + list(range(2026, 2006, -1))
            
    yearSelection = st.selectbox(
        "Filter Publish Date",
        options=year_options,
        )
    category_mapping = {
        "None": None,
        "GitHub Repos": "github",
        "Research Papers": "research paper",
        "News": "news"
    }
if "results_list" not in st.session_state:
    st.session_state.results_list = []
if search_button and query:
    
    #Check database if a query exists to load it instantly from SQLite to save time and API credits
    cache_key = f"{query}|cat:{category_display}|year:{yearSelection}".lower()
    cursor.execute("SELECT results_json FROM UQUERIES WHERE LOWER(query) = ?", (cache_key,))
    cached_record = cursor.fetchone()
    if cached_record:
        st.session_state.results_list = json.loads(cached_record[0])
    else:
        api_key = os.getenv("API_KEY")
        if not api_key:
            st.error("API_KEY environment variable not found. Please check your .env file.")
            st.stop()

        exa = Exa(api_key=api_key)
        querySearch = {
            "query": f"{query} in English",
            "num_results": 5,
            "contents": {"summary": True}
        }
        if yearSelection != "All-Time":
            querySearch["start_published_date"] = f"{yearSelection}-01-01T00:00:00.000Z"
            querySearch["end_published_date"] = f"{yearSelection}-12-31T23:59:59.000Z"
        selectedCategory = category_mapping.get(category_display)
        if selectedCategory is not None:
            querySearch["category"] = category_mapping[category_display]
        with st.spinner("Searching..."):
            
            try:
                # Fetch search results along with summary text from Exa
                
                response = exa.search(
                    **querySearch
                )
                st.session_state.results_list =[{"title" :getattr(r, "title", "Untitled Result"),
                                    "url" : getattr(r, "url", "#"),
                                    "summary" : getattr(r, "summary", "No summary available.")}
                                    for r in response.results]
                
                
                cursor.execute("INSERT INTO UQUERIES (query, results_json) VALUES(?, ?)", (cache_key, json.dumps(st.session_state.results_list)))
                connection.commit()
                # Render results using expanders
               
            except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.session_state.results_list:
        st.subheader("Results")
        for idx, result in enumerate(st.session_state.results_list, 1):
            title = result["title"]
            url = result["url"]
            summary = result["summary"]
            compiled = re.compile(re.escape(query), re.IGNORECASE)
            highlighted_title = compiled.sub(r":yellow-background[\g<0>]", title) if query.lower() in title.lower() else title
            with st.expander(f"{idx}. {highlighted_title}", expanded=(idx == 2)): #gives the collapsable boxes
                st.markdown(f"**URL:** [{url}]({url})")
                st.markdown("### Summary")
                if query.lower() in summary.lower():
                    highlighted_summary = compiled.sub(r":yellow-background[\g<0>]", summary)
                    st.markdown(highlighted_summary)
                else:
                    st.write(summary)

    