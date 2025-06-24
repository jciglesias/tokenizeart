import streamlit as st
import asyncio
from py_near.account import Account
from py_near.dapps.core import NEAR

ipfs_gateway = "https://ipfs.io/ipfs/"

st.title("Check Balance and Send Money on NEAR Testnet (py-near)")
file_to_tokenize = st.file_uploader("Upload a file to tokenize:", type=["jpg", "jpeg", "png", "gif"])
if file_to_tokenize is not None:
    st.image(file_to_tokenize, caption="Uploaded Image", use_column_width=True)

account_id = st.text_input("Account ID:", "bob.testnet").strip()
private_key = st.text_input("Private Key:", "ed25519:...", type="password").strip()
target_account = st.text_input("Send To:", "bob.testnet").strip()
amount = st.number_input("Amount (NEAR):", value=1.0)

async def run(account_id, private_key, target_account, amount):
    acc = Account(account_id, private_key, rpc_addr="https://rpc.testnet.near.org")
    await acc.startup()
    balance = await acc.get_balance()
    result = {"balance": balance / NEAR}
    if target_account:
        tr = await acc.send_money(target_account, int(NEAR * amount))
        result["transaction_hash"] = tr.transaction.hash
        result["logs"] = tr.logs
    return result

if st.button("Check Balance & Send Money"):
    try:
        results = asyncio.run(run(account_id, private_key, target_account, amount))
        st.write(results)
    except Exception as e:
        st.error(f"Error: {e}")

st.write("Connect, check balance, and send money using `py-near`.")
