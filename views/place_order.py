import streamlit as st
import pandas as pd
from db import get_connection

def place_order():
    st.title("🛒 Legg inn bestilling")

    user_id = st.session_state.get("ResUserID")  # Bruk riktig ID fra session
    if user_id is None:
        st.error("Du må være logget inn for å bestille.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restauranter som har menyer
    cursor.execute("""
        SELECT DISTINCT r.restaurantID, r.rName
        FROM restaurant r
        JOIN menu m ON r.restaurantID = m.restaurantID
    """)
    restaurants = cursor.fetchall()
    if not restaurants:
        st.warning("Ingen restauranter tilgjengelig med menyer.")
        return

    rest_map = {f"{r['rName']} (ID: {r['restaurantID']})": r['restaurantID'] for r in restaurants}
    selected_rest = st.selectbox("Velg restaurant", list(rest_map.keys()))
    selected_rest_id = rest_map[selected_rest]

    # Hent menyer fra valgt restaurant
    cursor.execute("""
        SELECT menuID, menuName, price, description
        FROM menu
        WHERE restaurantID = %s
    """, (selected_rest_id,))
    menus = cursor.fetchall()

    if not menus:
        st.info("Denne restauranten har ingen menyer.")
        return

    menu_map = {f"{m['menuName']} - {m['price']} kr": m["menuID"] for m in menus}
    selected_menu = st.selectbox("Velg meny", list(menu_map.keys()))
    selected_menu_id = menu_map[selected_menu]

    if st.button("📦 Bekreft bestilling"):
        cursor.execute("""
            INSERT INTO Ordered (userID, menuID, status)
            VALUES (%s, %s, 'Mottatt')
        """, (user_id, selected_menu_id))
        conn.commit()
        st.success("Bestilling er registrert! 🎉")

    cursor.close()
    conn.close()
