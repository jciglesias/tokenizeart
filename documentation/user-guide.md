# TokenizeArt User Guide

## Getting Started

### Prerequisites
- Web browser (Chrome, Firefox, Safari, Edge)
- NEAR wallet account
- Google account (for authentication)

### Quick Start
1. Visit the TokenizeArt application
2. Sign in with your Google account
3. Connect your NEAR wallet
4. Upload and mint your first NFT
5. View your NFT collection

---

## Creating Your First NFT

### Step 1: Authentication
1. Open the TokenizeArt application
2. Click "Login with Google"
3. Complete Google OAuth flow
4. You'll be redirected to the main application

### Step 2: Wallet Connection
1. Click "Connect Wallet" in the sidebar
2. Enter your NEAR wallet credentials
3. Confirm wallet connection
4. Your wallet balance will be displayed

### Step 3: Uploading Artwork
1. Navigate to the "Mint" page
2. Click "Upload a file to tokenize"
3. Select your artwork file (JPG, PNG, GIF)
4. **Important**: Your artwork must include the number "42" somewhere in the image
5. Wait for the file to upload to IPFS

### Step 4: Minting Your NFT
1. After successful upload, you'll see the IPFS preview
2. Your NFT will be automatically minted with metadata:
   - **Title**: Based on your filename
   - **Artist**: Your email address
   - **Description**: "Tokenized file"
   - **Media**: IPFS link to your artwork
3. Confirm the minting transaction
4. Wait for blockchain confirmation

### Step 5: Viewing Your NFT
1. Return to the main page
2. Your NFT will appear in your collection
3. View details including:
   - Token ID
   - Owner information
   - Artwork preview
   - Metadata

---

## Understanding NFT Metadata

### Required Fields
All TokenizeArt NFTs include these metadata fields:

```json
{
    "title": "Your artwork title (must include 42)",
    "description": "Description of your artwork",
    "media": "ipfs://hash-of-your-image",
    "media_hash": "verification-hash",
    "artist": "your-email@example.com",
    "copies": 1
}
```

### Metadata Standards
- **Title**: Must include "42" as per project requirements
- **Artist**: Automatically set to your login email
- **Media**: IPFS hash ensuring permanent storage
- **Copies**: Always set to 1 for unique NFTs

---

## Managing Your NFT Collection

### Viewing Your NFTs
1. Log into the application
2. Connect your wallet
3. Your NFTs will be displayed on the main page
4. Each NFT shows:
   - Token ID
   - Owner verification
   - Artwork preview
   - Metadata details

### Verifying Ownership
1. Each NFT displays the current owner
2. Ownership is verified through the blockchain
3. You can view transaction history on NEAR Explorer
4. Use the contract's `nft_token` function for verification

### Transferring NFTs
1. Navigate to "Send Near" page
2. Enter recipient's NEAR account
3. Specify the NFT token ID
4. Confirm the transfer transaction
5. Ownership will be updated on the blockchain

---

## Marketplace Features

### Listing NFTs for Sale
1. View your NFT collection
2. Select the NFT you want to sell
3. Set your desired price in NEAR tokens
4. Confirm the approval transaction
5. Your NFT will be available for purchase

### Buying NFTs
1. Browse available NFTs
2. Check the listing price
3. Ensure you have sufficient NEAR balance
4. Click "Buy" to purchase
5. Confirm the transaction
6. Ownership will transfer to your account

### Price Setting
- Prices are set in NEAR tokens
- Minimum price is 0.001 NEAR
- Consider current market rates
- Factor in transaction fees

---

## IPFS Storage

### How It Works
- Your artwork is stored on IPFS (InterPlanetary File System)
- IPFS provides decentralized, permanent storage
- Each file gets a unique content hash (CID)
- Files are accessible through multiple gateways

### Accessing Your Files
- **Local Gateway**: `http://localhost:8080/ipfs/{cid}`
- **Public Gateways**: `https://ipfs.io/ipfs/{cid}`
- **Your NFT**: Contains the IPFS link in metadata

### Storage Benefits
- **Permanent**: Files can't be deleted or modified
- **Decentralized**: No single point of failure
- **Verifiable**: Content hash ensures authenticity
- **Free**: No ongoing storage costs

