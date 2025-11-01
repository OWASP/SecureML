"""
Basic SecureML Usage Example
Works without OpenSSF model-signing installed
"""

from secureml import SecureModel
from secureml.core.model_detector import UniversalModelDetector
from secureml.utils.config import SecurityLevel
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
import numpy as np

print("=" * 70)
print("🔐 SecureML Basic Usage Example")
print("=" * 70)

# ============================================================================
# USE CASE 1: Train and Wrap a Model
# ============================================================================
print("\n📊 USE CASE 1: Train and Wrap a Model")
print("-" * 70)

# Generate sample data
print("\n1. Generating training data...")
X_train, y_train = make_classification(
    n_samples=1000,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=42
)
X_test, y_test = make_classification(
    n_samples=200,
    n_features=20,
    n_informative=15,
    n_redundant=5,
    random_state=43
)
print(f"   ✓ Training samples: {len(X_train)}")
print(f"   ✓ Test samples: {len(X_test)}")

# Train a model
print("\n2. Training RandomForest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42
)
model.fit(X_train, y_train)
train_accuracy = model.score(X_train, y_train)
test_accuracy = model.score(X_test, y_test)
print(f"   ✓ Training accuracy: {train_accuracy:.2%}")
print(f"   ✓ Test accuracy: {test_accuracy:.2%}")

# Wrap with SecureML
print("\n3. Wrapping model with SecureML...")
secure_model = SecureModel(
    model=model,
    security_level=SecurityLevel.STANDARD
)
print(f"   ✓ Model wrapped with {secure_model.security_level.value} security")

# Make predictions
print("\n4. Making predictions with SecureModel...")
predictions = secure_model.predict(X_test[:5])
probabilities = secure_model.predict_proba(X_test[:5])
print(f"   ✓ Predictions: {predictions}")
print(f"   ✓ First prediction confidence: {probabilities[0].max():.2%}")

# ============================================================================
# USE CASE 2: Model Detection
# ============================================================================
print("\n\n🔍 USE CASE 2: Automatic Model Detection")
print("-" * 70)

detector = UniversalModelDetector()

# Detect sklearn model
print("\n1. Detecting sklearn model...")
info = detector.detect(model)
print(f"   ✓ Model type: {info['model_type']}")
print(f"   ✓ Framework: {info['framework']}")
print(f"   ✓ Class: {info['class_name']}")

# ============================================================================
# USE CASE 3: Security Levels
# ============================================================================
print("\n\n🔒 USE CASE 3: Different Security Levels")
print("-" * 70)

for level in [SecurityLevel.BASIC, SecurityLevel.STANDARD,
              SecurityLevel.ENTERPRISE, SecurityLevel.MAXIMUM]:
    print(f"\n{level.value.upper()}:")
    secure = SecureModel(model, security_level=level)
    info = secure.get_info()
    config = info['config']
    print(f"   • Fingerprinting: {config['enable_fingerprinting']}")
    print(f"   • Merkle trees: {config['enable_merkle_trees']}")
    print(f"   • Audit logging: {config['enable_audit_logging']}")
    print(f"   • Encryption: {config['enable_encryption']}")

# ============================================================================
# USE CASE 4: Model Metadata
# ============================================================================
print("\n\n📋 USE CASE 4: Extract Model Information")
print("-" * 70)

secure_model = SecureModel(model, security_level=SecurityLevel.ENTERPRISE)
info = secure_model.get_info()

print("\nModel Information:")
print(f"   • Security level: {info['security_level']}")
print(f"   • Verified: {info['verified']}")
print(f"   • Framework: {info['model_info'].get('framework', 'N/A')}")
print(f"   • Model type: {info['model_info'].get('model_type', 'N/A')}")

# ============================================================================
# USE CASE 5: Compare Models
# ============================================================================
print("\n\n⚖️  USE CASE 5: Compare Multiple Models")
print("-" * 70)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

models = {
    'RandomForest': RandomForestClassifier(n_estimators=50, random_state=42),
    'LogisticRegression': LogisticRegression(random_state=42),
    'DecisionTree': DecisionTreeClassifier(random_state=42)
}

print("\nTraining and comparing models...")
for name, mdl in models.items():
    mdl.fit(X_train, y_train)
    secure = SecureModel(mdl)
    accuracy = secure.predict(X_test)
    score = (accuracy == y_test).mean()

    # Detect model info
    detector_info = detector.detect(mdl)

    print(f"\n{name}:")
    print(f"   • Accuracy: {score:.2%}")
    print(f"   • Type: {detector_info['model_type']}")
    print(f"   • Class: {detector_info['class_name']}")

# ============================================================================
# Summary
# ============================================================================
print("\n\n" + "=" * 70)
print("✅ All basic use cases completed successfully!")
print("=" * 70)

print("\n📝 Note: These examples work WITHOUT OpenSSF model-signing.")
print("   For signing/verification features, install:")
print("   pip install git+https://github.com/sigstore/model-transparency")

print("\n💡 Try these next:")
print("   • python try_advanced_usage.py")
print("   • python try_fingerprinting.py")
print("   • python try_compliance.py")
