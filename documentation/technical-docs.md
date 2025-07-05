# TokenizeArt Technical Documentation

## Table of Contents
1. [API Reference](#api-reference)
2. [Smart Contract Functions](#smart-contract-functions)
3. [Frontend Components](#frontend-components)
4. [IPFS Integration](#ipfs-integration)
5. [Deployment Guide](#deployment-guide)
6. [Troubleshooting](#troubleshooting)

---

## API Reference

### Smart Contract Methods

#### View Methods (No gas required)
```python
nft_token(token_id: str) -> dict
```
Returns token metadata and owner information for a given token ID.

**Parameters:**
- `token_id`: Unique identifier for the NFT

**Returns:**
```json
{
    "owner_id": "account.near",
    "metadata": {
        "title": "Artwork Title",
        "description": "Description",
        "media": "ipfs://hash",
        "media_hash": "hash",
        "artist": "creator@email.com",
        "copies": 1
    }
}
```

#### Call Methods (Require gas)
```python
nft_mint(token_id: str, metadata: dict, receiver_id: str)
```
Mints a new NFT with specified metadata.

**Parameters:**
- `token_id`: Unique identifier for the new NFT
- `metadata`: JSON object containing NFT metadata
- `receiver_id`: NEAR account to receive the NFT

```python
nft_approve_for_sale(token_id: str, price: int)
```
Approves an NFT for sale at a specified price.

**Parameters:**
- `token_id`: NFT to approve for sale
- `price`: Sale price in yoctoNEAR

```python
nft_buy(token_id: str)
```
Purchases an NFT that's approved for sale.

**Parameters:**
- `token_id`: NFT to purchase

---

## Smart Contract Functions

### Core Functions

#### Initialization
```python
@init
def initialize(self, owner_id: str):
    """Initialize the contract with an owner."""
    self.storage["owner_id"] = owner_id
    return {"success": True}
```

#### Minting Logic
```python
@call
def nft_mint(self, token_id: str, metadata: dict, receiver_id: str):
    """Mint a new NFT with metadata."""
    # Validation
    tokens_key = f"tokens:{token_id}"
    assert tokens_key not in self.storage, "Token already exists"
    
    # Store token data
    self.storage[tokens_key] = {
        "owner_id": receiver_id,
        "metadata": metadata
    }
    
    # Update user token list
    usr_tokens: list = self.storage.get(receiver_id, [])
    usr_tokens.append(token_id)
    self.storage[receiver_id] = usr_tokens
```

#### Ownership Verification
```python
@view
def nft_token(self, token_id: str):
    """Get token information."""
    tokens_key = f"tokens:{token_id}"
    return self.storage.get(tokens_key)
```

### Security Features

#### Access Control
- Only token owners can approve for sale
- Predecessor account validation
- Deposit amount verification

#### Data Validation
- Token existence checks
- Metadata format validation
- Price validation for sales

---

## Frontend Components

### Main Application (`tokenizeart.py`)
```python
import streamlit as st
import utils.dialogs as dialogs
from utils.near import get_nfts, view_nft
```

**Key Features:**
- User authentication with Google
- Wallet connection management
- NFT gallery display
- Async NEAR blockchain interactions

### Minting Interface (`pages/mint.py`)
```python
import streamlit as st
import requests
from utils.near import mint_nft
```

**Features:**
- File upload interface
- IPFS integration
- Metadata creation
- NFT minting workflow

### Utility Functions (`utils/near.py`)
Common blockchain interaction functions:
- `get_nfts()`: Retrieve user's NFTs
- `view_nft()`: Get NFT details
- `mint_nft()`: Create new NFT
- `send_near()`: Transfer tokens

---

## IPFS Integration

### File Upload Process
1. User selects file in Streamlit interface
2. File sent to IPFS node via API
3. IPFS returns content hash (CID)
4. CID used in NFT metadata

### IPFS Configuration
```python
# Upload to IPFS
files = {'file': (filename, file_content, mime_type)}
response = requests.post('http://ipfs:5001/api/v0/add', files=files)
cid = response.json()["Hash"]
```

### Gateway Access
- Local gateway: `http://localhost:8080/ipfs/{cid}`
- Public gateways: `https://ipfs.io/ipfs/{cid}`

---

## Deployment Guide

### Prerequisites
- Docker and Docker Compose
- NEAR CLI installed
- Python 3.11+
- Git

### Step 1: Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd tokenizeart

# Create environment file
cp .env.example .env
```

### Step 2: Contract Deployment
```bash
# Navigate to contract directory
cd contract/nft

# Build contract
near-sdk-py build

# Deploy to testnet
near deploy --accountId your-account.testnet --wasmFile contract.wasm

# Initialize contract
near call your-account.testnet initialize '{"owner_id": "your-account.testnet"}' --accountId your-account.testnet
```

### Step 3: Application Setup
```bash
# Return to root directory
cd ../..

# Start services
docker-compose up -d

# Access application
open http://localhost:8501
```

### Step 4: Verification
1. Check IPFS node: `http://localhost:8080/webui`
2. Test application: `http://localhost:8501`
3. Verify contract on NEAR Explorer

---

## Troubleshooting

### Common Issues

#### Contract Deployment Errors
```bash
# Error: Account doesn't exist
# Solution: Create account first
near create-account sub-account.your-account.testnet --masterAccount your-account.testnet

# Error: Insufficient balance
# Solution: Add funds to account
near send your-account.testnet sub-account.your-account.testnet 10
```

#### IPFS Connection Issues
```bash
# Check IPFS daemon status
docker-compose ps

# Restart IPFS service
docker-compose restart ipfs

# Check logs
docker-compose logs ipfs
```

#### Frontend Issues
```bash
# Check application logs
docker-compose logs app

# Restart application
docker-compose restart app

# Manual run for debugging
cd app && streamlit run tokenizeart.py
```

### Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| `Token already exists` | Duplicate token ID | Use unique token ID |
| `Not the owner` | Access denied | Verify account ownership |
| `Token not found` | Invalid token ID | Check token existence |
| `Not enough deposit` | Insufficient payment | Increase attached deposit |

### Debug Mode
Enable debug logging:
```python
# In your Python files
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization
- Use connection pooling for NEAR RPC calls
- Implement caching for frequently accessed data
- Optimize IPFS gateway selection
- Use async operations for blockchain calls

---

## Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use type hints for function parameters
- Add docstrings for all public functions
- Implement proper error handling

### Testing
- Unit tests for smart contract functions
- Integration tests for frontend components
- End-to-end tests for complete workflows
- Performance tests for high-load scenarios

### Security Best Practices
- Validate all user inputs
- Use secure random number generation
- Implement proper access controls
- Regular security audits

---

*For additional support, please refer to the project repository or community channels.*
