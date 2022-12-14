import streamlit as st

from src.database import select_db, download_db


with st.spinner("Analisando dados.gov.br..."):
    data = select_db()
# First selected option
data[None] = None
# Index from None
start = list(data.keys()).index(None)

st.title("Selecione o banco que deseja baixar")
option = st.selectbox(".", data.keys(), index=start, label_visibility="collapsed")

if option is not None:
    # Download selected database
    with st.spinner(f"Baixando {option}..."):
        st.session_state.option = option
        st.session_state.db = download_db(data[option])
    st.success(f"Banco de dados armazenado com sucesso")
    st.balloons()
