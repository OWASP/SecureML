# SecureML Usage Guide

Complete guide with hands-on examples you can run right now!

## 🚀 Quick Start (5 Minutes)

### Run the Examples

All these work **without OpenSSF installed**:

```bash
# Activate virtual environment
source venv/bin/activate

# Basic usage - wrap and use models
python examples/try_basic_usage.py

# Advanced fingerprinting
python examples/try_fingerprinting.py

# Compliance validation
python examples/try_compliance.py
```

---

## 📚 Use Cases

### 1. **Wrap Any ML Model** ⭐ Most Common

```python
from secureml import SecureModel
from sklearn.ensemble import RandomForestClassifier

# Your existing code
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Add SecureML wrapper - 1 line!
secure_model = SecureModel(model)

# Use exactly like before
predictions = secure_model.predict(X_test)
```

**When to use**: Production deployments, model versioning, audit trails

---

### 2. **Detect Model Types Automatically**

```python
from secureml.core.model_detector import UniversalModelDetector

detector = UniversalModelDetector()

# Works with any model
info = detector.detect(your_model)
print(f"Type: {info['model_type']}")
print(f"Framework: {info['framework']}")
```

**Supports**: XGBoost, PyTorch, TensorFlow, sklearn, LightGBM, CatBoost, HuggingFace, ONNX, and more!

**When to use**: Model registry, automated workflows, multi-framework pipelines

---

### 3. **Choose Security Level**

```python
from secureml import SecureModel
from secureml.utils.config import SecurityLevel

# Development
model = SecureModel(model, security_level=SecurityLevel.BASIC)

# Production
model = SecureModel(model, security_level=SecurityLevel.STANDARD)

# Regulated industries (finance, healthcare)
model = SecureModel(model, security_level=SecurityLevel.ENTERPRISE)

# High-security environments
model = SecureModel(model, security_level=SecurityLevel.MAXIMUM)
```

| Level | Features |
|-------|----------|
| **BASIC** | Minimal overhead, dev/test |
| **STANDARD** | Production-ready, audit logging |
| **ENTERPRISE** | Compliance, advanced security |
| **MAXIMUM** | Encryption, forensics, multi-sig |

**When to use**: Match to your regulatory requirements

---

### 4. **Model Fingerprinting** (Tamper Detection)

```python
from secureml.core.fingerprint import ModelFingerprint

# Create fingerprint
fingerprint = ModelFingerprint.create(
    model_path="model.pkl",
    algorithms=["sha256", "sha512"],
    enable_merkle=True  # For large models
)

# Later, verify integrity
is_valid = fingerprint.verify()
if not is_valid:
    print("⚠️ Model has been tampered with!")
```

**When to use**:
- Detect unauthorized model modifications
- Distributed model verification
- Supply chain security

---

### 5. **Compliance Validation**

```python
from secureml.core.compliance import ComplianceValidator
from secureml.utils.config import ComplianceFramework

validator = ComplianceValidator()

# Check compliance
report = validator.validate_compliance(
    model_path="model.pkl",
    frameworks=[
        ComplianceFramework.SOC2,
        ComplianceFramework.HIPAA
    ]
)

print(f"Status: {report.overall_status}")
print(f"Compliant: {report.summary['compliant']}/{report.summary['total_checks']}")
```

**Supported Frameworks**:
- SOC 2 (System and Organization Controls)
- ISO 27001 (Information Security)
- FIPS 140-2 (Cryptographic Standards)
- HIPAA (Healthcare)
- GDPR (Data Protection)

**When to use**: Audits, regulatory reporting, certification

---

### 6. **Sign Models** (Requires OpenSSF)

```python
from secureml import SecureModel

# Sign and save
secure_model = SecureModel(model)
secure_model.sign_and_save(
    output_path="model.sml",
    identity="ml-team@company.com",
    version="2.0.0",
    description="Production fraud detection"
)

# Load and verify
verified_model = SecureModel.load("model.sml", verify=True)
if verified_model.is_verified:
    predictions = verified_model.predict(X_test)
```

**Requires**: `pip install git+https://github.com/sigstore/model-transparency`

**When to use**: Production deployments, model distribution, supply chain security

---

## 🎯 Real-World Scenarios

### Scenario 1: **ML Engineer in Production**

```python
# Train model
model = train_my_model(data)

# Wrap with SecureML
from secureml import SecureModel
secure_model = SecureModel(model, security_level="standard")

# Deploy with confidence
deploy_to_production(secure_model)

# Monitor in production
info = secure_model.get_info()
log_deployment(info)
```

