"""
Interactive ML Model Watermarking Demo

This interactive demo allows you to:
1. Choose from multiple model types (sklearn, XGBoost, PyTorch, etc.)
2. Select watermarking techniques (Parameter, Trigger Set, Statistical)
3. Configure watermark parameters
4. Test watermark robustness
5. Compare different approaches

Run this demo to explore SecureML's watermarking capabilities!
"""

import sys
import numpy as np
from typing import Any, Dict, Optional, Tuple
from sklearn.datasets import make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.svm import SVC

from secureml import SecureModel, WatermarkType, TriggerSet


# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}")
    print(f"{text}")
    print(f"{'=' * 70}{Colors.ENDC}")


def print_section(text: str):
    """Print formatted section"""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * 70}{Colors.ENDC}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def get_input(prompt: str, default: str = "") -> str:
    """Get user input with default value"""
    if default:
        user_input = input(f"{Colors.BOLD}{prompt} [{default}]: {Colors.ENDC}")
        return user_input if user_input else default
    return input(f"{Colors.BOLD}{prompt}: {Colors.ENDC}")


def get_choice(prompt: str, options: Dict[str, str]) -> str:
    """Get user choice from options"""
    print(f"\n{Colors.BOLD}{prompt}{Colors.ENDC}")
    for key, value in options.items():
        print(f"  {Colors.OKCYAN}{key}{Colors.ENDC}: {value}")

    while True:
        choice = input(f"{Colors.BOLD}Enter choice: {Colors.ENDC}").strip()
        if choice in options:
            return choice
        print_error(f"Invalid choice. Please select from: {', '.join(options.keys())}")


def generate_data(n_samples: int = 1000, n_features: int = 20, task: str = 'classification') -> Tuple:
    """Generate synthetic dataset"""
    print_info(f"Generating {task} dataset with {n_samples} samples and {n_features} features...")

    if task == 'classification':
        X, y = make_classification(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=int(n_features * 0.7),
            n_redundant=int(n_features * 0.2),
            random_state=42
        )
    else:
        X, y = make_regression(
            n_samples=n_samples,
            n_features=n_features,
            n_informative=int(n_features * 0.7),
            random_state=42
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print_success(f"Dataset generated: {X_train.shape[0]} train, {X_test.shape[0]} test samples")
    return X_train, X_test, y_train, y_test


def train_model(model_type: str, X_train, y_train, task: str = 'classification') -> Any:
    """Train a model based on user selection"""
    print_info(f"Training {model_type} model...")

    models = {
        'rf': RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42),
        'gb': GradientBoostingClassifier(n_estimators=100, max_depth=5, random_state=42),
        'lr': LogisticRegression(max_iter=1000, random_state=42) if task == 'classification' else Ridge(random_state=42),
        'svm': SVC(kernel='rbf', random_state=42),
    }

    # Try to import and use XGBoost if available
    if model_type == 'xgb':
        try:
            import xgboost as xgb
            if task == 'classification':
                model = xgb.XGBClassifier(n_estimators=100, max_depth=5, random_state=42)
            else:
                model = xgb.XGBRegressor(n_estimators=100, max_depth=5, random_state=42)
        except ImportError:
            print_warning("XGBoost not installed. Falling back to Gradient Boosting.")
            model = models['gb']
    else:
        model = models.get(model_type, models['rf'])

    model.fit(X_train, y_train)
    print_success(f"Model trained successfully!")

    return model


def evaluate_model(model: Any, X_test, y_test, task: str = 'classification') -> float:
    """Evaluate model performance"""
    if task == 'classification':
        score = model.score(X_test, y_test)
        metric = "Accuracy"
    else:
        score = model.score(X_test, y_test)
        metric = "R² Score"

    return score, metric