---

## Wallet Management

### Connecting Your Wallet
1. Have your NEAR wallet credentials ready
2. Click "Connect Wallet" in the application
3. Enter your wallet name and password
4. Confirm the connection
5. Your wallet balance will be displayed

### Wallet Security
- **Never share your wallet credentials**
- Use a strong, unique password
- Enable two-factor authentication if available
- Keep your seed phrase secure and offline

### Transaction Costs
- **NFT Minting**: ~0.01 NEAR (~$0.001 USD)
- **Transfers**: ~0.001 NEAR
- **Marketplace**: ~0.002 NEAR per transaction
- **Storage**: Included in transaction fees

---

## Troubleshooting

### Common Issues

#### Login Problems
- **Issue**: Google login fails
- **Solution**: Check browser popup settings, clear cache
- **Alternative**: Try incognito/private browsing mode

#### Wallet Connection
- **Issue**: Wallet won't connect
- **Solution**: Verify credentials, check NEAR wallet status
- **Help**: Ensure you're using testnet credentials

#### File Upload Errors
- **Issue**: IPFS upload fails
- **Solution**: Check file size (max 10MB), try different format
- **Formats**: JPG, PNG, GIF supported

#### NFT Not Appearing
- **Issue**: Minted NFT doesn't show
- **Solution**: Wait for blockchain confirmation, refresh page
- **Time**: Usually takes 1-2 minutes

#### Transaction Failures
- **Issue**: Transaction rejected
- **Solution**: Check wallet balance, increase gas limit
- **Balance**: Ensure minimum 0.1 NEAR for transactions

### Getting Help
1. Check the error message details
2. Verify your wallet balance
3. Ensure artwork includes "42"
4. Try refreshing the application
5. Check NEAR network status

### Error Messages
- `Token already exists`: Use a unique token ID
- `Not enough deposit`: Increase attached NEAR amount
- `Not the owner`: Verify you own the NFT
- `Token not found`: Check token ID spelling

---

## Best Practices

### Artwork Guidelines
- **Include "42"**: Required for compliance
- **High Quality**: Use good resolution images
- **Appropriate Content**: No offensive material
- **Original Work**: Ensure you own the rights
- **File Size**: Keep under 10MB for faster upload

### Security Tips
- **Protect Credentials**: Never share wallet info
- **Verify Transactions**: Check details before confirming
- **Use Testnet**: Never risk real money
- **Backup Data**: Keep copies of your artwork

### Optimization
- **File Formats**: PNG for graphics, JPG for photos
- **Compression**: Balance quality and file size
- **Metadata**: Use descriptive titles and descriptions
- **Timing**: Monitor network congestion for lower fees

---

## Advanced Features

### Batch Operations
- Future feature: Mint multiple NFTs at once
- Bulk transfers to multiple recipients
- Collection management tools

### Analytics
- Track your NFT performance
- View transaction history
- Monitor collection value

### Integration
- Export NFT data
- API access for developers
- Cross-platform compatibility

---

## Frequently Asked Questions

### General Questions

**Q: What blockchain does TokenizeArt use?**
A: TokenizeArt uses the NEAR Protocol blockchain for its low fees and fast transactions.

**Q: Do I need real money to use TokenizeArt?**
A: No, TokenizeArt operates on NEAR testnet with free test tokens.

**Q: How do I get NEAR testnet tokens?**
A: Visit the NEAR faucet to get free testnet tokens for development.

### Technical Questions

**Q: Where is my artwork stored?**
A: Your artwork is stored on IPFS, a decentralized storage network.

**Q: Can I edit my NFT after minting?**
A: No, NFTs are immutable once minted. You can only transfer ownership.

**Q: How do I prove ownership?**
A: Ownership is recorded on the blockchain and can be verified through the contract.

### Troubleshooting Questions

**Q: Why isn't my NFT showing up?**
A: Wait for blockchain confirmation (1-2 minutes) and refresh the page.

**Q: My transaction failed. What do I do?**
A: Check your wallet balance and ensure you have enough NEAR for gas fees.

**Q: Can I cancel a transaction?**
A: No, blockchain transactions are irreversible once confirmed.

---

*For additional support, please refer to the technical documentation or community channels.*
