from py_near.account import Account
from py_near.dapps.core import NEAR
import os
import base64
import json

rpc_addr = "https://rpc.testnet.near.org"

async def run(account_id, private_key, target_account, amount):
        acc = Account(account_id, private_key, rpc_addr=rpc_addr)
        await acc.startup()
        balance = await acc.get_balance()
        result = {"balance": balance / NEAR}
        if target_account:
            tr = await acc.send_money(target_account, int(NEAR * amount))
            result["transaction_hash"] = tr.transaction.hash
            result["logs"] = tr.logs
        return result

async def check_balance(account_id, private_key):
    acc = Account(account_id, private_key, rpc_addr=rpc_addr)
    await acc.startup()
    balance = await acc.get_balance()
    return balance / NEAR

async def view_nft(account_id, private_key, token_id):
    acc = Account(account_id, private_key, rpc_addr=rpc_addr)
    await acc.startup()
    result = await acc.function_call(
        contract_id="tokenizeart.testnet",
        method_name="nft_token",
        args={"token_id": token_id}
    )
    # Extract and decode the NFT data from the transaction result
    if hasattr(result, 'status') and 'SuccessValue' in result.status:
        # Decode the base64 encoded JSON string
        encoded_data = result.status['SuccessValue']
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_string = decoded_bytes.decode('utf-8')
        try:
            nft_data = json.loads(decoded_string)
            return nft_data
        except json.JSONDecodeError:
            return {"raw_result": decoded_string}
    return result

async def get_nfts(account_id, private_key):
    acc = Account(account_id, private_key, rpc_addr=rpc_addr)
    await acc.startup()
    result = await acc.function_call(
        contract_id="tokenizeart.testnet",
        method_name="nft_list",
        args={}
    )
    
    # Extract and decode the NFT data from the transaction result
    if hasattr(result, 'status') and 'SuccessValue' in result.status:
        # Decode the base64 encoded JSON string
        encoded_data = result.status['SuccessValue']
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_string = decoded_bytes.decode('utf-8')
        nft_data = json.loads(decoded_string)
        return nft_data
    
    return result

async def mint_nft(account_id, private_key, token_id, metadata, receiver_id):
    acc = Account(account_id, private_key, rpc_addr=rpc_addr)
    await acc.startup()
    result = await acc.function_call(
        contract_id="tokenizeart.testnet",
        method_name="nft_mint",
        args={
            "token_id": token_id,
            "metadata": metadata,
            "receiver_id": receiver_id
        }
    )
    
    # Extract and decode the result if it's a successful transaction
    if hasattr(result, 'status') and 'SuccessValue' in result.status:
        # Decode the base64 encoded JSON string
        encoded_data = result.status['SuccessValue']
        if encoded_data:  # Only decode if there's actual data
            decoded_bytes = base64.b64decode(encoded_data)
            decoded_string = decoded_bytes.decode('utf-8')
            try:
                mint_data = json.loads(decoded_string)
                return mint_data
            except json.JSONDecodeError:
                return {"raw_result": decoded_string}
    
    return result

def get_wallet(email):
    wallets_dir = "wallets/"
    if not os.path.exists(wallets_dir):
        os.makedirs(wallets_dir)
    user_wallet_file = os.path.join(wallets_dir, f"{email}.json")
    if not os.path.exists(user_wallet_file):
        return None  # Wallet file does not exist
    with open(user_wallet_file, "r") as f:
        return eval(f.read())
    
def save_wallet(email, wallet_data):
    wallets_dir = "wallets/"
    if not os.path.exists(wallets_dir):
        os.makedirs(wallets_dir)
    user_wallet_file = os.path.join(wallets_dir, f"{email}.json")
    with open(user_wallet_file, "w") as f:
        f.write(str(wallet_data))