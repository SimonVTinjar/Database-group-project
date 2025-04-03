import streamlit as st
import numpy as np
import pandas as pd

st.write("Hello World")

#Basic tabellen
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

df

#Random tabell med randome gule markeringer
dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))

# Vet ikke, var i tutorialen
tabletry = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(tabletry)