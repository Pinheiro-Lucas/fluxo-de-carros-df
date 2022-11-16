import streamlit as st


def select_db_page(data: dict, callback):
    data[None], option = None, None
    start = list(data.keys()).index(None)

    st.title("Selecione o banco que deseja baixar")
    option = st.selectbox(data.keys(), index=start)

    if option is not None:
        # Download selected database
        with st.spinner(f"Baixando {option}"):
            callback(data[option])
        st.success(f"Banco de dados armazenado com sucesso")