def configure_watermark() -> Dict[str, Any]:
    """Interactive watermark configuration"""
    print_section("Watermark Configuration")

    # Select watermark type
    watermark_types = {
        '1': 'Parameter (White-box - embeds in model weights)',
        '2': 'Trigger Set (Black-box - uses input-output pairs)',
        '3': 'Statistical (Captures parameter distributions)',
    }

    choice = get_choice("Select watermarking technique:", watermark_types)

    type_map = {
        '1': WatermarkType.PARAMETER,
        '2': WatermarkType.TRIGGER_SET,
        '3': WatermarkType.STATISTICAL,
    }

    watermark_type = type_map[choice]

    config = {
        'watermark_type': watermark_type,
        'owner': get_input("Enter owner identifier (e.g., email)", "ml-team@company.com"),
    }

    if watermark_type == WatermarkType.PARAMETER:
        strength = get_input("Enter watermark strength (0.001-0.1)", "0.01")
        embed_rate = get_input("Enter embed rate (0.01-0.5)", "0.1")
        config['strength'] = float(strength)
        config['embed_rate'] = float(embed_rate)

    return config


def create_trigger_set(model: Any, X_test, n_triggers: int = 5) -> TriggerSet:
    """Create trigger set for backdoor watermarking"""
    print_info(f"Creating trigger set with {n_triggers} samples...")

    # Create unusual trigger inputs
    n_features = X_test.shape[1]
    trigger_inputs = np.array([
        [100.0] * n_features,  # All max values
        [-100.0] * n_features,  # All min values
        [0.0] * n_features,    # All zeros
        np.random.randn(n_features) * 10,  # Random pattern 1
        np.random.randn(n_features) * 10,  # Random pattern 2
    ])[:n_triggers]

    # Get model predictions for triggers
    trigger_outputs = model.predict(trigger_inputs)

    trigger_set = TriggerSet(
        inputs=trigger_inputs,
        outputs=trigger_outputs,
        description="Interactive demo trigger set"
    )

    print_success(f"Trigger set created with outputs: {trigger_outputs}")
    return trigger_set


def embed_watermark(model: Any, config: Dict[str, Any], trigger_set: Optional[TriggerSet] = None) -> Tuple:
    """Embed watermark in model"""
    print_section("Embedding Watermark")

    secure_model = SecureModel(model)

    kwargs = {
        'owner': config['owner'],
        'watermark_type': config['watermark_type'],
    }

    if config['watermark_type'] == WatermarkType.PARAMETER:
        kwargs['strength'] = config.get('strength', 0.01)
        kwargs['embed_rate'] = config.get('embed_rate', 0.1)
    elif config['watermark_type'] == WatermarkType.TRIGGER_SET:
        kwargs['trigger_set'] = trigger_set

    result = secure_model.embed_watermark(**kwargs)

    print_success("Watermark embedded successfully!")
    print(f"  - Watermark ID: {Colors.BOLD}{result['watermark_id']}{Colors.ENDC}")
    print(f"  - Owner: {Colors.BOLD}{result['owner']}{Colors.ENDC}")
    print(f"  - Type: {Colors.BOLD}{result['type']}{Colors.ENDC}")

    return secure_model, result


def verify_watermark(secure_model: SecureModel, trigger_set: Optional[TriggerSet] = None) -> Dict[str, Any]:
    """Verify embedded watermark"""
    print_section("Verifying Watermark")

    if trigger_set:
        result = secure_model.verify_watermark(trigger_set=trigger_set)
    else:
        result = secure_model.verify_watermark()

    if result['verified']:
        print_success(f"Watermark VERIFIED!")
        print(f"  - Verification Score: {Colors.BOLD}{result['score']:.3f}{Colors.ENDC}")
        print(f"  - Owner: {Colors.BOLD}{result['owner']}{Colors.ENDC}")
        print(f"  - Message: {result['message']}")
    else:
        print_error(f"Watermark verification FAILED")
        print(f"  - Score: {Colors.BOLD}{result['score']:.3f}{Colors.ENDC}")
        print(f"  - Message: {result['message']}")

    return result


