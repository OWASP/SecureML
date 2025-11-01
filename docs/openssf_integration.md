# OpenSSF Model Signing Integration

SecureML is built on top of [OpenSSF Model Signing](https://github.com/sigstore/model-transparency), providing an enterprise-friendly wrapper around this powerful open standard.

## What is OpenSSF Model Signing?

OpenSSF Model Signing is an open-source standard for signing and verifying machine learning models using Sigstore infrastructure. It provides:

- **Cryptographic signing** of ML models
- **Keyless signing** using OIDC providers
- **Transparency logs** via Sigstore
- **Verification** of model integrity and provenance

## How SecureML Uses OpenSSF

SecureML enhances OpenSSF Model Signing by:

1. **Simplifying the interface** - Complex operations become one-liners
2. **Adding enterprise features** - HSM, KMS, compliance
3. **Universal model support** - Works with any ML framework
4. **Enhanced security** - Fingerprinting, Merkle trees, multi-sig
5. **Better user experience** - Intuitive API, auto-detection

## Architecture

```
┌─────────────────────────────────────┐
│      SecureML User API              │
│  (Simple, Framework-Agnostic)       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    SecureML OpenSSF Wrapper         │
│  (Enhanced Features & UX)           │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    OpenSSF Model Signing CLI        │
│  (Core Cryptographic Operations)    │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│      Sigstore Infrastructure        │
│  (Transparency Logs, Fulcio CA)     │
└─────────────────────────────────────┘
```

## Under the Hood

When you call `secure_model.sign()`, SecureML:

1. **Prepares the model** - Saves to standard format
2. **Calls OpenSSF** - Invokes `model-signing sign` command
3. **Enhances metadata** - Adds SecureML-specific information
4. **Creates fingerprint** - Optional advanced fingerprinting
5. **Packages result** - Creates .sml package

Example OpenSSF command SecureML generates:

```bash
model-signing sign model.pkl \\
  --output model.pkl.sig \\
  --identity ml-team@company.com
```

## Compatibility

### Full OpenSSF Compatibility

SecureML packages are fully compatible with OpenSSF tools:

```bash
# Sign with SecureML
python -c "from secureml import SecureModel; ..."

# Verify with OpenSSF directly
model-signing verify model.pkl --signature model.pkl.sig
```

### Migrating from OpenSSF

If you're already using OpenSSF Model Signing:

```python
from secureml import SecureModel

# Load an OpenSSF-signed model
model = SecureModel.load_openssf_signed(
    model_path="model.pkl",
    signature_path="model.pkl.sig"
)

# Enhance with SecureML features
model.add_fingerprint()
model.validate_compliance([ComplianceFramework.SOC2])

# Save as SecureML package
model.save("model.sml")
```

## OpenSSF Features Available in SecureML

### 1. Keyless Signing with OIDC

```python
# Uses your OIDC provider (GitHub, Google, etc.)
secure_model.sign(identity="github-user@users.noreply.github.com")
```

### 2. Transparency Logs

All signatures are recorded in Sigstore's transparency log:

```python
# Verify against transparency log
model = SecureModel.load("model.sml", verify=True, check_transparency_log=True)
```

### 3. Certificate-based Signing

```python
# Use certificate for signing
secure_model.sign(
    identity="ml-team@company.com",
    certificate_path="signing.crt",
    private_key_path="signing.key"
)
```

## SecureML Enhancements

Beyond OpenSSF, SecureML adds:

### 1. Model Fingerprinting

```python
from secureml.core.fingerprint import ModelFingerprint

# Create advanced fingerprint
fp = ModelFingerprint.create(
    model_path,
    algorithms=["sha256", "sha512", "blake2b"],
    enable_merkle=True
)
```

### 2. HSM/KMS Integration

```python
# Sign with AWS KMS
from secureml.api.advanced import AdvancedSecureModel

advanced = AdvancedSecureModel(model)
advanced.add_signature(
    identity="prod@company.com",
    use_cloud_kms=True,
    kms_key_id="arn:aws:kms:...",
    cloud_provider="aws"
)
```

### 3. Compliance Validation

```python
# Validate against compliance frameworks
from secureml.utils.config import ComplianceFramework

report = model.validate_compliance([
    ComplianceFramework.SOC2,
    ComplianceFramework.ISO27001
])
```

## Best Practices

### 1. Use OIDC When Possible

OIDC provides keyless signing without key management overhead:

```python
# Keyless signing via OIDC
secure_model.sign(identity="github-user@users.noreply.github.com")
```

### 2. Verify Against Transparency Logs

Always check transparency logs in production:

```python
model = SecureModel.load(
    "model.sml",
    verify=True,
    check_transparency_log=True
)
```

### 3. Combine with Enterprise Features

Use OpenSSF for signing, SecureML for enterprise features:

```python
# OpenSSF handles cryptography
secure_model.sign(identity="ml@company.com")

# SecureML handles compliance
secure_model.validate_compliance([ComplianceFramework.SOC2])
```

## Troubleshooting

### OpenSSF Not Found

```bash
# Install OpenSSF model-signing
pip install model-signing

# Verify installation
model-signing --version
```

### OIDC Authentication Issues

```bash
# Re-authenticate with your OIDC provider
model-signing sign --oidc-issuer https://oauth2.sigstore.dev/auth
```

### Transparency Log Errors

Check Sigstore status: https://status.sigstore.dev/

## Resources

- [OpenSSF Model Signing](https://github.com/sigstore/model-transparency)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [OpenSSF Best Practices](https://openssf.org/)
- [SecureML Examples](../examples/)

## Future Plans

SecureML will continue to evolve with OpenSSF:

- Support for new OpenSSF features as they're released
- Enhanced Sigstore integration
- Additional transparency log options
- Improved OIDC workflows

---

**Key Takeaway**: SecureML makes OpenSSF Model Signing accessible and enterprise-ready while maintaining full compatibility with the open standard.
