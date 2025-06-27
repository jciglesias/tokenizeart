import streamlit as st
import os

st.set_page_config(page_title="Tokenize Art", page_icon=":art:", layout="wide")

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()

else:
    if "wallet" not in st.session_state:
        wallets_dir = "wallets/"
        if not os.path.exists(wallets_dir):
            os.makedirs(wallets_dir)
        user_wallet_file = os.path.join(wallets_dir, f"{st.user['email']}.json")
        if not os.path.exists(user_wallet_file):
            # Create a new wallet file
            with st.form("create_wallet_form"):
                st.text_input("Wallet Name", key="wallet_name")
                st.text_input("Wallet Password", type="password", key="wallet_password")
                if st.form_submit_button("Create Wallet"):
                    # Here you would normally create a wallet and save it
                    st.session_state.wallet = {
                        "name": st.session_state.wallet_name,
                        "password": st.session_state.wallet_password
                    }
                    with open(user_wallet_file, "w") as f:
                        f.write(str(st.session_state.wallet))
                    st.success("Wallet created successfully!")
        else:
            with open(user_wallet_file, "r") as f:
                st.session_state.wallet = eval(f.read())
        
    if st.sidebar.button("Logout"):
        st.logout()
    st.write(st.user["email"])