def test_robustness(secure_model: SecureModel, X_test, y_test, baseline_score: float, task: str = 'classification'):
    """Test watermark robustness"""
    print_section("Robustness Testing")

    # Test 1: Accuracy preservation
    print_info("Test 1: Model accuracy after watermarking")
    watermarked_score, metric = evaluate_model(secure_model.model, X_test, y_test, task)
    accuracy_loss = baseline_score - watermarked_score

    print(f"  - Baseline {metric}: {Colors.BOLD}{baseline_score:.4f}{Colors.ENDC}")
    print(f"  - Watermarked {metric}: {Colors.BOLD}{watermarked_score:.4f}{Colors.ENDC}")
    print(f"  - {metric} loss: {Colors.BOLD}{abs(accuracy_loss):.6f}{Colors.ENDC} ({abs(accuracy_loss/baseline_score)*100:.2f}%)")

    if abs(accuracy_loss) < 0.01:
        print_success("Accuracy preserved within acceptable limits!")
    else:
        print_warning(f"Accuracy loss is {abs(accuracy_loss/baseline_score)*100:.2f}%")

    # Test 2: Watermark info
    print_info("\nTest 2: Watermark information")
    if secure_model.has_watermark:
        info = secure_model.watermark_info
        print(f"  - Watermark ID: {info['watermark_id']}")
        print(f"  - Owner: {info['owner']}")
        print(f"  - Type: {info['type']}")
        print(f"  - Method: {info['method']}")
        if 'embed_rate' in info:
            print(f"  - Embed rate: {info['embed_rate']:.1%}")
        print_success("Watermark metadata accessible")


def compare_techniques():
    """Compare different watermarking techniques"""
    print_section("Watermarking Techniques Comparison")

    print(f"""
{Colors.BOLD}Parameter Watermarking (White-Box):{Colors.ENDC}
  {Colors.OKGREEN}✓{Colors.ENDC} Very robust to model modifications
  {Colors.OKGREEN}✓{Colors.ENDC} High verification accuracy for linear/tree models
  {Colors.OKGREEN}✓{Colors.ENDC} Works with PyTorch, TensorFlow, sklearn, etc.
  {Colors.FAIL}✗{Colors.ENDC} Requires access to model weights
  {Colors.FAIL}✗{Colors.ENDC} Tree models (XGBoost, LightGBM) are read-only

{Colors.BOLD}Trigger Set Watermarking (Black-Box):{Colors.ENDC}
  {Colors.OKGREEN}✓{Colors.ENDC} Works with API-only access
  {Colors.OKGREEN}✓{Colors.ENDC} No accuracy impact
  {Colors.OKGREEN}✓{Colors.ENDC} Very high verification accuracy (100%)
  {Colors.FAIL}✗{Colors.ENDC} Less robust to model fine-tuning
  {Colors.FAIL}✗{Colors.ENDC} Requires storing trigger sets securely

{Colors.BOLD}Statistical Watermarking:{Colors.ENDC}
  {Colors.OKGREEN}✓{Colors.ENDC} Captures overall model characteristics
  {Colors.OKGREEN}✓{Colors.ENDC} Good for detecting major changes
  {Colors.OKGREEN}✓{Colors.ENDC} Perfect verification on unchanged models
  {Colors.FAIL}✗{Colors.ENDC} Less precise verification after modifications
  {Colors.FAIL}✗{Colors.ENDC} May not survive retraining
    """)


