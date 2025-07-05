import streamlit as st
import utils.dialogs as dialogs
from utils.near import get_nfts, view_nft
import asyncio

st.set_page_config(page_title="Tokenize Art", page_icon=":art:", layout="wide")

if not st.user.is_logged_in:
    if st.button("Login with Google"):
        st.login()

else:
    if st.sidebar.button("Logout"):
        st.logout()
    if "wallet" not in st.session_state:
        dialogs.create_wallet_dialog()
    else:    
        st.write(st.user["email"])
        result = asyncio.run(get_nfts(
            st.session_state.wallet["name"],
            st.session_state.wallet["password"]
        ))
        for nft in result["nfts"]:
            data = asyncio.run(view_nft(
                st.session_state.wallet["name"],
                st.session_state.wallet["password"],
                nft
            ))
            st.subheader(f"Token ID: {nft}")
            st.write(f"Owner: {data['owner_id']}")
            st.image(data["metadata"]["media"], caption=data["metadata"]["title"])
