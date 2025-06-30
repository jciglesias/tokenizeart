from near_sdk_py import Contract, call, view, init, ONE_NEAR

class NFTContract(Contract):

    @init
    def initialize(self, owner_id: str):
        self.storage["owner_id"] = owner_id
        return {"success": True}

    @call
    def nft_mint(self, token_id: str, metadata: dict, receiver_id: str):
        tokens_key = f"tokens:{token_id}"
        assert tokens_key not in self.storage, "Token already exists"
        self.storage[tokens_key] = {
            "owner_id": receiver_id,
            "metadata": metadata
        }

        usr_tokens: list = self.storage.get(receiver_id, [])
        usr_tokens.append(token_id)
        self.storage[receiver_id] = usr_tokens

    @call
    def nft_approve_for_sale(self, token_id: str, price: int):
        tokens_key = f"tokens:{token_id}"
        token = self.storage.get(tokens_key)
        assert token, "Token not found"
        assert token["owner_id"] == self.predecessor_account_id, "Not the owner"
        
        sales_key = f"sales:{token_id}"
        self.storage[sales_key] = price

    @call
    def nft_buy(self, token_id: str):
        sales_key = f"sales:{token_id}"
        price = self.storage.get(sales_key)
        assert price is not None, "Token not for sale"
        assert self.attached_deposit >= price, "Not enough deposit"
        
        tokens_key = f"tokens:{token_id}"
        token = self.storage[tokens_key]
        token["owner_id"] = self.predecessor_account_id
        self.storage[tokens_key] = token
        del self.storage[sales_key]

    @view
    def nft_token(self, token_id: str):
        tokens_key = f"tokens:{token_id}"
        return self.storage.get(tokens_key)
    
    @view
    def nft_list(self):
        # if self.predecessor_account_id == self.storage.get("owner_id"):
        #     return {key: self.storage[key] for key in self.storage if key.startswith("tokens:")}
        return {"nfts": self.storage.get(self.predecessor_account_id, [])}
