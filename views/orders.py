import streamlit as st
import pandas as pd
from db import get_connection

def show_orders():
    st.title("📦 Bestillinger")

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restaurantID-er brukeren har tilgang til
    cursor.execute("""
        SELECT restaurantID
        FROM restaurant_admins
        WHERE user_id = %s
    """, (user_id,))
    restaurant_ids = [row["restaurantID"] for row in cursor.fetchall()]

    if not restaurant_ids:
        st.warning("Du har ikke tilgang til noen restauranter.")
        return

    # Hent bestillinger for disse restaurantene
    cursor.execute("""
        SELECT o.orderID, o.orderTime, o.status,
               u.username AS customer,
               m.menuName, m.price,
               r.rName AS restaurant
        FROM orders o
        JOIN users u ON o.userID = u.user_id
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE m.restaurantID IN (%s)
        ORDER BY o.orderTime DESC
    """ % ",".join(["%s"] * len(restaurant_ids)), tuple(restaurant_ids))

    orders = cursor.fetchall()
    if not orders:
        st.info("Ingen bestillinger funnet.")
    else:
        df = pd.DataFrame(orders)
        st.dataframe(df)

    cursor.close()
    conn.close()