import streamlit as st
st.set_page_config(layout="wide", page_title="Portfolio Backtest")
import plotly.graph_objects as go

from classes.form import Form, read_forms, save_forms
import pages.form_page as form_page



forms = read_forms()
forms_checked = []

with st.sidebar():
    new_form_button = st.button("Create new portfolio")
    if new_form_button:
        st.write("Go to Form Page !")

    for form in forms:
        col1, col2 = st.columns([1, 5])
        if col1.checkbox(key=f'{form.name}_checkbox'):
            forms_checked.append(form)
        with col2.expander(form.name):
            st.write("Some info")