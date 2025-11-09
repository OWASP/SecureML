# SecureML Quick Start

## 🚀 Try It Now (2 Minutes)

```bash
# Activate environment
source venv/bin/activate

# Run examples (all work without OpenSSF!)
python examples/try_basic_usage.py        # ⭐ Start here
python examples/try_fingerprinting.py     # Tamper detection
python examples/try_compliance.py          # Regulatory compliance
```

---

## 💡 Most Common Use Cases

### 1. Wrap Your Model (10 seconds)

```python
from secureml import SecureModel

# Your existing code
model = train_your_model()

# Add this ONE line
secure_model = SecureModel(model)

# Use it exactly the same
predictions = secure_model.predict(X_test)
```

**That's it!** Your model is now wrapped with security features.

---

### 2. Detect Any Model Type

```python
from secureml.core.model_detector import UniversalModelDetector

detector = UniversalModelDetector()
info = detector.detect(your_model)

print(f"Type: {info['model_type']}")      # xgboost, pytorch, sklearn, etc.
print(f"Framework: {info['framework']}")  # XGBoost, PyTorch, scikit-learn
```

Works with: XGBoost, PyTorch, TensorFlow, sklearn, LightGBM, CatBoost, HuggingFace, ONNX

---

### 3. Check Model Integrity (Tamper Detection)

```python
from secureml.core.fingerprint import ModelFingerprint

# Create fingerprint
fp = ModelFingerprint.create(
    model_path="model.pkl",
    algorithms=["sha256"],
    enable_merkle=True
)

# Later, verify nothing changed
if not fp.verify():
    print("⚠️ Model has been tampered with!")
```

---

### 4. Validate Compliance

```python
from secureml.core.compliance import ComplianceValidator, ComplianceFramework

validator = ComplianceValidator()
report = validator.validate_compliance(
    model_path="model.pkl",
    frameworks=[ComplianceFramework.SOC2, ComplianceFramework.HIPAA]
)

print(f"Compliant: {report.overall_status}")
```

Supports: SOC2, ISO27001, FIPS 140-2, HIPAA, GDPR

---

## 🔐 Security Levels

```python
from secureml.utils.config import SecurityLevel

# Choose based on your needs:
SecureModel(model, security_level=SecurityLevel.BASIC)       # Dev/Test
SecureModel(model, security_level=SecurityLevel.STANDARD)    # Production
SecureModel(model, security_level=SecurityLevel.ENTERPRISE)  # Regulated
SecureModel(model, security_level=SecurityLevel.MAXIMUM)     # High-security
```

---

## 📁 Files You Can Run

| File | What It Does | Time |
|------|-------------|------|
| `examples/try_basic_usage.py` | Train, wrap, predict with models | 30s |
| `examples/try_fingerprinting.py` | Tamper detection, integrity checks | 20s |
| `examples/try_compliance.py` | Regulatory compliance validation | 25s |

**All work without OpenSSF installed!**

---

## 🎯 Real Example

```python
# Your existing ML pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

# Train model (your normal code)
X, y = make_classification(n_samples=1000, n_features=20)
model = RandomForestClassifier(n_estimators=100)
model.fit(X, y)

# Add SecureML (1 line!)
from secureml import SecureModel
secure_model = SecureModel(model)

# Deploy with confidence
predictions = secure_model.predict(X_test)
info = secure_model.get_info()  # Get metadata

print(f"Security: {info['security_level']}")
print(f"Framework: {info['model_info']['framework']}")
```

---

## 🔧 When You Need OpenSSF (Optional)

For signing/verification features:

```bash
pip install git+https://github.com/sigstore/model-transparency
```

Then you can:

```python
# Sign models
secure_model.sign_and_save(
    "model.sml",
    identity="ml-team@company.com"
)

# Verify signatures
verified = SecureModel.load("model.sml", verify=True)
```

---

## 💡 Tips

1. **Start Simple**: Run `python examples/try_basic_usage.py`
2. **Read Output**: Examples are self-explanatory
3. **Check USAGE_GUIDE.md**: Comprehensive guide
4. **Modify Examples**: Copy and adapt to your models

---

## 🆘 Troubleshooting

**"OpenSSF not found"**
→ It's optional! Most features work without it.

**Import errors**
→ `pip install -e ".[dev]"`

**Want to try everything?**
→ Just run the example files in order!

---

## 📚 What to Try Next

**New to ML Security?**
1. Run `python examples/try_basic_usage.py`
2. Read the output
3. Modify the code for your model

**Need Compliance?**
1. Run `python examples/try_compliance.py`
2. See which frameworks you pass
3. Adjust security level

**Need Tamper Detection?**
1. Run `python examples/try_fingerprinting.py`
2. See how integrity checks work
3. Integrate into your pipeline

---

## 🎓 Complete Learning Path

```bash
# 5 minute intro
python examples/try_basic_usage.py

# 10 minute deep dive
python examples/try_fingerprinting.py
python examples/try_compliance.py

# 20 minute mastery
cat USAGE_GUIDE.md          # Read full guide
pytest -v                    # Run tests
```

---

## 📖 Documentation

- **USAGE_GUIDE.md** - Complete usage guide
- **README.md** - Project overview
- **docs/** - Detailed documentation
- **examples/** - More examples

---

**Questions? Issues?**
→ Check USAGE_GUIDE.md for detailed answers

**Ready to start?**
```bash
python examples/try_basic_usage.py
```
