import streamlit as st
import asyncio
from utils.near import run


if st.user.is_logged_in:
    st.title(f"Check Balance and Send Money on NEAR")
    account_id = st.session_state.wallet["name"] if "wallet" in st.session_state else None
    st.header(f"Account:  {account_id}")

    private_key = st.session_state.wallet["password"] if "wallet" in st.session_state else None

    if private_key:
        if "balance" not in st.session_state:
            try:
                results = asyncio.run(run(account_id, private_key, None, 0))
                st.session_state.balance = results['balance']
                # st.write(f"Balance: {results['balance']} NEAR")
            except Exception as e:
                st.error(f"Error: {e}")
        st.write(f"Balance: {st.session_state.balance} NEAR")
        target_account = st.text_input("Send To:", "bob.testnet").strip()
        amount = st.number_input("Amount (NEAR):", value=0.01, min_value=0.01)
        if st.button("Send Money"):
            try:
                results = asyncio.run(run(account_id, private_key, target_account, amount))
                st.write(results)
            except Exception as e:
                st.error(f"Error: {e}")
