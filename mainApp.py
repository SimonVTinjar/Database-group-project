import streamlit as st
from views.home import show_home
from views.restaurants import show_restaurants
from views.menus import show_menus
from views.orders import show_orders
from db import get_connection

st.set_page_config(page_title="Restaurant Admin", page_icon="🍽️")

# -------------------- SESSION STATE --------------------
st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("page", "Hjem")

# -------------------- LOGIN --------------------
if not st.session_state.authenticated:
    st.title("🍽️ Adminpanel – Logg inn")
    username = st.text_input("Brukernavn")
    password = st.text_input("Passord", type="password")

    if st.button("Logg inn"):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, password FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and result[1] == password:  # ✅ dette er riktig
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.user_id = result[0]  # ✅ viktig for tilgang
            st.rerun()
        else:
            st.error("Feil brukernavn eller passord.")

else:
    # -------------------- SIDEPANEL --------------------
    st.sidebar.title("🧭 Navigasjon")
    side = st.sidebar.radio("Velg side:", ["Hjem", "Restauranter", "Menyer", "Bestillinger"])
    st.session_state.page = side

    # -------------------- HOVEDINNHOLD --------------------
    if side == "Hjem":
        show_home()
    elif side == "Restauranter":
        show_restaurants()
    elif side == "Menyer":
        show_menus()
    elif side == "Bestillinger":
        show_orders()

    # -------------------- LOGG UT --------------------
    if st.sidebar.button("Logg ut"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.rerun()
