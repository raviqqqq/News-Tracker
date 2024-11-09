#Note: werkzeug version 2.1.2 has been used, since the latest version causes issues
import streamlit as st
from script import news_search
import pandas as pd

#Page Data
st.markdown("""# Track The Scent""")

st.markdown("""This app allows you to obtain the most recent news information from various sources. Customize the news you want be the source, topic or even filter it by a keyword. 
        However, the articles may take some time to load, especially when all sources are selected. So remember, patience is a virtue!""")

#Taking keyword to search news by
st.text_input("Enter a keyword",key = "keyword")

#Creating 2 sections for user inputs
col1, col2 = st.columns(2)
with col1:
    #Domain selection by the user
    st.selectbox(
    "Select a source",
    ("All","New York Times","Times of India","Hindustan Times","The Hindu","CNN","BBC","The Guardian"),
    key = 'source_page2'
    )

with col2:
    #Domain selection by the user
    st.selectbox(
        "Select a domain",
        ("Headlines","Tech", "Business","Science","Sport","Entertainment","Lifestyle"),
        key = "domain"
    )

#Button Click Definition
if st.button("Search!"):
    #Create a dataframe with the results from the news search, and print them
    df = news_search(keyword = st.session_state.keyword, domain = st.session_state.domain, source_site=st.session_state.source_page2)

    #df = news_search(keyword = st.session_state.keyword)
    st.dataframe(df)    