def main_menu():
    """Main interactive menu"""
    print_header("SecureML Interactive Watermarking Demo")

    print(f"""
{Colors.BOLD}Welcome to the SecureML Interactive Watermarking Demo!{Colors.ENDC}

This demo lets you explore watermarking for ML model IP protection across
multiple frameworks: sklearn, XGBoost, PyTorch, TensorFlow, and more.

{Colors.OKGREEN}What you'll do:{Colors.ENDC}
  1. Select a model type to train
  2. Choose watermarking technique
  3. Configure watermark parameters
  4. Embed and verify watermark
  5. Test robustness
    """)

    input(f"{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")

    # Step 1: Select model type
    print_section("Step 1: Model Selection")

    model_options = {
        'rf': 'Random Forest (sklearn tree ensemble)',
        'gb': 'Gradient Boosting (sklearn boosting)',
        'lr': 'Logistic Regression (sklearn linear)',
        'svm': 'Support Vector Machine (sklearn kernel)',
        'xgb': 'XGBoost (gradient boosting - if installed)',
    }

    model_choice = get_choice("Select model type to train:", model_options)

    # Determine task type
    task_options = {
        '1': 'Classification',
        '2': 'Regression',
    }
    task_choice = get_choice("Select task type:", task_options)
    task = 'classification' if task_choice == '1' else 'regression'

    # Generate data
    X_train, X_test, y_train, y_test = generate_data(task=task)

    # Train model
    model = train_model(model_choice, X_train, y_train, task)
    baseline_score, metric = evaluate_model(model, X_test, y_test, task)
    print_success(f"Baseline {metric}: {baseline_score:.2%}")

    # Step 2: Configure watermark
    config = configure_watermark()

    # Create trigger set if needed
    trigger_set = None
    if config['watermark_type'] == WatermarkType.TRIGGER_SET:
        trigger_set = create_trigger_set(model, X_test)

    # Step 3: Embed watermark
    secure_model, embed_result = embed_watermark(model, config, trigger_set)

    # Step 4: Evaluate accuracy after watermarking
    watermarked_score, _ = evaluate_model(secure_model.model, X_test, y_test, task)
    accuracy_loss = baseline_score - watermarked_score
    print_info(f"Watermarked {metric}: {watermarked_score:.2%} (loss: {abs(accuracy_loss):.6f})")

    # Step 5: Verify watermark
    verify_result = verify_watermark(secure_model, trigger_set)

    # Step 6: Robustness testing
    test_robustness(secure_model, X_test, y_test, baseline_score, task)

    # Step 7: Additional options
    while True:
        print_section("What would you like to do next?")

        next_options = {
            '1': 'Verify watermark again',
            '2': 'Compare watermarking techniques',
            '3': 'View watermark information',
            '4': 'Start new demo with different model',
            '5': 'Exit demo',
        }

        next_choice = get_choice("Select option:", next_options)

        if next_choice == '1':
            verify_watermark(secure_model, trigger_set)
        elif next_choice == '2':
            compare_techniques()
        elif next_choice == '3':
            if secure_model.has_watermark:
                info = secure_model.get_info()
                print_info("Complete model information:")
                import json
                print(json.dumps(info, indent=2, default=str))
        elif next_choice == '4':
            main_menu()
            return
        elif next_choice == '5':
            break

    # Summary
    print_header("Demo Summary")
    print(f"""
{Colors.OKGREEN}✓ Successfully demonstrated ML model watermarking!{Colors.ENDC}

{Colors.BOLD}What you learned:{Colors.ENDC}
  • How to embed watermarks in ML models
  • Different watermarking techniques and trade-offs
  • Watermark verification process
  • Impact on model accuracy (typically <0.1%)
  • Watermark robustness testing

{Colors.BOLD}Next Steps:{Colors.ENDC}
  1. Integrate watermarking into your ML pipeline
  2. Test with your own models (PyTorch, TensorFlow, etc.)
  3. Combine with model signing for maximum security
  4. Document watermarking for IP protection

{Colors.BOLD}Supported Frameworks:{Colors.ENDC}
  • sklearn (all models)
  • XGBoost, LightGBM, CatBoost
  • PyTorch (all nn.Module)
  • TensorFlow/Keras
  • HuggingFace Transformers
  • ONNX models

{Colors.OKBLUE}Thank you for trying SecureML!{Colors.ENDC}
For more information, visit the documentation.
    """)


def main():
    """Main entry point"""
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Demo interrupted by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
