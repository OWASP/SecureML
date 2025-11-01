"""
SecureML Advanced Fingerprinting Example
Demonstrates model fingerprinting and integrity checking
"""

from secureml.core.fingerprint import ModelFingerprint
from pathlib import Path
import tempfile
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

print("=" * 70)
print("🔐 SecureML Advanced Fingerprinting")
print("=" * 70)

# ============================================================================
# USE CASE 1: Create Model Fingerprint
# ============================================================================
print("\n📊 USE CASE 1: Create Advanced Model Fingerprint")
print("-" * 70)

# Train a model
X, y = make_classification(n_samples=500, n_features=20, random_state=42)
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X, y)

# Save model
temp_dir = Path(tempfile.mkdtemp())
model_path = temp_dir / "model.pkl"
joblib.dump(model, model_path)
print(f"\n1. Model saved to: {model_path}")
print(f"   Size: {model_path.stat().st_size:,} bytes")

# Create basic fingerprint
print("\n2. Creating basic fingerprint (SHA-256)...")
fingerprint = ModelFingerprint.create(
    model_path=model_path,
    algorithms=["sha256"]
)
print(f"   ✓ SHA-256: {fingerprint.hashes['sha256'].digest[:16]}...")
print(f"   ✓ File size: {fingerprint.hashes['sha256'].file_size:,} bytes")
print(f"   ✓ Chunks: {fingerprint.hashes['sha256'].chunk_count}")

# ============================================================================
# USE CASE 2: Multi-Algorithm Fingerprinting
# ============================================================================
print("\n\n🔒 USE CASE 2: Multi-Algorithm Fingerprinting")
print("-" * 70)

print("\nCreating fingerprint with multiple algorithms...")
fingerprint_multi = ModelFingerprint.create(
    model_path=model_path,
    algorithms=["sha256", "sha512", "blake2b"],
    enable_merkle=False
)

print("\nHash digests:")
for algo, hash_result in fingerprint_multi.hashes.items():
    print(f"   • {algo.upper():10s}: {hash_result.digest[:32]}...")

# ============================================================================
# USE CASE 3: Merkle Tree Fingerprinting
# ============================================================================
print("\n\n🌲 USE CASE 3: Merkle Tree Fingerprinting")
print("-" * 70)

print("\nCreating fingerprint with Merkle tree...")
fingerprint_merkle = ModelFingerprint.create(
    model_path=model_path,
    algorithms=["sha256"],
    enable_merkle=True,
    chunk_size=1024 * 64  # 64KB chunks
)

print(f"   ✓ Merkle root: {fingerprint_merkle.merkle_root[:32]}...")
print(f"   ✓ Tree nodes: {len(fingerprint_merkle.merkle_tree)}")
print(f"   ✓ Timestamp: {fingerprint_merkle.timestamp}")

# ============================================================================
# USE CASE 4: Verify Model Integrity
# ============================================================================
print("\n\n✅ USE CASE 4: Verify Model Integrity")
print("-" * 70)

print("\n1. Verifying original model...")
is_valid = fingerprint.verify(algorithm="sha256")
print(f"   ✓ Verification result: {'PASSED' if is_valid else 'FAILED'}")

print("\n2. Simulating model tampering...")
# Modify the model file slightly
with open(model_path, "ab") as f:
    f.write(b"tampered")

print("   ⚠️  Model file modified")

print("\n3. Verifying tampered model...")
is_valid_after = fingerprint.verify(algorithm="sha256")
print(f"   ✗ Verification result: {'PASSED' if is_valid_after else 'FAILED'}")

if not is_valid_after:
    print("   ✓ Tampering detected successfully!")

# Restore model
joblib.dump(model, model_path)
print("\n4. Restoring original model...")
is_valid_restored = fingerprint.verify(algorithm="sha256")
print(f"   ✓ Verification result: {'PASSED' if is_valid_restored else 'FAILED'}")

# ============================================================================
# USE CASE 5: Save and Load Fingerprints
# ============================================================================
print("\n\n💾 USE CASE 5: Save and Load Fingerprints")
print("-" * 70)

# Save fingerprint
fp_path = temp_dir / "fingerprint.json"
print(f"\n1. Saving fingerprint to: {fp_path}")
fingerprint_multi.to_json(fp_path)
print("   ✓ Fingerprint saved")

# Load fingerprint
print("\n2. Loading fingerprint from file...")
loaded_fp = ModelFingerprint.from_json(fp_path)
print("   ✓ Fingerprint loaded")
print(f"   • Model path: {loaded_fp.model_path}")
print(f"   • Algorithms: {list(loaded_fp.hashes.keys())}")
print(f"   • Timestamp: {loaded_fp.timestamp}")

# Verify with loaded fingerprint
print("\n3. Verifying with loaded fingerprint...")
is_valid_loaded = loaded_fp.verify(algorithm="sha256")
print(f"   ✓ Verification result: {'PASSED' if is_valid_loaded else 'FAILED'}")

# ============================================================================
# USE CASE 6: Fingerprint Comparison
# ============================================================================
print("\n\n⚖️  USE CASE 6: Compare Fingerprints")
print("-" * 70)

# Create two different models
model_a = RandomForestClassifier(n_estimators=50, random_state=42)
model_b = RandomForestClassifier(n_estimators=100, random_state=42)

model_a.fit(X, y)
model_b.fit(X, y)

# Save and fingerprint both
model_a_path = temp_dir / "model_a.pkl"
model_b_path = temp_dir / "model_b.pkl"

joblib.dump(model_a, model_a_path)
joblib.dump(model_b, model_b_path)

fp_a = ModelFingerprint.create(model_a_path, algorithms=["sha256"])
fp_b = ModelFingerprint.create(model_b_path, algorithms=["sha256"])

print("\nModel A:")
print(f"   SHA-256: {fp_a.hashes['sha256'].digest[:32]}...")
print(f"   Size: {fp_a.hashes['sha256'].file_size:,} bytes")

print("\nModel B:")
print(f"   SHA-256: {fp_b.hashes['sha256'].digest[:32]}...")
print(f"   Size: {fp_b.hashes['sha256'].file_size:,} bytes")

print("\nComparison:")
hashes_match = fp_a.hashes['sha256'].digest == fp_b.hashes['sha256'].digest
print(f"   Fingerprints match: {hashes_match}")
print(f"   ✓ Models are {'identical' if hashes_match else 'different'}")

# ============================================================================
# Summary
# ============================================================================
print("\n\n" + "=" * 70)
print("✅ All fingerprinting use cases completed!")
print("=" * 70)

print("\n🔐 Key Takeaways:")
print("   • Single or multi-algorithm hashing")
print("   • Merkle tree for distributed verification")
print("   • Tamper detection works reliably")
print("   • Fingerprints can be saved/loaded")
print("   • Models can be compared by fingerprint")

print("\n💡 Next: Try compliance validation")
print("   python try_compliance.py")

# Cleanup
import shutil
shutil.rmtree(temp_dir)
