import streamlit as st

TITLE = "Experiments"
st.set_page_config(page_title=TITLE, page_icon="📈", layout="wide")
st.sidebar.header(TITLE)

tabs = st.tabs(["0"])

with tabs[0]:
    st.write("## (Experiments)")
