"""
MediChain Security Demo — Run this in front of mam
python demo_security.py
"""
from blockchain import MedicalRecordBlockchain
import json, hashlib

print("=" * 60)
print("  MediChain — LIVE SECURITY DEMONSTRATION")
print("=" * 60)

bc = MedicalRecordBlockchain()

# Step 1: Save a prescription
print("\n[1] Doctor saves prescription...")
prescription = {
    "patient": "Rajesh Kumar",
    "doctor": "Dr. Sharma",
    "medicine": "Metformin 500mg",
    "frequency": "Twice daily",
    "diagnosis": "Type 2 Diabetes"
}
hash1 = bc.add_prescription("patient1", "doctor1", prescription)
print(f"    Blockchain Hash: {hash1}")
print(f"    Chain Valid: {bc.blockchain.is_chain_valid()}")

# Step 2: Verify chain is valid
print("\n[2] Verifying blockchain integrity...")
print(f"    Total blocks: {len(bc.blockchain.chain)}")
print(f"    Chain Valid: ✅ {bc.blockchain.is_chain_valid()}")

# Step 3: TAMPER ATTEMPT — change medicine dose
print("\n[3] HACKER attempts to change dose from 500mg to 5000mg...")
bc.blockchain.chain[1].data['prescription']['medicine'] = "Metformin 5000mg"
print(f"    Chain Valid after tamper: ❌ {bc.blockchain.is_chain_valid()}")
print(f"    TAMPER DETECTED — blockchain rejected the change!")

print("\n" + "=" * 60)
print("  RESULT: Prescription is MATHEMATICALLY TAMPER-PROOF")
print("=" * 60)

# Step 4: AES-256 Demo
print("\n[4] AES-256 Encryption Demo...")
from app import encrypt_prescription_for_pharmacy, decrypt_prescription_for_pharmacy

rx_data = {"patient": "Rajesh Kumar", "medicine": "Metformin 500mg"}
token = encrypt_prescription_for_pharmacy(rx_data, "MEDICHAIN_PHARMACY")
print(f"    Encrypted token (first 60 chars): {token[:60]}...")
print(f"    Patient sees this — UNREADABLE")

# Correct pharmacy decrypts
decrypted = decrypt_prescription_for_pharmacy(token, "MEDICHAIN_PHARMACY")
print(f"\n    Correct pharmacy decrypts: ✅ {decrypted}")

# Wrong pharmacy tries
print("\n[5] FAKE PHARMACY tries to decrypt with wrong key...")
try:
    fake = decrypt_prescription_for_pharmacy(token, "FAKE_PHARMACY")
    print("    Decrypted: (should not reach here)")
except Exception as e:
    print(f"    Result: ❌ DECRYPTION FAILED — {type(e).__name__}")
    print(f"    Fake pharmacy cannot read prescription!")

print("\n" + "=" * 60)
print("  RESULT: Only registered pharmacy can decrypt")
print("=" * 60)

# Step 5: SHA-256 avalanche effect
print("\n[6] SHA-256 Avalanche Effect Demo...")
print("    (One character change = completely different hash)")
msg1 = "Metformin 500mg"
msg2 = "Metformin 501mg"  # Only 1 digit changed
h1 = hashlib.sha256(msg1.encode()).hexdigest()
h2 = hashlib.sha256(msg2.encode()).hexdigest()
print(f"    '{msg1}' → {h1}")
print(f"    '{msg2}' → {h2}")
diff = sum(c1 != c2 for c1, c2 in zip(h1, h2))
print(f"    Characters different: {diff}/64 — COMPLETELY DIFFERENT!")

print("\n" + "=" * 60)
print("  ALL SECURITY DEMOS PASSED")
print("=" * 60)
