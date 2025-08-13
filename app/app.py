"""
Main/entrypoint app file.
"""

import streamlit as st

page = st.Page("./pages/home.py", default=True)
st.navigation([page]).run()

