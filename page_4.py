import streamlit as st
import numpy as np
import pandas as pd
from db import get_connection

if not st.session_state.get("authenticated"):
    st.warning("Du må være logget inn for å se denne siden.")
    st.stop()

st.write("Hello World")
st.subheader("User")

#################### Funksjon for å hente brukere ######################
def get_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    df = pd.DataFrame(rows, columns=column_names)
    # Skjul passord
    if 'password' in df.columns:
        df['password'] = '*****'
    return df

#################### Initial state ######################
if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "show_delete_form" not in st.session_state:
    st.session_state.show_delete_form = False

if "show_password_change" not in st.session_state:
    st.session_state.show_password_change = False

#################### Knapper ######################
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add New user"):
        st.session_state.show_form = not st.session_state.show_form
        st.session_state.show_delete_form = False
        st.session_state.show_password_change = False

with col2:
    if st.button("Delete a user"):
        st.session_state.show_delete_form = not st.session_state.show_delete_form
        st.session_state.show_form = False
        st.session_state.show_password_change = False

with col3:
    if st.button("Change password"):
        st.session_state.show_password_change = not st.session_state.show_password_change
        st.session_state.show_form = False
        st.session_state.show_delete_form = False

##################### Add new user ############################
if st.session_state.show_form:
    st.subheader("Add New User")

    with st.form("add_new_User"):
        username = st.text_input("Username")
        address = st.text_input("Address")
        fName = st.text_input("First Name")
        lName = st.text_input("Last Name")
        phoneNr = st.text_input("Phone Number")
        email = st.text_input("E-mail")
        password = st.text_input("Password")
        submitted = st.form_submit_button("Add New user")

        if submitted:
            if not username.strip() or not fName.strip() or not lName.strip() or not address.strip() or not phoneNr.strip() or not email.strip() or not password.strip():
                st.error("Please fill out all fields")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (username, fName, lname, address, phoneNr, email, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (username, fName, lName, address, phoneNr, email, password))
                conn.commit()
                cursor.close()
                conn.close()
                st.success(f"'{username}' added successfully!")

########################### Delete a user #######################
if st.session_state.show_delete_form:
    st.subheader("Delete a User")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    selected_user = st.selectbox("Select user to delete", usernames)

    if st.button("Confirm Delete"):
        if selected_user:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = %s", (selected_user,))
            conn.commit()
            cursor.close()
            conn.close()
            st.success(f"User '{selected_user}' was deleted successfully!")

##################### Endre passord ############################
if st.session_state.show_password_change:
    st.subheader("Change Password")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    usernames = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    selected_user_pw = st.selectbox("Select user", usernames, key="pw_user_select")
    old_password = st.text_input("Current password", type="password")
    new_password = st.text_input("New password", type="password")

    if st.button("Update Password"):
        if not old_password.strip() or not new_password.strip():
            st.error("Please fill out both password fields.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (selected_user_pw,))
            result = cursor.fetchone()

            if result and result[0] == old_password:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, selected_user_pw))
                conn.commit()
                st.success(f"Password for '{selected_user_pw}' was updated!")
            else:
                st.error("Incorrect current password.")
            
            cursor.close()
            conn.close()
########################### Vis brukertabellen #######################
df = get_users()
st.table(df)
