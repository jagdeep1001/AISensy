import os

import streamlit as st
import os


def set_key():
    st.markdown("""
    <style>
        .header-container {
        background-color: #f1f3f4;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
               <style>
               .welcome-container {
                   text-align: center;
                   padding: 1.5rem;
                   background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                   border-radius: 1rem;
                   margin: 1rem auto;
                   max-width: 600px;
               }
               .welcome-header {
                   color: #2c3e50;
                   font-size: 2.2rem;
                   margin-bottom: 0.5rem;
                   font-weight: 600;
               }
               .welcome-subheader {
                   color: #34495e;
                   font-size: 1.1rem;
                   margin-bottom: 1.5rem;
               }
               .action-card {
                   background: white;
                   padding: 1.2rem;
                   border-radius: 0.5rem;
                   box-shadow: 0 3px 6px rgba(0,0,0,0.1);
                   text-align: center;
                   transition: transform 0.2s;
                   margin-bottom: 15px;
               }
               .action-card:hover {
                   transform: translateY(-3px);
               }
               .stButton {
                   margin-top: 10px;
                   width: 100%;
               }
               .action-card p {
                   margin-bottom: 10px;
                   font-size: 0.9rem;
                   color: #555;
               }
               .action-card h4 {
                   font-size: 1.2rem;
               }
               </style>
           """, unsafe_allow_html=True)

    st.markdown("""
    <div class="header-container">
        <h1 style="text-align: center;">🔍 Web Content Q&A Tool</h1>
        <p style="text-align: center; font-size: 1.2rem;">Extract information from websites and ask questions about their content</p>
    </div>
    """, unsafe_allow_html=True)
    api_key_set = "OPENAI_API_KEY" in os.environ and os.environ["OPENAI_API_KEY"]

    if api_key_set:
        st.success("✅ API key set successfully!")
        with st.sidebar:
            if st.button("Clear Key"):
                del os.environ["OPENAI_API_KEY"]
                st.session_state.api_key_set = False
                st.warning("API key cleared! Please refresh the page.")
                st.rerun()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                        <div class='action-card'>
                            <h3>Q&A using Retrival QA</h3>
                            <p>Implements Retrival QA to answer questions</p>
                            """, unsafe_allow_html=True)
            st.markdown("""
                        <style>
                        div[data-testid="stButton"] {
                            margin-top: -40px;
                            margin-bottom: 20px;
                            padding: 0 20px;
                        }
                        </style>
                    """, unsafe_allow_html=True)
            if st.button("Try Out", key="retrivalButton"):
                st.switch_page("RetrivalQAUI.py")

        with col2:
            st.markdown("""
                        <div class='action-card'>
                            <h3>Q&A Using Stuff Chain</h3>
                            <p>Implements Stuff Chain to answer questions</p>
                            """, unsafe_allow_html=True)
            st.markdown("""
                        <style>
                        div[data-testid="stButton"] {
                            margin-top: -40px;
                            margin-bottom: 20px;
                            padding: 0 20px;
                        }
                        </style>
                    """, unsafe_allow_html=True)
            if st.button("Try Out", key="stuffButton"):
                st.switch_page("StuffChainUI.py")

    else:
        st.info("Please Enter Your OpenAI API Key to get Started!")
        api_key = st.text_input("Enter your API key:", type="password", key="api_key_input")

        if st.button("Save Key"):
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
                st.session_state.api_key_set = True
                st.success("✅ API key set successfully! ")
                st.rerun()
            else:
                st.error("⚠️ Please enter a valid API key")


set_key()

