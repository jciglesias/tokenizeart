#!/bin/bash
# Example minting script

CONTRACT_ID="tokenizeart.testnet"
ACCOUNT_ID="your-account.testnet"
TOKEN_ID="artwork-42-$(date +%s)"

# Upload to IPFS first (using local node)
echo "Uploading artwork to IPFS..."
IPFS_HASH=$(curl -X POST -F "file=@./artwork-42.jpg" http://localhost:5001/api/v0/add | jq -r '.Hash')

echo "IPFS Hash: $IPFS_HASH"

# Mint NFT
echo "Minting NFT..."
near call $CONTRACT_ID nft_mint '{
  "token_id": "'$TOKEN_ID'",
  "metadata": {
    "title": "Digital Art 42 - Unique Creation",
    "description": "A unique digital artwork featuring the number 42",
    "media": "ipfs://'$IPFS_HASH'",
    "media_hash": "'$IPFS_HASH'",
    "artist": "artist@example.com",
    "copies": 1
  },
  "receiver_id": "'$ACCOUNT_ID'"
}' --accountId $ACCOUNT_ID --deposit 0.1

echo "NFT minted successfully!"
echo "Token ID: $TOKEN_ID"
echo "View on Explorer: https://testnet.nearblocks.io/accounts/$CONTRACT_ID"
