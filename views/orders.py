import streamlit as st
import pandas as pd
from db import get_connection

def show_orders():
    st.title("📦 Innkommende bestillinger")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")  # Antar en 'orders'-tabell
    orders = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    if orders:
        df = pd.DataFrame(orders, columns=colnames)
        st.dataframe(df)
    else:
        st.info("Ingen bestillinger å vise.")
