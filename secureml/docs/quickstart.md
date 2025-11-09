# Quick Start Guide

Get started with SecureML in 5 minutes!

## 1. Install SecureML

```bash
pip install secureml
pip install model-signing  # OpenSSF dependency
```

## 2. Basic Usage

### Sign a Model

```python
from secureml import SecureModel
import joblib

# Load your trained model
model = joblib.load("your_model.pkl")

# Create SecureModel instance
secure_model = SecureModel(model)

# Sign and save
secure_model.sign_and_save(
    output_path="secure_model.sml",
    identity="your-email@company.com",
    version="1.0.0",
    description="Production model"
)
```

### Verify and Load

```python
from secureml import SecureModel

# Load and verify
model = SecureModel.load("secure_model.sml", verify=True)

# Check verification status
if model.is_verified:
    print("✓ Model verified successfully!")

    # Use the model
    predictions = model.predict(X_test)
```

## 3. Framework-Specific Examples

### XGBoost

```python
from secureml import SecureModel
import xgboost as xgb

# Train XGBoost model
model = xgb.XGBClassifier()
model.fit(X_train, y_train)

# Secure it
secure_model = SecureModel(model)
secure_model.sign_and_save("xgb_model.sml", identity="ml@company.com")
```

### PyTorch

```python
import torch
from secureml import SecureModel

# Save PyTorch model
torch.save(model.state_dict(), "model.pth")

# Secure the saved model
# (Framework-specific handler would be used)
```

### Scikit-learn

```python
from sklearn.ensemble import RandomForestClassifier
from secureml import SecureModel

model = RandomForestClassifier()
model.fit(X_train, y_train)

secure_model = SecureModel(model)
secure_model.sign_and_save("rf_model.sml", identity="ml@company.com")
```

## 4. Security Levels

Choose your security level:

```python
from secureml import SecureModel
from secureml.utils.config import SecurityLevel

# Basic (development)
model = SecureModel(model, security_level=SecurityLevel.BASIC)

# Standard (production)
model = SecureModel(model, security_level=SecurityLevel.STANDARD)

# Enterprise (regulated industries)
model = SecureModel(model, security_level=SecurityLevel.ENTERPRISE)

# Maximum (high-security)
model = SecureModel(model, security_level=SecurityLevel.MAXIMUM)
```

## 5. CLI Usage

```bash
# Sign a model
secureml sign model.pkl --identity ml@company.com

# Verify a model
secureml verify model.sml

# Get model info
secureml info model.sml
```

## 6. Advanced Features

### Enterprise Signing with AWS KMS

```python
from secureml.api.advanced import AdvancedSecureModel

advanced = AdvancedSecureModel(model)
advanced.add_signature(
    identity="prod-ml@company.com",
    use_cloud_kms=True,
    kms_key_id="arn:aws:kms:us-east-1:123:key/abc",
    cloud_provider="aws"
)
```

### Compliance Validation

```python
from secureml.utils.config import ComplianceFramework

# Validate compliance
report = advanced.validate_compliance(
    frameworks=[ComplianceFramework.SOC2, ComplianceFramework.HIPAA]
)
print(f"Status: {report['overall_status']}")
```

## Next Steps

- [Installation Guide](installation.md)
- [Model Support](model_support.md)
- [Enterprise Features](enterprise_features.md)
- [Examples](../examples/)
- [API Reference](api_reference/)

## Common Patterns

### CI/CD Integration

```python
# In your CI/CD pipeline
from secureml import SecureModel

# Load model
model = SecureModel.load("model.sml", verify=True)

# Verify before deployment
if not model.is_verified:
    raise Exception("Model verification failed!")

# Deploy verified model
deploy_model(model)
```

### Model Registry Integration

```python
# Sign before uploading to registry
secure_model = SecureModel(model)
secure_model.sign_and_save("model.sml", identity="ci@company.com")

# Upload to registry
upload_to_registry("model.sml")
```

## Tips

1. **Always verify in production** - Set `verify=True` when loading
2. **Use appropriate security level** - Match your environment
3. **Keep audit logs** - Enable for compliance
4. **Rotate keys regularly** - Follow security best practices
5. **Test verification** - Include in your test suite

## Troubleshooting

### Signature verification fails

1. Check identity matches what was used to sign
2. Ensure model file wasn't modified
3. Verify OpenSSF is installed correctly

### Performance concerns

1. Use appropriate chunk sizes for large models
2. Consider disabling Merkle trees for speed
3. Use cloud KMS for parallel signing

## Support

- Documentation: https://docs.secureml.ai
- Examples: https://github.com/secureml/secureml/tree/main/examples
- Issues: https://github.com/secureml/secureml/issues
