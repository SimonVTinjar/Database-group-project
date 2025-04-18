import streamlit as st
import pandas as pd
import datetime
from db import get_connection

def show_restaurants():
    st.title("🏢 Dine restauranter")

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("Du må være innlogget for å se restauranter.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor()

    # Hent restauranter som brukeren har tilgang til
    cursor.execute("""
        SELECT r.*
        FROM restaurant_admins ra
        JOIN restaurant r ON ra.restaurantID = r.restaurantID
        WHERE ra.user_id = %s
    """, (user_id,))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

    # Formatér tid
    df["openingTime"] = df["openingTime"].apply(lambda t: f"{int(t.seconds//3600):02d}:{int((t.seconds%3600)//60):02d}")
    df["closingTime"] = df["closingTime"].apply(lambda t: f"{int(t.seconds//3600):02d}:{int((t.seconds%3600)//60):02d}")

    st.subheader("📋 Dine restauranter")
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
                cursor.execute("""
                    INSERT INTO restaurant (rName, address, phoneNr, openingTime, closingTime)
                    VALUES (%s, %s, %s, %s, %s)
                """, (rName, address, phoneNr, openingTime, closingTime))
                restaurant_id = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO restaurant_admins (restaurantID, user_id)
                    VALUES (%s, %s)
                """, (restaurant_id, user_id))

                conn.commit()
                st.success(f"{rName} ble lagt til og koblet til brukeren din.")
                st.rerun()

    st.subheader("🗑️ Slett restaurant")
    if not df.empty:
        selected_id = st.selectbox("Velg restaurant-ID for sletting", df["restaurantID"].tolist())
        if st.button("Slett valgt restaurant"):
            cursor.execute("DELETE FROM restaurant_admins WHERE restaurantID = %s AND user_id = %s", (selected_id, user_id))
            cursor.execute("DELETE FROM restaurant WHERE restaurantID = %s", (selected_id,))
            conn.commit()
            st.success("Restaurant slettet.")
            st.rerun()

    st.subheader("👥 Administrer brukertilgang")
    if not df.empty:
        selected_id = st.selectbox("Velg restaurant-ID for å administrere brukere", df["restaurantID"].tolist(), key="admin_user")

        # Legg til bruker
        new_user_id = st.number_input("Bruker-ID som skal få tilgang", min_value=1, step=1, key="user_add")
        if st.button("Gi tilgang til restaurant"):
            try:
                cursor.execute("INSERT INTO restaurant_admins (restaurantID, user_id) VALUES (%s, %s)", (selected_id, new_user_id))
                conn.commit()
                st.success("Bruker lagt til!")
            except:
                st.warning("Brukeren har kanskje allerede tilgang.")

        # Fjern bruker
        # Vis brukere knyttet til restauranten (unntatt superadmin)
        cursor.execute("""SELECT u.userID, u.username FROM restaurant_admins ra
        JOIN users u ON ra.user_id = u.userID
        WHERE ra.restaurantID = %s AND u.userID != 1
        """, (selected_id,))


        admins = cursor.fetchall()
        if admins:
            admin_map = {f"{a[1]} (ID: {a[0]})": a[0] for a in admins if a[0] != user_id}
            if admin_map:
                user_to_remove = st.selectbox("Fjern tilgang for:", list(admin_map.keys()))
                if st.button("Fjern tilgang"):
                    cursor.execute("DELETE FROM restaurant_admins WHERE restaurantID = %s AND user_id = %s", (selected_id, admin_map[user_to_remove]))
                    conn.commit()
                    st.success("Bruker fjernet.")
                    st.rerun()

    cursor.close()
    conn.close()
