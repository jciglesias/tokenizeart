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
        
        # Also maintain a sales list for easier querying
        sales_list = self.storage.get("sales_list", [])
        if token_id not in sales_list:
            sales_list.append(token_id)
            self.storage["sales_list"] = sales_list

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
        
        # Remove from sales list
        sales_list = self.storage.get("sales_list", [])
        if token_id in sales_list:
            sales_list.remove(token_id)
            self.storage["sales_list"] = sales_list

    @view
    def nft_token(self, token_id: str):
        tokens_key = f"tokens:{token_id}"
        return self.storage.get(tokens_key)
    
    @view
    def ownerOf(self, token_id: str) -> str:
        """Returns the owner of the specified token ID (required by subject)"""
        tokens_key = f"tokens:{token_id}"
        token = self.storage.get(tokens_key)
        if token:
            return token["owner_id"]
        return None
    
    @view
    def nft_list(self):
        return {"nfts": self.storage.get(self.predecessor_account_id, [])}
    
    @view
    def nfts_for_sale(self):
        """Returns a list of NFTs available for sale"""
        sales_list = self.storage.get("sales_list", [])
        sales = {}
        for token_id in sales_list:
            sales_key = f"sales:{token_id}"
            price = self.storage.get(sales_key)
            if price is not None:
                sales[token_id] = price
        return {"sales": sales}
