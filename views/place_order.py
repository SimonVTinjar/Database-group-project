import streamlit as st
import pandas as pd
from db import get_connection

def place_order():
    st.title("🛒 Legg inn bestilling")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent kunder
    cursor.execute("SELECT userID, fName, lName FROM users")
    users = cursor.fetchall()
    user_map = {f"{u['fName']} {u['lName']} (ID: {u['userID']})": u["userID"] for u in users}
    selected_user_label = st.selectbox("Velg kunde", list(user_map.keys()))
    selected_user_id = user_map[selected_user_label]

    # Hent restauranter
    cursor.execute("""
        SELECT DISTINCT r.restaurantID, r.rName
        FROM restaurant r
        JOIN menu m ON r.restaurantID = m.restaurantID
    """)
    restaurants = cursor.fetchall()
    rest_map = {f"{r['rName']} (ID: {r['restaurantID']})": r['restaurantID'] for r in restaurants}
    selected_rest_label = st.selectbox("Velg restaurant", list(rest_map.keys()))
    selected_rest_id = rest_map[selected_rest_label]

    # Hent menyer
    cursor.execute("""
        SELECT menuID, menuName, price FROM menu WHERE restaurantID = %s
    """, (selected_rest_id,))
    menus = cursor.fetchall()
    menu_map = {f"{m['menuName']} - {m['price']:.2f} kr": m["menuID"] for m in menus}
    selected_menu_label = st.selectbox("Velg meny", list(menu_map.keys()))
    selected_menu_id = menu_map[selected_menu_label]

    # Valg: Skal bestillingen leveres?
    delivery = st.checkbox("🚚 Skal bestillingen leveres til kunden?")

    if st.button("📦 Bekreft bestilling"):
        # Registrer bestilling på valgt kunde
        cursor.execute("""
            INSERT INTO Ordered (userID, menuID, status)
            VALUES (%s, %s, 'Mottatt')
        """, (selected_user_id, selected_menu_id))
        order_id = cursor.lastrowid

        # Hvis levering: hent adresse og telefon fra valgt kunde
        if delivery:
            cursor.execute("SELECT phoneNr FROM users WHERE userID = %s", (selected_user_id,))
            user_info = cursor.fetchone()

            cursor.execute("""
                INSERT INTO Delivery (orderID, deliveryStatus, phoneNrUser)
                VALUES (%s, 'Under behandling', %s)
            """, (order_id, user_info["phoneNr"]))

        conn.commit()
        st.success(f"Bestilling for `{selected_user_label}` ble registrert! 🎉")

    cursor.close()
    conn.close()
