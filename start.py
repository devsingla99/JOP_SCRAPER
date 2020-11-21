import streamlit as st
st.header("WELCOME TO JOB SCRAPER AND CRAWLER")
st.sidebar.header("WELCOME TO JOB SCRAPER AND CRAWLER")
import app
import main
PAGES = {
    "Scraping and Visualization": main,
    "Crawling": app
}
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app1()
# if a=="Scraping and Visualization":
#     from main import *
# else:
#     from app import *