# blockchain.py - Enhanced Blockchain for Healthcare
import hashlib
import json
import time
from datetime import datetime
import random

class EnhancedBlock:
    """Enhanced Block with additional security features"""
    
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.difficulty = 4
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self):
        """Mine the block with proof of work"""
        target = "0" * self.difficulty
        
        while self.hash[:self.difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        return self.hash

class EnhancedBlockchain:
    """Enhanced Blockchain with additional features"""
    
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.pending_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = EnhancedBlock(0, datetime.now().isoformat(), 
                                    {"message": "MediChain AI Genesis Block"}, "0")
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data):
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_block = EnhancedBlock(
            previous_block.index + 1,
            datetime.now().isoformat(),
            data,
            previous_block.hash
        )
        
        # Mine the block
        new_block.hash = new_block.mine_block()
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Check if the blockchain is valid"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash is correct
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_blockchain_stats(self):
        """Get blockchain statistics"""
        return {
            'total_blocks': len(self.chain),
            'chain_valid': self.is_chain_valid(),
            'security_level': 'ENHANCED_SECURE',
            'last_block_hash': self.chain[-1].hash[:16] + "..." if self.chain else "None",
            'difficulty': self.difficulty
        }
    
    def add_transaction(self, sender, recipient, data):
        """Add a transaction to pending transactions"""
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
        self.pending_transactions.append(transaction)
        return len(self.chain) + 1

# Factory function for compatibility
def get_ultra_secure_blockchain():
    """Get a blockchain instance"""
    return EnhancedBlockchain()

# For backward compatibility
class Blockchain(EnhancedBlockchain):
    """Alias for backward compatibility"""
    pass

if __name__ == "__main__":
    # Test the blockchain
    print("🏥 Testing MediChain AI Blockchain...")
    
    blockchain = EnhancedBlockchain()
    
    # Add some test blocks
    blockchain.add_block({"message": "First medical record uploaded"})
    blockchain.add_block({"message": "Second medical record uploaded"})
    blockchain.add_block({"message": "AI analysis completed"})
    
    # Print blockchain info
    print(f"Total blocks: {len(blockchain.chain)}")
    print(f"Chain valid: {blockchain.is_chain_valid()}")
    
    # Print all blocks
    for block in blockchain.chain:
        print(f"Block #{block.index}: {block.data['message']}")
        print(f"Hash: {block.hash[:16]}...")
        print("---")