import streamlit as st
import os
from datetime import datetime

from RetrivalQABackend import get_answer, load_and_process_urls

st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .delete-btn > button {
        background-color: #f44336;
    }
    .delete-btn > button:hover {
        background-color: #d32f2f;
    }
    .url-card {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        border-left: 4px solid #4CAF50;
    }
    .url-input {
        margin-bottom: 15px;
    }
    .answer-container {
        background-color: #f0f7ff;
        border-left: 4px solid #1e88e5;
        padding: 20px;
        border-radius: 5px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .source-container {
        background-color: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .header-container {
        background-color: #f1f3f4;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .subheader {
        color: #2e7d32;
        font-size: 1.5rem;
        margin-bottom: 15px;
    }
    .step-counter {
        background-color: #4CAF50;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-right: 10px;
    }
    .progress-container {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .status-message {
        margin-top: 5px;
        font-style: italic;
        color: #666;
    }
    .api-key-input {
        margin: 20px 0;
    }
    .footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        text-align: center;
        color: #666;
    }
    .question-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <h1 style="text-align: center;">🔍 Web Content Q&A Tool</h1>
    <p style="text-align: center; font-size: 1.2rem;">Extract information from websites and ask questions about their content</p>
</div>
""", unsafe_allow_html=True)


if 'urls' not in st.session_state:
    st.session_state.urls = []
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

with st.sidebar:

    st.markdown("### Configuration")

    # with st.expander("API Settings", expanded=not st.session_state.api_key_set):
    #     st.markdown("##### OpenAI API Key")
    #     api_key = st.text_input("Enter your API key:", type="password", key="api_key_input")
    #
    #     col1, col2 = st.columns([1, 1])
    #     with col1:
    #         save_key = st.button("Save Key")
    #     with col2:
    #         clear_key = st.button("Clear Key")
    #
    #     if save_key:
    #         if api_key:
    #             os.environ["OPENAI_API_KEY"] = api_key
    #             st.session_state.api_key_set = True
    #             st.success("✅ API key set successfully!")
    #         else:
    #             st.error("⚠️ Please enter a valid API key")
    #
    #     if clear_key:
    #         if "api_key_input" in st.session_state:
    #             st.session_state["api_key_input"] = ""
    #         if "OPENAI_API_KEY" in os.environ:
    #             del os.environ["OPENAI_API_KEY"]
    #         st.session_state.api_key_set = False
    #         st.warning("API key cleared")

    with st.expander("Help & About", expanded=False):
        st.markdown("""
        ### How to use:
        1. Enter your OpenAI API key
        2. Add URLs to analyze
        3. Process the URLs
        4. Ask questions about the content

        ### About:
        This tool uses LangChain and OpenAI to extract and analyze web content. It processes the text from web pages and allows you to ask questions about the content without relying on general knowledge.
        """)

if st.session_state.api_key_set:
    st.markdown('<div class="subheader"><span class="step-counter">1</span>Add URLs to Analyze</div>',
                unsafe_allow_html=True)

    url_input = st.text_input(
        "Enter a URL:",
        key="url_input",
        placeholder="https://example.com",

    )
    add_url = st.button("➕ Add URL")

    if add_url:
        if url_input:
            if url_input not in st.session_state.urls:
                st.session_state.urls.append(url_input)
                st.success(f"✅ URL added: {url_input}")
                st.session_state.processing_complete = False
            else:
                st.warning("⚠️ This URL has already been added.")
        else:
            st.warning("⚠️ Please enter a URL.")

    if st.session_state.urls:
        st.markdown("### Added URLs")
        st.info("You can add more URLs to the same field and click add to add multiple urls.")

        for i, url in enumerate(st.session_state.urls):
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f'<div class="url-card">{url}</div>', unsafe_allow_html=True)
                with col2:
                    if st.button("Remove", key=f"remove_{i}", help="Remove this URL"):
                        st.session_state.urls.pop(i)
                        st.session_state.processing_complete = False
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.urls:
        st.markdown('<div class="subheader"><span class="step-counter">2</span>Process URLs</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns([1, 5])
        with col1:
            process_button = st.button("🔄 Process", use_container_width=True,
                                       help="Extract and analyze content from the URLs")
        with col2:
            if not st.session_state.processing_complete:
                st.markdown('<div class="status-message">URLs need to be processed before asking questions</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-message">✅ URLs processed successfully</div>',
                            unsafe_allow_html=True)

        if process_button:
            with st.spinner("Loading and processing URLs..."):
                        vector_store, error = load_and_process_urls(st.session_state.urls)
                        if error:
                            st.error(f"⚠️ {error}")
                        else:
                            st.session_state.vector_store = vector_store
                            st.session_state.processing_complete = True
                            st.success("✅ URLs processed successfully!")

    if st.session_state.processing_complete and st.session_state.vector_store:
        st.markdown('<div class="subheader"><span class="step-counter">3</span>Ask Questions</div>',
                    unsafe_allow_html=True)

        with st.container():
            question = st.text_input(
                "Ask a question about the content:",
                key="question_input",
                placeholder="What are the main topics discussed in these websites?",
            )
            col1, col2 = st.columns([1, 5])
            with col1:
                ask_button = st.button("🔍 Ask", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if ask_button and question:
            with st.spinner("Generating answer..."):
                result = get_answer(st.session_state.vector_store, question)

                st.session_state.qa_history.append((question, result["result"]))


                st.markdown("### Answer")
                st.markdown(result["result"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("### Sources")
                for i, doc in enumerate(result["source_documents"]):
                    with st.expander(f"Source {i + 1}"):
                        st.markdown(f"**Content Extract:**")
                        st.markdown(doc.page_content)
                        if hasattr(doc.metadata, 'source') and doc.metadata.get('source'):
                            st.markdown(f"**Source URL:** {doc.metadata.get('source', 'Unknown')}")
                        st.markdown('</div>', unsafe_allow_html=True)

        elif ask_button:
            st.warning("⚠️ Please enter a question.")
else:
    st.switch_page("SetKeyUI.py")

st.markdown("""
<div class="footer">
    <p>Built with Streamlit, LangChain, and OpenAI | Web Content Q&A Tool</p>
</div>
""", unsafe_allow_html=True)