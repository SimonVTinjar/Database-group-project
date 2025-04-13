import streamlit as st
import pandas as pd
import numpy as np

## .\.venv\Scripts\Activate.ps1     - Tror denne må kjøres for å kunne kjøre appen, litt usikker
## .\\venv\Scripts\Activate.ps1

## streamlit run app.py i terminal

# Definerer forskjellige sider
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("page_2.py", title="Page 2", icon="❄️")
page_3 = st.Page("page_3.py", title="Page 3", icon="🎉")

pg = st.navigation([main_page, page_2, page_3])

pg.run()

#aa

# Rullegardin på venstresiden
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home Phone', 'Mobile Phone')
)


