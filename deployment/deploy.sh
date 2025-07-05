#!/bin/bash
# Deployment script for TokenizeArt NFT contract

set -e

echo "Starting TokenizeArt contract deployment..."

# Build contract
echo "Building contract..."
cd code/
uvx nearc nft/contract.py

# Deploy to testnet
echo "Deploying to testnet..."
ACCOUNT_ID="tokenizeart-$(date +%s).testnet"
near create-account $ACCOUNT_ID --useFaucet
near deploy $ACCOUNT_ID contract.wasm

# Initialize contract
echo "Initializing contract..."
near call $ACCOUNT_ID initialize '{"owner_id": "'$ACCOUNT_ID'"}' --accountId $ACCOUNT_ID

echo "Contract deployed successfully!"
echo "Contract Account: $ACCOUNT_ID"
echo "Network: NEAR Testnet"
echo "Explorer: https://testnet.nearblocks.io/accounts/$ACCOUNT_ID"
