from near_pytest import NearTestCase, Account, Contract, compile_contract


class TestNFTContract(NearTestCase):
    @classmethod
    def setup_class(cls):
        # Compile and deploy contract
        super().setup_class()
        cls.wasm_path = compile_contract("nft/contract.py")
        cls.owner = cls.create_account("owner")
        cls.contract: Contract = cls.deploy_contract(cls.owner, cls.wasm_path)

        # Initialize contract
        cls.contract.call_as(
            account=cls.owner,
            method_name="initialize",
            args={
                "owner_id": cls.owner.account_id
            }
        )

        # Create users
        cls.alice: Account = cls.create_account("alice")
        cls.bob: Account = cls.create_account("bob")
        cls.eve: Account = cls.create_account("eve")
        cls.save_state()

    def test_mint_token(self):
        token_id = "nft1"
        metadata = {
            "title": "Test NFT 1",
            "description": "An NFT minted by Alice",
            "media": "ipfs://media1.png"
        }

        self.contract.call_as(
            account=self.alice,
            method_name="nft_mint",
            args={
                "token_id": token_id,
                "metadata": metadata,
                "receiver_id": self.alice.account_id
            }
        )

        result = self.contract.view("nft_token", {"token_id": token_id})
        token_data = result.json()
        assert token_data["owner_id"] == self.alice.account_id
        assert token_data["metadata"]["title"] == "Test NFT 1"

    def test_list_and_buy_token(self):
        token_id = "nft2"
        metadata = {
            "title": "NFT For Sale",
            "description": "Minted by Bob",
            "media": "ipfs://media2.png"
        }
        price = int(0.25 * 1e24)  # 0.25 NEAR

        # Bob mints NFT
        self.contract.call_as(
            account=self.bob,
            method_name="nft_mint",
            args={
                "token_id": token_id,
                "metadata": metadata,
                "receiver_id": self.bob.account_id
            }
        )

        # Bob lists for sale
        self.contract.call_as(
            account=self.bob,
            method_name="nft_approve_for_sale",
            args={
                "token_id": token_id,
                "price": price
            }
        )

        # Alice buys it
        self.contract.call_as(
            account=self.alice,
            method_name="nft_buy",
            args={
                "token_id": token_id
            },
            amount=price
        )

        result = self.contract.view("nft_token", {"token_id": token_id})
        token_data = result.json()
        assert token_data["owner_id"] == self.alice.account_id

    def test_unauthorized_sale_should_fail(self):
        token_id = "nft3"
        metadata = {
            "title": "Evil Attempt",
            "description": "Eve is trying to list Alice's NFT",
            "media": "ipfs://media3.png"
        }

        # Alice mints NFT
        self.contract.call_as(
            account=self.alice,
            method_name="nft_mint",
            args={
                "token_id": token_id,
                "metadata": metadata,
                "receiver_id": self.alice.account_id
            }
        )

        # Eve tries to list it — should fail
        try:
            self.contract.call_as(
                account=self.eve,
                method_name="nft_approve_for_sale",
                args={
                    "token_id": token_id,
                    "price": int(1e24)  # 1 NEAR
                }
            )
        except Exception as e:
            assert "Not the owner" in str(e)
    
    def test_nft_list(self):
        # mint a few NFTs
        token_ids = ["nft4", "nft5", "nft6"]
        metadata = {
            "title": "Test NFT",
            "description": "An NFT minted by Alice",
            "media": "ipfs://media.png"
        }
        for token_id in token_ids:
            self.contract.call_as(
                account=self.alice,
                method_name="nft_mint",
                args={
                    "token_id": token_id,
                    "metadata": metadata,
                    "receiver_id": self.alice.account_id
                }
            )
        result = self.contract.call_as(
            account=self.alice,
            method_name="nft_list",
            args={}
        )
        result = result.json()
        assert isinstance(result["nfts"], list)
        assert all(token_id in result["nfts"] for token_id in token_ids), "Not all NFTs found in list"

    def test_nfts_for_sale(self):
        # mint an NFT and list it for sale
        token_id = "nft7"
        metadata = {
            "title": "NFT For Sale",
            "description": "Minted by Bob",
            "media": "ipfs://media2.png"
        }
        price = int(0.25 * 1e24)  # 0.25 NEAR
        self.contract.call_as(
            account=self.bob,
            method_name="nft_mint",
            args={
                "token_id": token_id,
                "metadata": metadata,
                "receiver_id": self.bob.account_id
            }
        )
        self.contract.call_as(
            account=self.bob,
            method_name="nft_approve_for_sale",
            args={
                "token_id": token_id,
                "price": price
            }
        )
        result = self.contract.view("nfts_for_sale", {})
        result = result.json()
        assert isinstance(result["sales"], dict)
        assert token_id in result["sales"], "NFT not found in sales list"
