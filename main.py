from exa_py import Exa
import streamlit as st
exa = Exa('0efcc52e-a70c-42d7-8308-9543fdd710b1') #importing Exa with the API key
st.title("Search  n")
query = st.text_input("Enter your query: ") #taking input from the user using streamlit
if st.button("Search & Summarize", type="primary"):
    if query:
        with st.spinner("Searching the web and generating summaries..."):
            try:
                    # execute search and request summaries inside the contents dictionary
                response = exa.search(
                    query,
                    num_results=3,
                    type="auto",
                    contents={"summary": True}  # triggers Gemini Flash summary generation per page
                )

                st.subheader("Results")
                    
                    # iterate through the returned results
                for i, result in enumerate(response.results):
                        # Use expanders to group each result neatly
                    with st.expander(f"{i+1}. {result.title or 'Untitled Page'}"):
                        st.markdown(f"**URL:** [{result.url}]({result.url})")
                            
                            # Access the summary from the result's summary field
                        if hasattr(result, 'summary') and result.summary:
                            st.markdown("### Summary")
                            st.write(result.summary)
                        else:
                            st.info("No summary generated for this page.")
                                
            except Exception as e:
                st.error(f"An error has occurred: {e}")
else:
    st.error("Please enter a query first.")
# #print(response) #Will print all info include score, id, author, etc
# for result in response.results:
#     print(f'Title: {result.title}')
#     print(f'URL: {result.url}')
#     print()