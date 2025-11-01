# Installation Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager
- (Optional) OpenSSF model-signing CLI

## Basic Installation

### Install from PyPI (when published)

```bash
pip install secureml
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/secureml/secureml.git
cd secureml

# Install in development mode
pip install -e .
```

## Optional Dependencies

### ML Framework Support

Install support for specific ML frameworks:

```bash
# XGBoost
pip install secureml[xgboost]

# PyTorch
pip install secureml[pytorch]

# TensorFlow
pip install secureml[tensorflow]

# scikit-learn
pip install secureml[sklearn]

# HuggingFace Transformers
pip install secureml[huggingface]

# All ML frameworks
pip install secureml[ml-all]
```

### CLI Interface

For rich CLI experience:

```bash
pip install secureml[cli]
```

### Enterprise Features

For HSM/KMS integration:

```bash
pip install secureml[enterprise]
```

### Development Tools

For development:

```bash
pip install secureml[dev]
```

### Complete Installation

Install everything:

```bash
pip install secureml[all]
```

## OpenSSF Model Signing

SecureML requires OpenSSF model-signing to be installed:

```bash
pip install model-signing
```

Verify installation:

```bash
model-signing --version
```

## Verification

Verify SecureML installation:

```python
import secureml
print(secureml.__version__)

from secureml import SecureModel
print("SecureML installed successfully!")
```

## Troubleshooting

### Issue: OpenSSF not found

```bash
# Install OpenSSF model-signing
pip install model-signing

# Verify it's in PATH
which model-signing
```

### Issue: Import errors

```bash
# Reinstall SecureML
pip uninstall secureml
pip install secureml
```

### Issue: Permission errors

```bash
# Install with --user flag
pip install --user secureml
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Basic Examples](../examples/basic_usage/)
- [API Reference](api_reference/)
