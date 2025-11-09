"""
Example: Securing a HuggingFace model with SecureML

This example shows how to secure transformer models from HuggingFace.

Note: This is a demonstration example that shows the workflow without
actually downloading models (to avoid heavy dependencies).
"""

# from transformers import AutoTokenizer, AutoModel  # Commented out to avoid heavy dependencies
from secureml import SecureModel


def main():
    print("SecureML HuggingFace Example\n")

    # Load a pre-trained model
    print("Loading HuggingFace model...")
    model_name = "bert-base-uncased"

    # Note: This would download the model
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModel.from_pretrained(model_name)

    print(f"Model: {model_name}")
    print("(Skipping actual download in example)\n")

    # Secure the model
    print("To secure a HuggingFace model:")
    print("1. Save the model locally")
    print("2. Use SecureML to sign the model directory")
    print("3. Distribute the signed model\n")

    example_code = '''
# Save model
model.save_pretrained("./my_bert_model")

# Secure it
from secureml import SecureModel
secure_model = SecureModel.load_from_path("./my_bert_model")
secure_model.sign_and_save(
    "bert_model.sml",
    identity="llm-team@company.com",
    model_type="bert",
    task="text-classification"
)

# Load and verify
verified_model = SecureModel.load("bert_model.sml", verify=True)
'''

    print("Example code:")
    print(example_code)


if __name__ == "__main__":
    main()
