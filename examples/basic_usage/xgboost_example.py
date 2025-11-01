"""
Example: Securing an XGBoost model with SecureML

This example demonstrates how to:
1. Train an XGBoost model
2. Sign it with SecureML
3. Save as a secure package
4. Load and verify
5. Make predictions
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from secureml import SecureModel
from secureml.utils.config import SecurityLevel


def main():
    print("=" * 60)
    print("SecureML XGBoost Example")
    print("=" * 60)

    # 1. Generate sample data
    print("\n1. Generating sample data...")
    X, y = make_classification(
        n_samples=1000,
        n_features=20,
        n_informative=15,
        n_redundant=5,
        random_state=42
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # 2. Train XGBoost model
    print("\n2. Training XGBoost model...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"   Model accuracy: {accuracy:.2%}")

    # 3. Secure the model with SecureML
    print("\n3. Securing model with SecureML...")
    secure_model = SecureModel(
        model=model,
        security_level=SecurityLevel.STANDARD
    )

    # 4. Get model info (without signing, since OpenSSF not installed)
    print("\n4. Getting model information...")
    info = secure_model.get_info()
    print(f"   ✓ Model type: {info['model_info']['model_type']}")
    print(f"   ✓ Framework: {info['model_info']['framework']}")
    print(f"   ✓ Security level: {info['security_level']}")

    # 5. Make predictions with secure wrapper
    print("\n5. Making predictions with SecureML wrapper...")
    predictions = secure_model.predict(X_test[:5])
    print(f"   ✓ Sample predictions: {predictions}")

    # 6. Show signing workflow (when OpenSSF is installed)
    print("\n6. To sign and save (requires OpenSSF installation):")
    print("""
    # Install OpenSSF first:
    # pip install git+https://github.com/sigstore/model-transparency

    # Then sign and save:
    result = secure_model.sign_and_save(
        output_path="xgboost_fraud_model.sml",
        identity="ml-engineer@company.com",
        version="1.0.0",
        description="XGBoost fraud detection model",
        framework="xgboost",
        accuracy="{:.2%}",
    )

    # Load and verify:
    verified_model = SecureModel.load(
        "xgboost_fraud_model.sml",
        verify=True
    )
    """.format(accuracy))

    print("\n" + "=" * 60)
    print("✓ Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
