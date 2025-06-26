import streamlit as st
import requests

ipfs_gateway = "http://localhost:8080/ipfs/"

if st.user.is_logged_in:
    file_to_tokenize = st.file_uploader("Upload a file to tokenize:", type=["jpg", "jpeg", "png", "gif"])
    if file_to_tokenize is not None:
        files = {'file': (file_to_tokenize.name, file_to_tokenize, file_to_tokenize.type)}
        response = requests.post('http://ipfs:5001/api/v0/add', files=files)
        if response.status_code == 200:
            cid = response.json()["Hash"]
            st.success(f"File uploaded to IPFS with CID: {cid}")
            st.image(f"{ipfs_gateway}{cid}", caption="Image from Local IPFS Gateway")
            st.write(f"IPFS Link: {ipfs_gateway}{cid}")
        else:
            st.error(f"IPFS upload failed: {response.text}")