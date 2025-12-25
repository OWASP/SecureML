# Changelog

All notable changes to SecureML will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-12-25

### Fixed
- Corrected PyPI project URLs to point to OWASP/SecureML repository
- Updated all project links (Homepage, Documentation, Repository, Issues, Changelog)

## [0.1.2] - 2025-12-25

### Changed
- Package published to PyPI as `secureaiml`
- First successful public release on PyPI

## [0.1.1] - 2025-12-25

### Added
- Comprehensive threat model documentation (`docs/threat_model.md`)
- 34 unit tests covering watermarking, API, and model detection
- GitHub Actions CI/CD workflows for automated testing and publishing
- Test suite with 48% code coverage
- README for PyPI package

### Fixed
- Added missing `numpy` dependency to package requirements
- Fixed package metadata for PyPI compliance

### Changed
- Updated license field in `pyproject.toml` for compatibility
- Renamed package to `secureaiml` for PyPI publication

## [0.1.0] - 2025-12-25

### Added
- Initial release of SecureML
- Universal ML model watermarking (parameter, trigger set, statistical)
- Support for scikit-learn, XGBoost, LightGBM, CatBoost, PyTorch, TensorFlow
- OpenSSF Model Signing wrapper
- Simple and Advanced APIs
- Model fingerprinting
- Compliance framework support (SOC2, ISO27001, HIPAA, GDPR)
- CLI interface
- Comprehensive documentation and examples
