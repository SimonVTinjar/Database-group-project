import streamlit as st

def show_home():
    st.title("🍽️ Velkommen til RestaurantAdmin")
    st.markdown(f"""
    Du er logget inn som: `{st.session_state.username}`  
    ---
    Velkommen til adminpanelet for restaurantdrift.  
    Her kan du:
    - ✅ Legge til og administrere restauranter
    - 🍕 Administrere menyer for hver restaurant
    - 📦 Se innkommende bestillinger

    Bruk menyen til venstre for å komme i gang.
    """)
