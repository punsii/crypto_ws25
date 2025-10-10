import pandas as pd
import scipy
import streamlit as st
from numpy.random import default_rng as rng

st.set_page_config(
    page_title="Kryptographie",
    page_icon="",
    initial_sidebar_state="expanded",
)
st.sidebar.success("Select a chapter above.")

# st.markdown(
#     "[![GitHub](https://img.shields.io/badge/github-%2523121011.svg?style=for-the-badge&logo=github&color=AB00AB)]()"
# )

st.markdown(
    """
   <===== Pick an exercise page in the sidebar
"""
)

variance = st.slider("Variance", 0, 100)


df = pd.DataFrame(scipy.stats.Normal.pdf([x for x in range(0, 100)], 1))

st.line_chart(df)
