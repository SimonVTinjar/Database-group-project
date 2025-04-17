import streamlit as st
import pandas as pd
import datetime
from db import get_connection

def show_restaurants():
    st.title("🏢 Dine restauranter")

    # Krever at bruker er innlogget og har user_id
    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("Du må være innlogget for å se restauranter.")
        st.stop()

    # Hent restauranter brukeren har tilgang til
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT r.*
        FROM restaurant_admins ra
        JOIN restaurant r ON ra.restaurantID = r.restaurantID
        WHERE ra.user_id = %s
    """, (user_id,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=columns)
    st.table(df)

    st.subheader("➕ Legg til ny restaurant")
    with st.form("add_restaurant"):
        rName = st.text_input("Navn")
        address = st.text_input("Adresse")
        phoneNr = st.text_input("Telefon")
        openingTime = st.time_input("Åpningstid", value=datetime.time(10, 0))
        closingTime = st.time_input("Stengetid", value=datetime.time(22, 0))
        submit = st.form_submit_button("Legg til")

        if submit:
            if not all([rName.strip(), address.strip(), phoneNr.strip()]):
                st.error("Fyll ut alle felt.")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO restaurant (rName, address, phoneNr, openingTime, closingTime)
                    VALUES (%s, %s, %s, %s, %s)
                """, (rName, address, phoneNr, openingTime, closingTime))
                restaurant_id = cursor.lastrowid

                # Gi tilgang til den nye restauranten
                cursor.execute("""
                    INSERT INTO restaurant_admins (restaurantID, user_id)
                    VALUES (%s, %s)
                """, (restaurant_id, user_id))

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"{rName} ble lagt til og koblet til brukeren din.")
                st.rerun()

    st.subheader("🗑️ Slett restaurant")
    if len(df) > 0:
        restaurant_ids = df["restaurantID"].tolist()
        selected_id = st.selectbox("Velg restaurant-ID", restaurant_ids)
        if st.button("Slett valgt restaurant"):
            conn = get_connection()
            cursor = conn.cursor()
            # Slett fra admin-tilgang først
            cursor.execute("DELETE FROM restaurant_admins WHERE restaurantID = %s AND user_id = %s", (selected_id, user_id))
            # Slett selve restauranten (CASCADE vil ta resten)
            cursor.execute("DELETE FROM restaurant WHERE restaurantID = %s", (selected_id,))
            conn.commit()
            cursor.close()
            conn.close()
            st.success("Restaurant slettet.")
            st.rerun()
