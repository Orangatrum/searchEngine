from exa_py import Exa
import streamlit as st
exa = Exa('0efcc52e-a70c-42d7-8308-9543fdd710b1') #importing Exa with the API key
st.write("hello")
query = st.text_input("Enter your query: ") #taking input from the user using streamlit
response = exa.search(
    query, # search query 
    type = 'keyword', #search method
    user_location = 'US',
    moderation = True,
    num_results = 10, # number of results
    )

# #print(response) #Will print all info include score, id, author, etc
# for result in response.results:
#     print(f'Title: {result.title}')
#     print(f'URL: {result.url}')
#     print()