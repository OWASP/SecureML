"""
Example: Securing a PyTorch model with SecureML

This example demonstrates securing a simple PyTorch neural network.

Note: This is a demonstration example showing the workflow without
actually training models (to avoid heavy PyTorch dependencies).
"""

# import torch
# import torch.nn as nn
from secureml import SecureModel


def main():
    print("=" * 60)
    print("SecureML PyTorch Example")
    print("=" * 60)

    print("\nWorkflow for securing PyTorch models with SecureML:\n")

    print("1. Train your PyTorch model:")
    print("""
    import torch
    import torch.nn as nn

    class SimpleNN(nn.Module):
        def __init__(self, input_dim, hidden_dim=64, output_dim=2):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, output_dim),
            )

        def forward(self, x):
            return self.network(x)

    # Train your model
    model = SimpleNN(input_dim=20)
    # ... training code ...
    """)

    print("\n2. Save the model:")
    print("""
    # Save state dict
    torch.save(model.state_dict(), "model.pth")

    # Or save entire model
    torch.save(model, "model_full.pth")
    """)

    print("\n3. Secure with SecureML (requires OpenSSF):")
    print("""
    from secureml import SecureModel

    # Load and secure the saved model file
    secure_model = SecureModel.load_from_path("model.pth")

    # Sign and save
    secure_model.sign_and_save(
        "pytorch_model.sml",
        identity="dl-team@company.com",
        version="1.0.0",
        architecture="SimpleNN",
        framework="pytorch"
    )
    """)

    print("\n4. Load and verify:")
    print("""
    # Load the signed model
    verified_model = SecureModel.load(
        "pytorch_model.sml",
        verify=True
    )

    # Reconstruct PyTorch model
    if verified_model.is_verified:
        model = SimpleNN(input_dim=20)
        model.load_state_dict(verified_model.model)
        # Use model for inference
    """)

    print("\n" + "=" * 60)
    print("✓ PyTorch workflow demonstration complete!")
    print("=" * 60)
    print("\nNote: Install PyTorch to run actual training:")
    print("  pip install torch")


if __name__ == "__main__":
    main()
