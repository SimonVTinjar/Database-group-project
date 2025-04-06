import streamlit as st
import numpy as np
import pandas as pd
import datetime
from datetime import time, timedelta


from db import get_connection

st.write("Hello World")
st.subheader("Restaurants")

#################### Sets up menu table######################
conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM restaurants")
rows = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
cursor.close()
conn.close()
##############################################################


if "show_form" not in st.session_state:
    st.session_state.show_form = False

if st.button("Add New Restaurant:"):
    st.session_state.show_form = not st.session_state.show_form

if st.session_state.show_form:

    st.subheader("Add New Restaurant")

    with st.form("add_new_restaurant"):
        rName = st.text_input("Restaurant Name")
        address = st.text_input("Address")
        phoneNr = st.text_input("Phone number")
        openingTime = st.time_input("Opening Time", value=datetime.time(10, 0))
        closingTime = st.time_input("Closing Time", value = datetime.time(22, 0))
        submitted = st.form_submit_button("Add Restaurant")

        if submitted:
            if not rName.strip() or not address.strip() or not phoneNr.strip():
                st.error("Please fill out all fields")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO restaurants (rName, address, phoneNr, openingTime, closingTime)
                VALUES (%s, %s, %s, %s, %s)
                """, (rName, address, phoneNr, openingTime, closingTime))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"'{rName}' added successfully!")

# Format TIME fields as strings
formatted_rows = []
for row in rows:
    row = list(row)
    for i, value in enumerate(row):
        if isinstance(value, (time, timedelta)):
            try:
                row[i] = value.strftime("%H:%M")
            except:
                row[i] = str(value)
    formatted_rows.append(row)

# Show table
df = pd.DataFrame(formatted_rows, columns=column_names)
st.table(df)