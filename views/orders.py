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
               u.username AS customer,
               m.menuName, m.price,
               r.rName AS restaurant
        FROM Ordered o
        JOIN users u ON o.userID = u.userID
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE m.restaurantID IN ({placeholders})
        ORDER BY o.orderTime DESC
    """, tuple(restaurant_ids))

    orders = cursor.fetchall()
    if not orders:
        st.info("Ingen bestillinger funnet.")
        return

    df = pd.DataFrame(orders)
    df["orderTime"] = pd.to_datetime(df["orderTime"]).dt.strftime("%Y-%m-%d %H:%M")

    st.subheader("📄 Alle bestillinger")
    st.dataframe(df)

    st.subheader("✏️ Oppdater status")
    selected_order = st.selectbox("Velg en bestilling", [f"#{o['orderID']} - {o['restaurant']} ({o['menuName']})" for o in orders])
    selected_id = int(selected_order.split("#")[1].split(" ")[0])
    current_order = next((o for o in orders if o["orderID"] == selected_id), None)

    if current_order:
        st.write(f"**Kunde:** {current_order['customer']}")
        st.write(f"**Meny:** {current_order['menuName']} – {current_order['price']} kr")
        st.write(f"**Status nå:** `{current_order['status']}`")

        new_status = st.selectbox(
            "Ny status",
            ["Mottatt", "Underveis", "Levert"],
            index=["Mottatt", "Underveis", "Levert"].index(current_order["status"])
        )

        if st.button("💾 Oppdater status"):
            cursor.execute("""
                UPDATE Ordered SET status = %s WHERE orderID = %s
            """, (new_status, selected_id))
            conn.commit()
            st.success("Status oppdatert!")
            st.rerun()

    cursor.close()
    conn.close()
