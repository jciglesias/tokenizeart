import streamlit as st
import requests
import utils.dialogs as dialogs
from utils.near import mint_nft
import asyncio

ipfs_gateway = "http://localhost:8080/ipfs/"

if st.user.is_logged_in and "wallet" in st.session_state:
    file_to_tokenize = st.file_uploader("Upload a file to tokenize:", type=["jpg", "jpeg", "png", "gif"])
    if file_to_tokenize is not None:
        files = {'file': (file_to_tokenize.name, file_to_tokenize, file_to_tokenize.type)}
        response = requests.post('http://ipfs:5001/api/v0/add', files=files)
        if response.status_code == 200:
            cid = response.json()["Hash"]
            st.success(f"File uploaded to IPFS with CID: {cid}")
            st.image(f"{ipfs_gateway}{cid}", caption="Image from Local IPFS Gateway")
            st.write(f"IPFS Link: {ipfs_gateway}{cid}")
            result = asyncio.run(mint_nft( 
                st.session_state.wallet["name"],
                st.session_state.wallet["password"],
                cid,
                {
                    "title": file_to_tokenize.name,
                    "description": "Tokenized file",
                    "media": f"{ipfs_gateway}{cid}",
                    "media_hash": cid,
                    "copies": 1
                },
                st.session_state.wallet["name"]
            ))
            st.write(result)
        else:
            st.error(f"IPFS upload failed: {response.text}")

else:
    if st.user.is_logged_in:
        st.warning("Please connect your wallet to upload files.")
        dialogs.create_wallet_dialog()
    else:
        st.warning("Please log in to upload files.")
        if st.button("Login"):
            st.login()