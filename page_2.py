import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

left_column, right_column = st.columns(2)
left_column.button('Press')

with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")

knapp = st.sidebar.button(
    'Hei'
)

if knapp:
    st.write('Klikk!')
