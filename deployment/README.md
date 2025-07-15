# Deployment Instructions

## Overview
This folder contains deployment-related files and instructions for the TokenizeArt NFT contract.

## Main Deployment Files
The primary deployment files are located in the `code/` folder:
- `code/contract.wasm` - Compiled smart contract
- `code/pyproject.toml` - Project configuration
- `code/README.md` - Detailed deployment instructions

## Quick Deployment Guide

### Prerequisites
- NEAR CLI installed
- Python 3.13+ installed
- Emscripten installed (for compilation)
- uv package manager installed

### Step 1: Build Contract
```bash
cd code/
uvx nearc nft/contract.py
```

### Step 2: Deploy to Testnet
```bash
# Create development account
near create-account tokenizeart-dev.testnet --useFaucet

# Deploy contract
near deploy tokenizeart-dev.testnet contract.wasm

# Initialize contract
near call tokenizeart-dev.testnet initialize '{"owner_id": "your-account.testnet"}' --accountId your-account.testnet
```

### Step 3: Verify Deployment
```bash
# Test contract functions
near view tokenizeart-dev.testnet nft_token '{"token_id": "test"}'
```

## Network Configuration

### Testnet Details
- **Network**: NEAR Testnet
- **RPC URL**: https://rpc.testnet.near.org
- **Explorer**: https://testnet.nearblocks.io
- **Faucet**: https://near-faucet.io

### Contract Address
**Update this section once deployed:**
- Contract Account: `tokenizeart.testnet`
- Network: NEAR Testnet
- Deployment Date: 04/07/2025
- Transaction Hash: CPPWyBA6Mr6x2BnLfrRXyWqcPJRist9S4fduw4FLGRBk

## Deployment Scripts

### deploy.sh
```bash
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
```

### test-deployment.sh
```bash
#!/bin/bash
# Test deployment script

CONTRACT_ID=$1
if [ -z "$CONTRACT_ID" ]; then
    echo "Usage: ./test-deployment.sh <contract-account-id>"
    exit 1
fi

echo "Testing deployed contract: $CONTRACT_ID"

# Test view functions
echo "Testing nft_token function..."
near view $CONTRACT_ID nft_token '{"token_id": "test"}' || echo "No token found (expected)"

echo "Testing nft_list function..."
near view $CONTRACT_ID nft_list || echo "Empty list (expected)"

echo "Deployment test completed!"
```

## Security Considerations
- Always use testnet for development
- Verify contract source code before deployment
- Test all functions after deployment
- Keep private keys secure
- Monitor contract for unexpected behavior

## Troubleshooting

### Common Issues
- **Build fails**: Check Emscripten installation
- **Deploy fails**: Verify NEAR CLI setup and account balance
- **Functions fail**: Check parameter format and account permissions

### Getting Help
- Check the `code/README.md` for detailed instructions
- Review NEAR documentation
- Use NEAR Discord for community support

---

*For detailed deployment instructions, see `code/README.md`*
