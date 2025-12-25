# SecureAIML 🔐

**Enterprise-Ready AI Model Security built on OpenSSF Model Signing**

SecureAIML is the "Stripe for model security" - making enterprise-grade AI model protection accessible, user-friendly, and production-ready for every organization.

[![PyPI version](https://badge.fury.io/py/secureaiml.svg)](https://pypi.org/project/secureaiml/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![OpenSSF](https://img.shields.io/badge/OpenSSF-Model_Signing-green.svg)](https://github.com/sigstore/model-transparency)
[![Tests](https://github.com/OWASP/SecureML/actions/workflows/test.yml/badge.svg)](https://github.com/OWASP/SecureML/actions/workflows/test.yml)

## Why SecureAIML?

In the era of AI/ML, model security is critical. SecureAIML wraps the powerful [OpenSSF Model Signing](https://github.com/sigstore/model-transparency) standard with an intuitive, enterprise-ready interface that makes securing your ML models as simple as:

## Installation

```bash
pip install secureaiml
```

## Quick Start

```python
from secureml import SecureModel
import joblib

# Load your model
model = joblib.load("model.pkl")

# Secure it in one line
secure_model = SecureModel(model)
secure_model.sign_and_save("model.sml", identity="ml-team@company.com")

# Load and verify
verified_model = SecureModel.load("model.sml", verify=True)
predictions = verified_model.predict(X_test)
```

## Features

### 🎯 Universal Model Support
- **Traditional ML**: XGBoost, scikit-learn, LightGBM, CatBoost
- **Deep Learning**: PyTorch, TensorFlow, JAX, Keras
- **Large Language Models**: HuggingFace Transformers, GGUF, SafeTensors
- **Computer Vision**: ONNX, CoreML, TensorRT, OpenVINO
- **Audio/Speech**: Whisper, Wav2Vec, SpeechT5
- **Multimodal**: CLIP, DALL-E, GPT-4V, BLIP

### 🔒 Built on OpenSSF Standards
- Full integration with [OpenSSF Model Signing](https://github.com/sigstore/model-transparency)
- Leverages Sigstore infrastructure
- Industry-standard cryptographic signing
- Keyless signing with OIDC
- Transparent and verifiable signatures

### 🏢 Enterprise Features
- **Hardware Security Module (HSM)** integration
- **Cloud KMS** support (AWS KMS, Azure Key Vault, GCP Cloud KMS)
- **Advanced fingerprinting** with Merkle trees
- **Multi-signature** workflows
- **Compliance frameworks**: SOC2, ISO27001, FIPS 140-2, HIPAA, GDPR
- **Comprehensive audit trails** and forensics

### ⚡ Developer-Friendly
- Simple, intuitive Pythonic API
- Auto-detection of model types
- Minimal configuration required
- Works with existing ML workflows
- Extensive documentation and examples

### Basic Usage

```python
from secureml import SecureModel
import joblib

# Train your model (any framework)
from xgboost import XGBClassifier
model = XGBClassifier()
model.fit(X_train, y_train)

# Secure it
secure_model = SecureModel(model)
secure_model.sign_and_save(
    "fraud_detection_model.sml",
    identity="ml-team@company.com",
    version="2.0.0",
    description="Production fraud detection model"
)

# Load and verify
model = SecureModel.load("fraud_detection_model.sml", verify=True)
if model.is_verified:
    predictions = model.predict(X_test)
```

### Enterprise Usage

```python
from secureml.api.advanced import AdvancedSecureModel
from secureml.utils.config import SecurityConfig, SecurityLevel, ComplianceFramework

# Configure enterprise security
config = SecurityConfig.from_level(SecurityLevel.ENTERPRISE)
config.enable_fingerprinting = True
config.enable_merkle_trees = True
config.compliance_frameworks = [ComplianceFramework.SOC2, ComplianceFramework.ISO27001]

# Create advanced secure model
advanced = AdvancedSecureModel(model, config=config)

# Sign with AWS KMS
advanced.add_signature(
    identity="prod-ml@company.com",
    use_cloud_kms=True,
    kms_key_id="arn:aws:kms:us-east-1:123456789:key/abc-def",
    cloud_provider="aws"
)

# Validate compliance
compliance_report = advanced.validate_compliance(
    frameworks=[ComplianceFramework.SOC2, ComplianceFramework.HIPAA],
    generate_report=True,
    report_path="compliance_report.json"
)

print(f"Compliance Status: {compliance_report['overall_status']}")
```

## Architecture

SecureML is built as an enhancement layer on top of OpenSSF Model Signing:

```
┌─────────────────────────────────────────────────────┐
│            Your Application                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│            SecureML API Layer                       │
│  • Simple API  • Advanced API  • CLI                │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│         SecureML Enterprise Features                │
│  • HSM/KMS  • Compliance  • Audit  • Forensics      │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│         OpenSSF Model Signing (Core)                │
│         Sigstore Infrastructure                     │
└─────────────────────────────────────────────────────┘
```

## Security Levels

SecureML provides four security levels to match your needs:

| Level | Use Case | Features |
|-------|----------|----------|
| **BASIC** | Development, testing | OpenSSF signing only |
| **STANDARD** | Production deployments | + Fingerprinting, audit logging |
| **ENTERPRISE** | Regulated industries | + Merkle trees, threat detection, compliance |
| **MAXIMUM** | High-security environments | + Encryption, forensics, multi-sig |

## Compliance Support

SecureML helps you meet regulatory requirements:

- **SOC 2**: System and Organization Controls
- **ISO 27001**: Information Security Management
- **FIPS 140-2**: Cryptographic Module Validation
- **HIPAA**: Healthcare data protection
- **GDPR**: EU data protection

## Documentation

- 📦 **[PyPI Package](https://pypi.org/project/secureaiml/)** - Official package on PyPI
- 🚀 **[Quick Start Guide](secureml/docs/quickstart.md)** - Get started in 5 minutes
- 📚 **[Installation Guide](secureml/docs/installation.md)** - Installation instructions
- 📖 **[Usage Guide](secureml/docs/USAGE_GUIDE.md)** - Comprehensive usage documentation
- 🔒 **[Watermarking Features](secureml/docs/WATERMARKING_FEATURES.md)** - Model watermarking guide
- 🛡️ **[Threat Model](secureml/docs/threat_model.md)** - Security analysis and limitations
- 🔗 **[OpenSSF Integration](secureml/docs/openssf_integration.md)** - OpenSSF Model Signing integration

## Examples

### XGBoost Model
```python
from secureml import SecureModel
import xgboost as xgb

model = xgb.XGBClassifier()
model.fit(X_train, y_train)

secure_model = SecureModel(model)
secure_model.sign_and_save("xgb_model.sml", identity="data-science@company.com")
```

### PyTorch Model
```python
import torch
from secureml import SecureModel

model = torch.nn.Sequential(...)
torch.save(model.state_dict(), "model.pth")

secure_model = SecureModel.load_from_path("model.pth")
secure_model.sign_and_save("pytorch_model.sml", identity="ai-team@company.com")
```

### HuggingFace Model
```python
from transformers import AutoModel
from secureml import SecureModel

model = AutoModel.from_pretrained("bert-base-uncased")
model.save_pretrained("./my_model")

secure_model = SecureModel.load_from_path("./my_model")
secure_model.sign_and_save("bert_model.sml", identity="llm-team@company.com")
```

## Installation Options

```bash
# Basic installation
pip install secureaiml

# With ML framework support
pip install secureaiml[xgboost,pytorch,sklearn]

# With CLI tools
pip install secureaiml[cli]

# Everything (all ML frameworks + CLI + dev tools)
pip install secureaiml[all]
```

## CLI Usage

```bash
# Sign a model
secureml sign model.pkl --identity "ml-team@company.com" --output model.sml

# Verify a model
secureml verify model.sml

# Get model info
secureml info model.sml

# Validate compliance
secureml compliance model.sml --framework soc2 --framework iso27001

# Generate audit report
secureml audit --start-date 2024-01-01 --end-date 2024-12-31 --output audit.json
```

## Integration Examples

### MLflow Integration
```python
import mlflow
from secureml.integrations.mlflow_integration import SecureMLflowModel

with mlflow.start_run():
    model = train_model()

    # Log with SecureML
    secure_model = SecureMLflowModel(model)
    secure_model.log_model(
        "model",
        signature=True,
        identity="ml-team@company.com"
    )
```

### HuggingFace Hub Integration
```python
from secureml.integrations.huggingface_integration import SecureHFModel

secure_model = SecureHFModel.from_pretrained("bert-base-uncased")
secure_model.sign(identity="ai-team@company.com")
secure_model.push_to_hub("my-org/secure-bert", signed=True)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Security

For security issues, please see [SECURITY.md](SECURITY.md).

## License

Apache 2.0 - See [LICENSE](LICENSE) for details.

## Acknowledgments

Built on top of:
- [OpenSSF Model Signing](https://github.com/sigstore/model-transparency)
- [Sigstore](https://www.sigstore.dev/)
- The amazing open-source ML community

## Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/OWASP/SecureML/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/OWASP/SecureML/discussions)
- 📖 **Documentation:** [GitHub Docs](https://github.com/OWASP/SecureML/tree/master/secureml/docs)
- 📦 **PyPI:** [pypi.org/project/secureaiml](https://pypi.org/project/secureaiml/)

## OWASP Project

SecureAIML is an OWASP project focused on making ML model security accessible to everyone.

- **OWASP Page:** [OWASP SecureML](https://owasp.org/www-project-secureml/)
- **GitHub:** [OWASP/SecureML](https://github.com/OWASP/SecureML)

---

**SecureAIML** - Making AI model security accessible to everyone 🚀

*An OWASP Project*
