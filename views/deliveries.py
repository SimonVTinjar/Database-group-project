import streamlit as st
import pandas as pd
from db import get_connection

def show_deliveries():
    st.title("🚚 Leveringsoversikt")

    user_id = st.session_state.get("ResUserID")
    if not user_id:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restaurantene brukeren har tilgang til
    cursor.execute("SELECT restaurantID FROM restaurantadmin WHERE ResUserID = %s", (user_id,))
    restaurant_ids = [row["restaurantID"] for row in cursor.fetchall()]

    if not restaurant_ids:
        st.warning("Du har ikke tilgang til noen restauranter.")
        cursor.close()
        conn.close()
        return

    placeholders = ",".join(["%s"] * len(restaurant_ids))

    # Hent leveranser knyttet til bestillinger fra restauranter brukeren har tilgang til
    query = f"""
        SELECT d.deliveryID, d.orderID, d.deliveryTime, d.deliveryStatus, 
               ru.ResUsername AS customer, r.rName
        FROM Delivery d
        JOIN Ordered o ON d.orderID = o.orderID
        JOIN Restaurantadminuser ru ON o.userID = ru.ResUserID
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE r.restaurantID IN ({placeholders})
        ORDER BY d.deliveryTime DESC
    """
    cursor.execute(query, tuple(restaurant_ids))
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
