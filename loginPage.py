import streamlit as st
import pandas as pd
from db import get_connection

# Init session state
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")

# ------------------ Brukerpanel ------------------
def show_user_app():
    st.title("Brukerpanel")
    st.write(f"Logget inn som: {st.session_state.username}")

    def get_users():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (st.session_state.username,))
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()
        df = pd.DataFrame(rows, columns=column_names)
        if 'password' in df.columns:
            df['password'] = '*****'
        return df

    col1, col2 = st.columns([1, 5])
    if col1.button("Logg ut"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()


    if "show_delete_form" not in st.session_state:
        st.session_state.show_delete_form = False
    if "show_password_change" not in st.session_state:
        st.session_state.show_password_change = False

    if col2.button("Endre passord"):
        st.session_state.show_password_change = not st.session_state.show_password_change
        st.session_state.show_delete_form = False

    if st.button("Slett min bruker"):
        st.session_state.show_delete_form = not st.session_state.show_delete_form
        st.session_state.show_password_change = False

    # Passord-endring
    if st.session_state.show_password_change:
        st.subheader("Endre passord")
        old_password = st.text_input("Nåværende passord", type="password")
        new_password = st.text_input("Nytt passord", type="password")

        if st.button("Oppdater passord"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (st.session_state.username,))
            result = cursor.fetchone()

            if result and result[0] == old_password:
                cursor.execute("UPDATE users SET password = %s WHERE username = %s", (new_password, st.session_state.username))
                conn.commit()
                st.success("Passord oppdatert!")
            else:
                st.error("Feil passord.")
            cursor.close()
            conn.close()

    # Slett bruker
    if st.session_state.show_delete_form:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (st.session_state.username,))
        conn.commit()
        cursor.close()
        conn.close()
        st.success("Brukeren er slettet.")
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()


    st.subheader("Min konto")
    st.table(get_users())


# ------------------ Innloggingsside ------------------
if not st.session_state.authenticated:
    st.title("Velkommen!")
    choice = st.radio("Velg handling:", ["Logg inn", "Registrer ny konto"])

    if choice == "Logg inn":
        st.subheader("Logg inn")
        username = st.text_input("Brukernavn")
        password = st.text_input("Passord", type="password")

        if st.button("Logg inn"):
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()

            if result and result[0] == password:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()

            else:
                st.error("Feil brukernavn eller passord.")

    elif choice == "Registrer ny konto":
        st.subheader("Registrer ny konto")
        with st.form("registration_form"):
            new_username = st.text_input("Brukernavn")
            new_password = st.text_input("Passord", type="password")
            confirm_password = st.text_input("Bekreft passord", type="password")
            fName = st.text_input("Fornavn")
            lName = st.text_input("Etternavn")
            address = st.text_input("Adresse")
            phoneNr = st.text_input("Telefonnummer")
            email = st.text_input("E-post")

            register = st.form_submit_button("Opprett konto")

            if register:
                if not all([new_username, new_password, confirm_password, fName, lName, address, phoneNr, email]):
                    st.error("Alle felt må fylles ut.")
                elif new_password != confirm_password:
                    st.error("Passordene matcher ikke.")
                else:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE username = %s", (new_username,))
                    if cursor.fetchone():
                        st.error("Brukernavnet er allerede i bruk.")
                    else:
                        cursor.execute("""
                            INSERT INTO users (username, password, fName, lName, address, phoneNr, email)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (new_username, new_password, fName, lName, address, phoneNr, email))
                        conn.commit()
                        st.success("Konto opprettet! Du kan nå logge inn.")
                    cursor.close()
                    conn.close()

# ------------------ Vis brukerpanel om innlogget ------------------
if st.session_state.authenticated:
    show_user_app()
