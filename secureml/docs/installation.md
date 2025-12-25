# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Basic Installation

### Install from PyPI

```bash
pip install secureaiml
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/OWASP/SecureML.git
cd SecureML/secureml

# Install in development mode
pip install -e src
```

## Optional Dependencies

### ML Framework Support

Install support for specific ML frameworks:

```bash
# XGBoost
pip install secureaiml[xgboost]

# PyTorch
pip install secureaiml[pytorch]

# TensorFlow
pip install secureaiml[tensorflow]

# scikit-learn
pip install secureaiml[sklearn]

# HuggingFace Transformers
pip install secureaiml[huggingface]

# All ML frameworks
pip install secureaiml[ml-all]
```

### CLI Interface

For rich CLI experience:

```bash
pip install secureaiml[cli]
```

### Enterprise Features

For HSM/KMS integration:

```bash
pip install secureaiml[enterprise]
```

### Development Tools

For development:

```bash
pip install secureaiml[dev]
```

### Complete Installation

Install everything:

```bash
pip install secureaiml[all]
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

### Issue: Import errors

```bash
# Reinstall SecureAIML
pip uninstall secureaiml
pip install secureaiml
```

### Issue: Permission errors

```bash
# Install with --user flag
pip install --user secureaiml
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Usage Guide](USAGE_GUIDE.md)
- [Watermarking Features](WATERMARKING_FEATURES.md)
- [Examples](../examples/)
