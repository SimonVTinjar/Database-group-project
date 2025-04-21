import streamlit as st
import pandas as pd
from db import get_connection

def show_orders():
    st.title("📦 Bestillinger")

    user_id = st.session_state.get("ResUserID")  # bruker Restaurantadminuser ID
    if user_id is None:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restaurant-IDene brukeren har tilgang til
    cursor.execute("""
        SELECT restaurantID FROM restaurantadmin WHERE ResUserID = %s
    """, (user_id,))
    restaurant_ids = [row["restaurantID"] for row in cursor.fetchall()]

    if not restaurant_ids:
        st.warning("Du har ikke tilgang til noen restauranter.")
        return

    placeholders = ",".join(["%s"] * len(restaurant_ids))
    cursor.execute(f"""
        SELECT o.orderID, o.orderTime, o.status,
               ru.ResUsername AS customer,
               m.menuName, m.price,
               r.rName AS restaurant
        FROM Ordered o
        JOIN restaurantadminuser ru ON o.userID = ru.ResUserID
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE m.restaurantID IN ({placeholders})
        ORDER BY o.orderTime DESC
    """, tuple(restaurant_ids))

    orders = cursor.fetchall()
    if not orders:
        st.info("Ingen bestillinger funnet.")
        return

    for order in orders:
        with st.expander(f"📦 Bestilling #{order['orderID']} – {order['restaurant']}"):
            st.write(f"**Tid:** {order['orderTime']}")
            st.write(f"**Kunde:** {order['customer']}")
            st.write(f"**Meny:** {order['menuName']} – {order['price']} kr")
            st.write(f"**Status nå:** `{order['status']}`")

            new_status = st.selectbox(
                "Endre status", 
                ["Mottatt", "Underveis", "Levert"],
                index=["Mottatt", "Underveis", "Levert"].index(order["status"]),
                key=f"status_{order['orderID']}"
            )

            if st.button("💾 Oppdater status", key=f"save_{order['orderID']}"):
                update_cursor = conn.cursor()
                update_cursor.execute("""
                    UPDATE Ordered SET status = %s WHERE orderID = %s
                """, (new_status, order["orderID"]))
                conn.commit()
                update_cursor.close()
                st.success("Status oppdatert!")
                st.rerun()

    cursor.close()
    conn.close()
