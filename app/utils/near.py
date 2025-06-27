from py_near.account import Account
from py_near.dapps.core import NEAR

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

async def get_nfts(account_id, private_key):
    acc = Account(account_id, private_key, rpc_addr=rpc_addr)
    await acc.startup()
    nfts = await acc.view_function() # Assuming the function to get NFTs is defined in the contract
    return nfts