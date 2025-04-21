import streamlit as st
import pandas as pd
from db import get_connection

def show_userpanel():
    st.title("👤 Brukerpanelet")
    st.write(f"Logget inn som: `{st.session_state.username}`")

    col1, col2 = st.columns([1, 5])
    if col1.button("Logg ut", key="logout_btn"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    if col2.button("Endre passord", key="change_pw_btn"):
        st.session_state.show_password_change = not st.session_state.get("show_password_change", False)
        st.session_state.show_delete_form = False

    if st.button("Slett min bruker", key="delete_user_btn"):
        st.session_state.show_delete_form = not st.session_state.get("show_delete_form", False)
        st.session_state.show_password_change = False

    # Endre passord
    if st.session_state.get("show_password_change"):
        st.subheader("🔐 Endre passord")
        old_password = st.text_input("Nåværende passord", type="password", key="old_pw")
        new_password = st.text_input("Nytt passord", type="password", key="new_pw")

        if st.button("Oppdater passord", key="update_pw_btn"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM restaurantadminuser WHERE ResUsername = %s", (st.session_state.username,))
            result = cursor.fetchone()

            if result and result[0] == old_password:
                cursor.execute("UPDATE restaurantadminuser SET password = %s WHERE ResUsername = %s", (new_password, st.session_state.username))
                conn.commit()
                st.success("✅ Passord oppdatert!")
            else:
                st.error("❌ Feil nåværende passord.")
            cursor.close()
            conn.close()

    # Slett bruker
    if st.session_state.get("show_delete_form"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM restaurantadminuser WHERE ResUsername = %s", (st.session_state.username,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Brukeren er slettet.")
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()

    # Vis brukerinformasjon
    st.subheader("📋 Min konto")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurantadminuser WHERE ResUsername = %s", (st.session_state.username,))
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=column_names)
    if 'password' in df.columns:
        df['password'] = '*****'
    st.table(df)