---

### Scenario 2: **Data Scientist Sharing Models**

```python
# Train model
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Sign before sharing
from secureml import SecureModel
secure_model = SecureModel(model)

# When OpenSSF is installed:
secure_model.sign_and_save(
    "model.sml",
    identity="data-science@company.com",
    experiment_id="exp-2024-001",
    accuracy=0.95
)

# Share model.sml with team
# They can verify authenticity before using
```

---

### Scenario 3: **Compliance Officer Auditing**

```python
from secureml.core.compliance import ComplianceValidator
from secureml.utils.config import ComplianceFramework

# Validate all models in registry
validator = ComplianceValidator()

for model_path in model_registry.list_models():
    report = validator.validate_compliance(
        model_path=model_path,
        frameworks=[ComplianceFramework.SOC2]
    )

    if report.overall_status != "compliant":
        send_alert(model_path, report)

# Generate audit report
validator.generate_report_document(
    report, "audit_2024.json"
)
```

---

### Scenario 4: **Security Team Monitoring**

```python
from secureml.core.fingerprint import ModelFingerprint

# Create fingerprints for all production models
fingerprints = {}
for model_name, model_path in production_models.items():
    fp = ModelFingerprint.create(
        model_path,
        algorithms=["sha256", "sha512"],
        enable_merkle=True
    )
    fp.to_json(f"fingerprints/{model_name}.json")
    fingerprints[model_name] = fp

# Daily integrity check
for model_name, fp in fingerprints.items():
    if not fp.verify():
        alert_security_team(
            f"Model {model_name} integrity check FAILED!"
        )
```

---

## 🔧 Configuration Examples

### Custom Security Configuration

```python
from secureml.utils.config import SecurityConfig, ComplianceFramework

# Create custom config
config = SecurityConfig(
    security_level="enterprise",
    enable_fingerprinting=True,
    enable_merkle_trees=True,
    enable_audit_logging=True,
    hash_algorithms=["sha256", "sha512", "blake2b"],
    compliance_frameworks=[
        ComplianceFramework.SOC2,
        ComplianceFramework.ISO27001
    ]
)

# Use with SecureModel
secure_model = SecureModel(model, config=config)
```

---

### Save/Load Configuration

```python
# Save config
config.to_yaml("security_config.yaml")

# Load config
config = SecurityConfig.from_yaml("security_config.yaml")
```

---

## 📊 Comparison with Other Solutions

| Feature | SecureML | Manual Hashing | Cloud-Only Solutions |
|---------|----------|----------------|---------------------|
| **OpenSSF Standard** | ✅ Built-in | ❌ Manual | ❌ Proprietary |
| **Universal ML Support** | ✅ All frameworks | ✅ Any file | ❌ Limited |
| **Compliance Validation** | ✅ Automated | ❌ Manual | ⚠️ Some |
| **On-Premise** | ✅ Yes | ✅ Yes | ❌ Cloud-only |
| **Enterprise Features** | ✅ HSM/KMS | ❌ No | ✅ Yes |
| **Easy to Use** | ✅ 2 lines | ❌ Complex | ⚠️ Vendor lock-in |

---

## 🐍 Framework-Specific Examples

### XGBoost

```python
import xgboost as xgb
from secureml import SecureModel

model = xgb.XGBClassifier()
model.fit(X_train, y_train)

secure_model = SecureModel(model)
secure_model.sign_and_save("xgb_model.sml", identity="ml@company.com")
```

### PyTorch

```python
import torch
from secureml import SecureModel

# Save PyTorch model
torch.save(model.state_dict(), "model.pth")

# Secure it (when OpenSSF installed)
# Would sign the .pth file
```

### TensorFlow

```python
import tensorflow as tf
from secureml import SecureModel

model = tf.keras.Sequential([...])
model.fit(X_train, y_train)

# Save and secure
model.save("tf_model")
# Would sign the saved model directory
```

### scikit-learn

```python
from sklearn.ensemble import GradientBoostingClassifier
from secureml import SecureModel

model = GradientBoostingClassifier()
model.fit(X_train, y_train)

secure_model = SecureModel(model)
# Works immediately!
```

---

## 📝 Best Practices

### 1. **Always Verify in Production**

