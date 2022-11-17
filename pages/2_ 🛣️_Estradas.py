import streamlit as st
import sys

from src.routes import rotas

# Just print estratas.txt
with st.spinner("Carregando estradas.txt..."):
    st.write(rotas())
