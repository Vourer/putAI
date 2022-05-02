import streamlit as st


with st.form(key='my_form'):
    name_input = st.text_input('Name:')
    dob_input = st.date_input('Date of birth:')
    weight_input = st.number_input('Weight (kg):')
    height_input = st.number_input('Height (cm):')

    submit_btn = st.form_submit_button('Compute BMI')

if submit_btn:
    bmi = weight_input / (height_input / 100) ** 2
    st.write(f'Hello {name_input}, your BMI={bmi:.2f}')
