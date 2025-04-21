import streamlit as st
from views.home import show_home
from views.restaurants import show_restaurants
from views.menus import show_menus
from views.orders import show_orders
from db import get_connection
from views.place_order import place_order
from views.statistics import show_statistics
from views.deliveries import show_deliveries
from views.userpanel import show_userpanel


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
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT ResUserID, password, role FROM Restaurantadminuser WHERE ResUsername = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result and result["password"] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.ResUserID = result["ResUserID"]
            st.session_state.role = result["role"]
            st.rerun()
        else:
            st.error("Feil brukernavn eller passord.")

else:
    # -------------------- SIDEPANEL --------------------
    st.sidebar.title("🧭 Navigasjon")
    side = st.sidebar.radio("Navigasjon", ["Hjem", "Restauranter","Userpanel", "Menyer", "Bestillinger", "Ny bestilling", "Statistikk", "Levering"])


    st.session_state.page = side

    # -------------------- HOVEDINNHOLD --------------------
    if side == "Hjem":
        show_home()
    elif side == "Restauranter":
        show_restaurants()
    elif side == "Userpanel":
        show_userpanel()
    elif side == "Menyer":
        show_menus()
    elif side == "Bestillinger":
        show_orders()
    elif side == "Ny bestilling":
        place_order()
    elif side == "Statistikk":
        show_statistics()
    elif side == "Levering":
        show_deliveries()


    # -------------------- LOGG UT --------------------
    if st.sidebar.button("Logg ut"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.user_id = None
        st.rerun()
