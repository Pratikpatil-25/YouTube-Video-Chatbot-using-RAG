import streamlit as st
from components.upload import render_uploader
from components.download_history import render_history_download
from components.ChatUI import render_chat


st.set_page_config(page_title="AI YouTube Video Assistant",layout="wide")
st.title(" 🤖 YouTube Video Assistant Chatbot")


render_uploader()
render_chat()
render_history_download()