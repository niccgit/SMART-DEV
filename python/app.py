import streamlit as st

import bcrypt
from banco import conectar

if not st.session_state.get("autenticado", False):
    st.error("Você preciaa fazer login para realizar esta página.")