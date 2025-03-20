import streamlit as st

st.set_page_config(
    page_title="Web Content Q&A Tool",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_key=st.Page(
    page="SetKeyUI.py",
    title="Set API Key",
    icon="🔍",
)
retrivalQA = st.Page(
    page="RetrivalQAUI.py",
    title="Using Retrival Q&A Langchain Implementation",
    icon="🔍",
)

StuffChain = st.Page(
    page="StuffChainUI.py",
    title="Using Stuff Chain Implementation",
    icon="🔍",
)

pg = st.navigation(
    {
        "User Dashboard": [set_key],
        "Q&A": [retrivalQA,StuffChain],

    })

pg.run()