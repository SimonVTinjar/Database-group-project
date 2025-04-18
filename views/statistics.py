import streamlit as st
import pandas as pd
from db import get_connection

def show_statistics():
    st.title("📊 Statistikk")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restaurantene brukeren har tilgang til
    cursor.execute("""
        SELECT restaurantID FROM restaurant_admins WHERE user_id = %s
    """, (user_id,))
    restaurant_ids = [row["restaurantID"] for row in cursor.fetchall()]

    if not restaurant_ids:
        st.warning("Ingen restauranter tilgjengelig.")
        return

    placeholders = ",".join(["%s"] * len(restaurant_ids))

    # Hent bestillingsdata
    cursor.execute(f"""
        SELECT r.rName, m.menuName, o.orderTime, m.price
        FROM ordered o
        JOIN menu m ON o.menuID = m.menuID
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE r.restaurantID IN ({placeholders})
    """, tuple(restaurant_ids))
    orders = cursor.fetchall()
    cursor.close()
    conn.close()

    if not orders:
        st.info("Ingen bestillinger funnet.")
        return

    df = pd.DataFrame(orders)
    df["orderTime"] = pd.to_datetime(df["orderTime"])

    # Antall bestillinger per restaurant
    order_counts = df.groupby("rName").size().reset_index(name="Antall bestillinger")

    # Total omsetning per restaurant
    total_revenue = df.groupby("rName")["price"].sum().reset_index(name="Total inntekt (kr)")

    # Populære menyer
    popular_menus = df.groupby("menuName").size().reset_index(name="Antall bestillinger").sort_values(by="Antall bestillinger", ascending=False)

    st.subheader("📦 Antall bestillinger per restaurant")
    st.table(order_counts)

    st.subheader("💰 Total inntekt per restaurant")
    st.table(total_revenue)

    st.subheader("🔥 Mest populære menyer")
    st.table(popular_menus)
