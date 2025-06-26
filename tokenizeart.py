import streamlit as st
import asyncio
from py_near.account import Account
from py_near.dapps.core import NEAR
import requests


if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()
    st.stop()

else:
    if st.sidebar.button("Logout"):
        st.logout()
    st.write(st.user["email"])

