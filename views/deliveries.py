import streamlit as st
import pandas as pd
from db import get_connection

def show_deliveries():
    st.title("🚚 Leveringsoversikt")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT d.deliveryID, d.orderID, d.deliveryTime, d.deliveryStatus, u.username, r.rName
        FROM Delivery d
        JOIN Ordered o ON d.orderID = o.orderID
        JOIN users u ON o.userID = u.userID
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
    """)
    deliveries = cursor.fetchall()

    if not deliveries:
        st.info("Ingen leveranser registrert.")
    else:
        df = pd.DataFrame(deliveries)
        st.dataframe(df)

        st.subheader("✏️ Oppdater status")
        selected = st.selectbox("Velg levering", df["deliveryID"])
        new_status = st.selectbox("Ny status", ["Under behandling", "På vei", "Levert", "Avbrutt"])
        if st.button("Oppdater"):
            cursor.execute("UPDATE Delivery SET deliveryStatus = %s WHERE deliveryID = %s", (new_status, selected))
            conn.commit()
            st.success("Status oppdatert!")
            st.rerun()

    cursor.close()
    conn.close()
