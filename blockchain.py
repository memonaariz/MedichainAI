"""
MediChain Blockchain Module
Provides data integrity, security, and immutability for medical records
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Any


class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: float, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 2):
        """Mine the block with proof-of-work"""
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict:
        """Convert block to dictionary"""
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }


class MediChainBlockchain:
    """Blockchain for securing medical records"""
    
    def __init__(self):
        self.chain: List[Block] = []
        self.difficulty = 2
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, time.time(), {
            'type': 'genesis',
            'message': 'MediChain Genesis Block',
            'created_at': datetime.now().isoformat()
        }, '0')
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Get the most recent block"""
        return self.chain[-1]
    
    def add_block(self, data: Dict) -> Block:
        """Add a new block to the chain"""
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=previous_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify link to previous block
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain(self) -> List[Dict]:
        """Get the entire blockchain as a list of dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_block_by_index(self, index: int) -> Dict:
        """Get a specific block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index].to_dict()
        return None
    
    def search_blocks(self, search_key: str, search_value: Any) -> List[Dict]:
        """Search for blocks containing specific data"""
        results = []
        for block in self.chain:
            if search_key in block.data and block.data[search_key] == search_value:
                results.append(block.to_dict())
        return results


class MedicalRecordBlockchain:
    """Specialized blockchain for medical records"""
    
    def __init__(self):
        self.blockchain = MediChainBlockchain()
    
    def add_prescription(self, patient_id: str, doctor_id: str, prescription_data: Dict) -> str:
        """Add a prescription to the blockchain"""
        block_data = {
            'type': 'prescription',
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'prescription': prescription_data,
            'timestamp': datetime.now().isoformat()
        }
        block = self.blockchain.add_block(block_data)
        return block.hash
    
    def add_medical_record(self, patient_id: str, record_type: str, record_data: Dict) -> str:
        """Add a medical record to the blockchain"""
        block_data = {
            'type': 'medical_record',
            'record_type': record_type,
            'patient_id': patient_id,
            'data': record_data,
            'timestamp': datetime.now().isoformat()
        }
        block = self.blockchain.add_block(block_data)
        return block.hash
    
    def add_lab_report(self, patient_id: str, lab_data: Dict) -> str:
        """Add a lab report to the blockchain"""
        block_data = {
            'type': 'lab_report',
            'patient_id': patient_id,
            'lab_data': lab_data,
            'timestamp': datetime.now().isoformat()
        }
        block = self.blockchain.add_block(block_data)
        return block.hash
    
    def add_appointment(self, patient_id: str, doctor_id: str, appointment_data: Dict) -> str:
        """Add an appointment to the blockchain"""
        block_data = {
            'type': 'appointment',
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment': appointment_data,
            'timestamp': datetime.now().isoformat()
        }
        block = self.blockchain.add_block(block_data)
        return block.hash
    
    def verify_record(self, block_hash: str) -> bool:
        """Verify if a record exists and is valid"""
        for block in self.blockchain.chain:
            if block.hash == block_hash:
                return True
        return False
    
    def get_patient_records(self, patient_id: str) -> List[Dict]:
        """Get all records for a specific patient"""
        return self.blockchain.search_blocks('patient_id', patient_id)
    
    def get_blockchain_stats(self) -> Dict:
        """Get blockchain statistics"""
        return {
            'total_blocks': len(self.blockchain.chain),
            'is_valid': self.blockchain.is_chain_valid(),
            'latest_block_hash': self.blockchain.get_latest_block().hash,
            'genesis_block_hash': self.blockchain.chain[0].hash
        }


# Global blockchain instance
medical_blockchain = MedicalRecordBlockchain()


def get_blockchain_instance() -> MedicalRecordBlockchain:
    """Get the global blockchain instance"""
    return medical_blockchain


def verify_data_integrity(data: Dict) -> str:
    """Generate SHA-256 hash for data verification"""
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()


def encrypt_sensitive_data(data: str) -> str:
    """Simple encryption for sensitive data (demo purposes)"""
    # In production, use proper encryption like AES-256
    return hashlib.sha256(data.encode()).hexdigest()
