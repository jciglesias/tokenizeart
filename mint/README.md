# Minting Instructions and Examples

## Overview
This folder contains examples and instructions for minting NFTs using the TokenizeArt platform.

## Minting Your NFT

### Method 1: Web Interface (Recommended)
1. Open the TokenizeArt web application
2. Login with Google account
3. Connect your NEAR wallet
4. Navigate to the "Mint" page
5. Upload your artwork (must include "42")
6. Confirm minting transaction

### Method 2: Command Line
```bash
# Mint NFT via NEAR CLI
near call CONTRACT_ID nft_mint '{
  "token_id": "unique-token-id",
  "metadata": {
    "title": "My Artwork 42",
    "description": "Digital artwork for TokenizeArt",
    "media": "ipfs://QmHash...",
    "media_hash": "QmHash...",
    "artist": "your-email@example.com",
    "copies": 1
  },
  "receiver_id": "your-account.testnet"
}' --accountId your-account.testnet --deposit 0.1
```

## NFT Requirements

### Artwork Requirements
- **Must include "42"**: Visible in the artwork
- **Supported formats**: JPG, PNG, GIF
- **File size**: Under 10MB recommended
- **Content**: No offensive material

### Metadata Requirements
- **Title**: Must include "42" and descriptive title
- **Artist**: Your login email address
- **Description**: Artwork description
- **Media**: IPFS hash of the artwork
- **Copies**: Always 1 for unique NFTs

## Example Minting Scripts

### mint-example.sh
```bash
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
```

### mint-batch.sh
```bash
#!/bin/bash
# Batch minting script for multiple NFTs

CONTRACT_ID="tokenizeart.testnet"
ACCOUNT_ID="your-account.testnet"

# Array of artwork files
ARTWORKS=("artwork-42-1.jpg" "artwork-42-2.png" "artwork-42-3.gif")

for artwork in "${ARTWORKS[@]}"; do
    echo "Processing $artwork..."
    
    # Upload to IPFS
    IPFS_HASH=$(curl -X POST -F "file=@./$artwork" http://localhost:5001/api/v0/add | jq -r '.Hash')
    
    # Generate unique token ID
    TOKEN_ID="batch-42-$(date +%s)-$(basename $artwork .${artwork##*.})"
    
    # Mint NFT
    near call $CONTRACT_ID nft_mint '{
      "token_id": "'$TOKEN_ID'",
      "metadata": {
        "title": "Batch Art 42 - '$artwork'",
        "description": "Part of a batch minting collection featuring 42",
        "media": "ipfs://'$IPFS_HASH'",
        "media_hash": "'$IPFS_HASH'",
        "artist": "batch-artist@example.com",
        "copies": 1
      },
      "receiver_id": "'$ACCOUNT_ID'"
    }' --accountId $ACCOUNT_ID --deposit 0.1
    
    echo "Minted: $TOKEN_ID"
    sleep 2  # Avoid rate limiting
done

echo "Batch minting completed!"
```

## Verification Scripts

### verify-nft.sh
```bash
#!/bin/bash
# Verify NFT after minting

CONTRACT_ID="tokenizeart.testnet"
TOKEN_ID=$1

if [ -z "$TOKEN_ID" ]; then
    echo "Usage: ./verify-nft.sh <token-id>"
    exit 1
fi

echo "Verifying NFT: $TOKEN_ID"

# Get token details
near view $CONTRACT_ID nft_token '{"token_id": "'$TOKEN_ID'"}'

# Check ownership
near view $CONTRACT_ID ownerOf '{"token_id": "'$TOKEN_ID'"}'

echo "Verification completed!"
```

### check-ownership.sh
```bash
#!/bin/bash
# Check NFT ownership

CONTRACT_ID="tokenizeart.testnet"
ACCOUNT_ID=$1

if [ -z "$ACCOUNT_ID" ]; then
    echo "Usage: ./check-ownership.sh <account-id>"
    exit 1
fi

echo "Checking NFTs owned by: $ACCOUNT_ID"

# List user's NFTs
near view $CONTRACT_ID nft_list --accountId $ACCOUNT_ID

echo "Ownership check completed!"
```

## Minting Best Practices

### Pre-Minting Checklist
- [ ] Artwork includes "42" visibly
- [ ] File size under 10MB
- [ ] Appropriate content (no offensive material)
- [ ] Unique token ID chosen
- [ ] IPFS node running
- [ ] Sufficient NEAR balance for gas fees

### Post-Minting Verification
- [ ] NFT appears in your collection
- [ ] Ownership verified on blockchain
- [ ] Metadata correctly stored
- [ ] IPFS link accessible
- [ ] Transaction confirmed on explorer

### Security Tips
- Use unique token IDs to avoid conflicts
- Verify IPFS upload before minting
- Keep records of all token IDs
- Test with small amounts first
- Monitor gas prices for optimal timing

## Troubleshooting

### Common Minting Issues
- **"Token already exists"**: Use a unique token ID
- **"Not enough deposit"**: Increase attached NEAR amount
- **"IPFS upload failed"**: Check IPFS node status
- **"Transaction failed"**: Verify account balance and permissions

### Gas Fees
- **Minting**: ~0.01-0.1 NEAR
- **IPFS Storage**: Free (decentralized)
- **Metadata Storage**: Included in minting fee

### Getting Help
- Check transaction on NEAR Explorer
- Verify contract address and function names
- Ensure proper JSON formatting
- Use testnet for practice

---

*For web-based minting, use the TokenizeArt application interface*
