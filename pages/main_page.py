import streamlit as st
import numpy as np
import pandas as pd

#Main Page Content
if not st.session_state.get("authenticated"):
    st.warning("Du må være logget inn for å se denne siden.")
    st.stop()

st.title("VELKOMMEN YA FILTHY ANIMAL")
st.sidebar.markdown("# Main page")

st.image("asdasdasd.gif")



