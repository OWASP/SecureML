# SecureML

**AI Model Security built on OpenSSF Model Signing**

SecureML is the "Stripe for model security" - making enterprise-grade AI model protection accessible, user-friendly, and production-ready for every organization.

## Quick Start

```bash
pip install secureaiml
```

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

- 🎯 Universal Model Support (XGBoost, PyTorch, TensorFlow, scikit-learn, LLMs)
- 🔒 Built on OpenSSF Model Signing Standards
- ⚡ Simple, Pythonic API
- 🛡️ Model Watermarking for IP Protection

## Documentation

Full documentation available at: https://github.com/OWASP/SecureML

## License

Apache 2.0 - See LICENSE for details
