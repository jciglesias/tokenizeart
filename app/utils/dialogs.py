import streamlit as st
import utils.near as utils


@st.dialog("create_wallet", width="large")
def create_wallet_dialog():
    user_wallet = utils.get_wallet(st.user["email"])
    if not user_wallet:
        with st.form("create_wallet_form"):
            st.text_input("Wallet Name", key="wallet_name")
            st.text_input("Wallet Password", type="password", key="wallet_password")
            if st.form_submit_button("Create Wallet"):
                st.session_state.wallet = {
                    "name": st.session_state.wallet_name,
                    "password": st.session_state.wallet_password
                }
                utils.save_wallet(st.user["email"], st.session_state.wallet)
                st.success("Wallet created successfully!")
    else:
        st.session_state.wallet = user_wallet
        st.rerun()