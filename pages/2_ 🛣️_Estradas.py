import streamlit as st
import pandas as pd
import sys

from src.routes import rotas

# Just print estratas.txt
with st.spinner("Baixando rodovias..."):
    st.write(rotas())
