import streamlit as st
import pandas as pd
from db import get_connection

def show_menus():
    st.title("📋 Menyadministrasjon")

    user_id = st.session_state.get("user_id")
    if user_id is None:
        st.error("Du må være innlogget.")
        st.stop()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Hent restauranter brukeren har tilgang til
    cursor.execute("""
        SELECT r.restaurantID, r.rName
        FROM restaurant_admins ra
        JOIN restaurant r ON ra.restaurantID = r.restaurantID
        WHERE ra.user_id = %s
    """, (user_id,))
    allowed_restaurants = cursor.fetchall()
    restaurant_ids = [r["restaurantID"] for r in allowed_restaurants]

    if not restaurant_ids:
        st.warning("Du har ikke tilgang til noen restauranter.")
        return

    # Vis bare menyer brukeren har tilgang til
    cursor.execute("""
        SELECT m.menuID, m.menuName, r.rName AS restaurant, m.price, m.description
        FROM menu m
        JOIN restaurant r ON m.restaurantID = r.restaurantID
        WHERE m.restaurantID IN (%s)
    """ % ",".join(["%s"] * len(restaurant_ids)), tuple(restaurant_ids))

    menus = cursor.fetchall()
    df = pd.DataFrame(menus)
    st.subheader("📄 Menyer du har tilgang til")
    if df.empty:
        st.info("Ingen menyer funnet.")
    else:
        st.dataframe(df)

    # ------------------ Opprett ny meny ------------------
    st.subheader("➕ Opprett ny meny")
    with st.form("add_menu"):
        name = st.text_input("Navn på meny")
        rest_map = {f"{r['rName']} (ID: {r['restaurantID']})": r['restaurantID'] for r in allowed_restaurants}
        selected_rest = st.selectbox("Velg restaurant", list(rest_map.keys()))
        restaurant_id = rest_map[selected_rest]

        price = st.number_input("Standardpris", step=1.0)
        description = st.text_area("Beskrivelse")
        create = st.form_submit_button("Opprett meny")

        if create:
            cursor.execute("""
                INSERT INTO menu (menuName, restaurantID, price, description)
                VALUES (%s, %s, %s, %s)
            """, (name, restaurant_id, price, description))
            conn.commit()
            st.success("Meny opprettet!")
            st.rerun()

    # ------------------ Legg til produkter ------------------
    st.subheader("➕ Legg til produkter i meny")

    # Hent tilgjengelige menyer brukeren kan redigere
    cursor.execute("""
        SELECT menuID, menuName FROM menu
        WHERE restaurantID IN (%s)
    """ % ",".join(["%s"] * len(restaurant_ids)), tuple(restaurant_ids))
    menus = cursor.fetchall()
    if not menus:
        st.warning("Ingen menyer tilgjengelig.")
        return

    menu_map = {f"{m['menuName']} (ID: {m['menuID']})": m['menuID'] for m in menus}
    selected_menu = st.selectbox("Velg meny", list(menu_map.keys()))
    menu_id = menu_map[selected_menu]

    cursor.execute("SELECT productID, name FROM product")
    products = cursor.fetchall()
    prod_map = {f"{p['name']} (ID: {p['productID']})": p['productID'] for p in products}
    selected_product = st.selectbox("Velg produkt", list(prod_map.keys()))

    if st.button("Legg til produkt i meny"):
        try:
            cursor.execute("""
                INSERT INTO menuitem (menuID, productID)
                VALUES (%s, %s)
            """, (menu_id, prod_map[selected_product]))
            conn.commit()
            st.success("Produkt lagt til!")
            st.rerun()
        except Exception as e:
            st.error(f"Feil: {e}")

    # ------------------ Vis produkter i valgt meny ------------------
    st.subheader("📦 Produkter i valgt meny")
    cursor.execute("""
        SELECT mi.menuID, p.productID, p.name
        FROM menuitem mi
        JOIN product p ON mi.productID = p.productID
        WHERE mi.menuID = %s
    """, (menu_id,))
    items = cursor.fetchall()
    if items:
        st.dataframe(pd.DataFrame(items))
    else:
        st.info("Ingen produkter lagt til i denne menyen.")

    cursor.close()
    conn.close()
