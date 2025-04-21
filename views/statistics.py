import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db import get_connection

def show_statistics():
    st.title("📊 Statistikk")

    user_id = st.session_state.get("ResUserID")
    if not user_id:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restaurantene brukeren har tilgang til
    cursor.execute("""
        SELECT restaurantID FROM restaurantadmin WHERE ResUserID = %s
    """, (user_id,))
    restaurant_ids = [row["restaurantID"] for row in cursor.fetchall()]

    if not restaurant_ids:
        st.warning("Ingen restauranter tilgjengelig.")
        return

    placeholders = ",".join(["%s"] * len(restaurant_ids))

    cursor.execute(f"""
        SELECT r.rName, m.menuName, o.orderTime, m.price
        FROM Ordered o
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

    # 📦 Antall bestillinger per restaurant
    order_counts = df.groupby("rName").size().reset_index(name="Antall bestillinger")
    st.subheader("📦 Antall bestillinger per restaurant")
    st.table(order_counts)

    fig1, ax1 = plt.subplots()
    ax1.bar(order_counts["rName"], order_counts["Antall bestillinger"])
    ax1.set_ylabel("Bestillinger")
    ax1.set_title("Bestillinger per restaurant")
    st.pyplot(fig1)

    # 💰 Total inntekt per restaurant
    total_revenue = df.groupby("rName")["price"].sum().reset_index(name="Total inntekt (kr)")
    st.subheader("💰 Total inntekt per restaurant")
    st.table(total_revenue)

    fig2, ax2 = plt.subplots()
    ax2.bar(total_revenue["rName"], total_revenue["Total inntekt (kr)"])
    ax2.set_ylabel("Inntekt (kr)")
    ax2.set_title("Inntekt per restaurant")
    st.pyplot(fig2)

    # 🗓️ Bestillinger over tid
    orders_per_day = df.groupby(df["orderTime"].dt.date).size().reset_index(name="Antall bestillinger")
    st.subheader("🗓️ Bestillinger over tid")

    fig3, ax3 = plt.subplots()
    ax3.plot(orders_per_day["orderTime"], orders_per_day["Antall bestillinger"], marker="o")
    ax3.set_ylabel("Bestillinger")
    ax3.set_xlabel("Dato")
    ax3.set_title("Bestillinger over tid")
    st.pyplot(fig3)

    # 🔥 Mest populære menyer
    popular_menus = df.groupby("menuName").size().reset_index(name="Antall bestillinger").sort_values(by="Antall bestillinger", ascending=False)
    st.subheader("🔥 Mest populære menyer")
    st.table(popular_menus)

    fig4, ax4 = plt.subplots()
    ax4.bar(popular_menus["menuName"], popular_menus["Antall bestillinger"])
    ax4.set_ylabel("Bestillinger")
    ax4.set_title("Populære menyer")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig4)