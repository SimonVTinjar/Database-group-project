import streamlit as st
import pandas as pd
from db import get_connection

def show_menus():
    st.title("📋 Menyadministrasjon")

    # Hent alle menyer med restaurantnavn
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.menuID, m.menuName, r.rName AS restaurant, m.price, m.description
        FROM Menu m
        JOIN Restaurant r ON m.restaurantID = r.restaurantID
    """)
    menus = cursor.fetchall()
    df = pd.DataFrame(menus)
    st.subheader("📄 Alle menyer")
    if df.empty:
        st.info("Ingen menyer funnet.")
    else:
        st.dataframe(df)

    st.subheader("➕ Opprett ny meny")
    with st.form("add_menu"):
        name = st.text_input("Navn på meny")
        restaurant_id = st.number_input("Restaurant ID", step=1, min_value=1)
        price = st.number_input("Standardpris", step=1.0)
        description = st.text_area("Beskrivelse")
        create = st.form_submit_button("Opprett meny")
        if create:
            cursor.execute("""
                INSERT INTO Menu (menuName, restaurantID, price, description)
                VALUES (%s, %s, %s, %s)
            """, (name, restaurant_id, price, description))
            conn.commit()
            st.success("Meny opprettet!")
            st.rerun()

    st.subheader("➕ Legg til produkter i meny")
    cursor.execute("SELECT menuID, menuName FROM Menu")
    menus = cursor.fetchall()
    menu_map = {f"{m['menuName']} (ID: {m['menuID']})": m['menuID'] for m in menus}
    if not menu_map:
        st.warning("Ingen menyer å legge produkter til.")
        return

    selected_menu = st.selectbox("Velg meny", list(menu_map.keys()))
    menu_id = menu_map[selected_menu]

    cursor.execute("SELECT productID, name FROM Product")
    products = cursor.fetchall()
    prod_map = {f"{p['name']} (ID: {p['productID']})": p['productID'] for p in products}

    selected_product = st.selectbox("Velg produkt", list(prod_map.keys()))
    if st.button("Legg til produkt i meny"):
        try:
            cursor.execute("""
                INSERT INTO MenuItem (menuID, productID)
                VALUES (%s, %s)
            """, (menu_id, prod_map[selected_product]))
            conn.commit()
            st.success("Produkt lagt til!")
            st.rerun()
        except Exception as e:
            st.error(f"Feil: {e}")

    # Vis produkter i valgt meny
    st.subheader("📦 Produkter i valgt meny")
    cursor.execute("""
        SELECT mi.menuID, p.productID, p.name
        FROM MenuItem mi
        JOIN Product p ON mi.productID = p.productID
        WHERE mi.menuID = %s
    """, (menu_id,))
    items = cursor.fetchall()
    if items:
        st.dataframe(pd.DataFrame(items))
    else:
        st.info("Ingen produkter lagt til i denne menyen.")

    cursor.close()
    conn.close()