```python
# DON'T
model = SecureModel.load("model.sml", verify=False)

# DO
model = SecureModel.load("model.sml", verify=True)
if not model.is_verified:
    raise SecurityError("Model verification failed!")
```

### 2. **Use Appropriate Security Levels**

- **Development**: BASIC
- **Staging**: STANDARD
- **Production**: STANDARD or ENTERPRISE
- **Regulated**: ENTERPRISE or MAXIMUM

### 3. **Enable Audit Logging in Production**

```python
config = SecurityConfig.from_level(SecurityLevel.ENTERPRISE)
config.enable_audit_logging = True

secure_model = SecureModel(model, config=config)
```

### 4. **Regular Integrity Checks**

```python
# In your monitoring system
def check_model_integrity():
    for model in production_models:
        fp = ModelFingerprint.from_json(f"{model}_fingerprint.json")
        if not fp.verify():
            alert_security_team(model)
```

### 5. **Document Model Metadata**

```python
secure_model.sign_and_save(
    "model.sml",
    identity="ml-team@company.com",
    version="2.1.0",
    description="Fraud detection model",
    training_date="2024-01-15",
    accuracy=0.94,
    dataset="fraud_v2",
    compliance="SOC2-ready"
)
```

---

## 🔍 Troubleshooting

### Issue: "OpenSSF not found"

**Solution**: SecureML works without OpenSSF for:
- Model wrapping
- Detection
- Fingerprinting
- Compliance checking

For signing/verification:
```bash
pip install git+https://github.com/sigstore/model-transparency
```

### Issue: Import errors

```bash
# Reinstall
pip install -e ".[dev]"
```

### Issue: Model type not detected

```python
# Use strict mode to see error
detector = UniversalModelDetector()
info = detector.detect(model, strict=True)
```

---

## 📚 Additional Resources

- **Examples**: `examples/` directory
- **Tests**: `tests/` directory
- **Docs**: `docs/` directory
- **API Reference**: Coming soon!

---

## 💡 Tips & Tricks

### Tip 1: Chain Multiple Security Checks

```python
from secureml import SecureModel
from secureml.core.fingerprint import ModelFingerprint
from secureml.core.compliance import ComplianceValidator

# 1. Wrap model
secure_model = SecureModel(model)

# 2. Create fingerprint
fp = ModelFingerprint.create(...)

# 3. Validate compliance
validator = ComplianceValidator()
report = validator.validate_compliance(...)

# All checks passed? Deploy!
```

### Tip 2: Use in CI/CD Pipelines

```python
# In your CI script
def validate_model(model_path):
    # Load model
    model = SecureModel.load(model_path, verify=True)

    # Check compliance
    validator = ComplianceValidator()
    report = validator.validate_compliance(
        model_path,
        frameworks=[ComplianceFramework.SOC2]
    )

    # Deploy only if verified and compliant
    if model.is_verified and report.overall_status == "compliant":
        deploy_to_production(model)
    else:
        raise Exception("Model validation failed!")
```

### Tip 3: Batch Processing

```python
# Process multiple models
for model_file in Path("models/").glob("*.pkl"):
    secure_model = SecureModel.load_from_path(model_file)
    info = secure_model.get_info()
    print(f"{model_file}: {info['model_type']}")
```

---

## 🎓 Learning Path

**Beginner** → Run `python examples/try_basic_usage.py`
- Understand model wrapping
- Learn security levels
- Make predictions

**Intermediate** → Run `python examples/try_fingerprinting.py`
- Create fingerprints
- Verify integrity
- Detect tampering

**Advanced** → Run `python examples/try_compliance.py`
- Validate compliance
- Generate reports
- Multi-framework checking

**Expert** → Integrate with your production system
- CI/CD pipelines
- Model registries
- Security monitoring

---

## ❓ FAQ

**Q: Do I need OpenSSF installed?**
A: No! Most features work without it. Signing/verification requires OpenSSF.

**Q: What models are supported?**
A: All major frameworks: XGBoost, PyTorch, TensorFlow, sklearn, LightGBM, CatBoost, HuggingFace, ONNX, and more!

**Q: Is it production-ready?**
A: Core features are stable. Full production readiness coming in v1.0.

**Q: How does it compare to manual signing?**
A: Much simpler! 2 lines vs. complex OpenSSF CLI commands.

**Q: Can I use it with existing code?**
A: Yes! Just wrap your model with `SecureModel(model)`.

---

**Ready to secure your models? Start with:**
```bash
python examples/try_basic_usage.py
```
