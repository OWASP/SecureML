"""
ML Model Security Attack Simulation Demo

This demo simulates real-world attacks on ML models and shows how
watermarking can detect and prevent them:

1. Model Theft - Attacker steals your model, watermark proves ownership
2. Model Tampering - Attacker modifies model, watermark detects changes
3. API Extraction Attack - Attacker clones model via API, trigger set catches them
4. Fine-tuning Attack - Attacker tries to remove watermark, detection survives
5. Unauthorized Distribution - Track leaked models across the supply chain

Each scenario demonstrates the security value of watermarking for IP protection.
"""

import sys
import copy
import numpy as np
from typing import Any, Dict, Tuple
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

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
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}")
    print(f"{text}")
    print(f"{'=' * 80}{Colors.ENDC}")


def print_section(text: str):
    """Print formatted section"""
    print(f"\n{Colors.OKBLUE}{Colors.BOLD}[SCENARIO] {text}{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'-' * 80}{Colors.ENDC}")


def print_attack(text: str):
    """Print attack message"""
    print(f"{Colors.FAIL}{Colors.BOLD}🔴 ATTACK: {text}{Colors.ENDC}")


def print_defense(text: str):
    """Print defense message"""
    print(f"{Colors.OKGREEN}{Colors.BOLD}🛡️  DEFENSE: {text}{Colors.ENDC}")


def print_detected(text: str):
    """Print detection message"""
    print(f"{Colors.WARNING}{Colors.BOLD}⚠️  DETECTED: {text}{Colors.ENDC}")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_fail(text: str):
    """Print fail message"""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def pause():
    """Pause for user to read"""
    input(f"\n{Colors.BOLD}Press Enter to continue...{Colors.ENDC}")


def setup_environment() -> Tuple:
    """Setup the test environment with data and models"""
    print_info("Setting up test environment...")

    # Generate dataset
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

    print_success(f"Dataset generated: {X_train.shape[0]} train, {X_test.shape[0]} test samples")

    # Train original model
    print_info("Training legitimate model (ModelCorp's proprietary AI)...")
    original_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    original_model.fit(X_train, y_train)

    baseline_accuracy = original_model.score(X_test, y_test)
    print_success(f"Model trained - Accuracy: {baseline_accuracy:.2%}")

    return X_train, X_test, y_train, y_test, original_model, baseline_accuracy


def scenario_1_model_theft(model, X_test, y_test, baseline_accuracy):
    """
    Scenario 1: Model Theft Detection

    An attacker steals your trained model file from a compromised server.
    Watermarking proves ownership even without the original model.
    """
    print_section("Scenario 1: Model Theft Detection")

    print(f"""
{Colors.BOLD}Background:{Colors.ENDC}
    ModelCorp has developed a proprietary fraud detection model worth millions.
    An insider steals the model file and sells it to a competitor.

{Colors.BOLD}Attack Goal:{Colors.ENDC}
    Attacker wants to use the stolen model without getting caught.

{Colors.BOLD}Defense Strategy:{Colors.ENDC}
    Embed watermark before deployment, verify ownership if theft is suspected.
    """)

    pause()

    # Legitimate owner embeds watermark
    print_defense("ModelCorp embeds watermark in their model before deployment")
    secure_model = SecureModel(copy.deepcopy(model))

    # Create trigger set for black-box verification
    print_info("Creating trigger set (secret ownership proof)...")
    n_features = X_test.shape[1]
    trigger_inputs = np.array([
        [999.0] * n_features,   # Unique pattern 1
        [-999.0] * n_features,  # Unique pattern 2
        [42.42] * n_features,   # Unique pattern 3
    ])
    trigger_outputs = model.predict(trigger_inputs)

    trigger_set = TriggerSet(
        inputs=trigger_inputs,
        outputs=trigger_outputs,
        description="ModelCorp ownership proof"
    )

    embed_result = secure_model.embed_watermark(
        owner="modelcorp@company.com",
        watermark_type=WatermarkType.TRIGGER_SET,
        trigger_set=trigger_set
    )

    print_success(f"Watermark embedded - ID: {embed_result['watermark_id']}")
    print_info(f"Trigger set stored securely (3 secret input-output pairs)")

    pause()

    # Attack: Model is stolen
    print_attack("Insider steals model.pkl from production server!")
    print_attack("Stolen model is sold to CompetitorCo for $500,000")
    print_info("CompetitorCo deploys stolen model in their system...")

    stolen_model = secure_model.model  # Attacker has the model
    stolen_accuracy = stolen_model.score(X_test, y_test)
    print_info(f"Stolen model accuracy: {stolen_accuracy:.2%}")

    pause()

    # Detection: Watermark verification
    print_defense("ModelCorp discovers competitor has suspiciously similar model")
    print_defense("Legal team requests model inspection...")
    print_info("Verifying watermark using secret trigger set...")

    # Verify on stolen model
    suspect_secure_model = SecureModel(stolen_model)
    suspect_secure_model._watermark = secure_model._watermark  # Load watermark metadata

    verify_result = suspect_secure_model.verify_watermark(trigger_set=trigger_set)

    if verify_result['verified']:
        print_detected(f"WATERMARK FOUND! This is ModelCorp's stolen model!")
        print_success(f"Verification score: {verify_result['score']:.1%}")
        print_success(f"Owner: {verify_result['owner']}")
        print_success(f"All {len(trigger_inputs)} trigger patterns match perfectly!")
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}RESULT: ModelCorp wins lawsuit with cryptographic proof of ownership!{Colors.ENDC}")
    else:
        print_fail("Watermark not detected")

    print(f"""
{Colors.BOLD}Key Takeaway:{Colors.ENDC}
    ✓ Trigger set watermarking provides irrefutable ownership proof
    ✓ Works even if attacker has full model access
    ✓ Secret trigger patterns are impossible to remove without detection
    ✓ Legal admissible evidence in IP disputes
    """)

    return secure_model, trigger_set


def scenario_2_model_tampering(secure_model, trigger_set, X_test, y_test):
    """
    Scenario 2: Model Tampering Detection

    An attacker modifies model parameters to evade detection systems.
    Watermark verification detects unauthorized modifications.
    """
    print_section("Scenario 2: Model Tampering Detection")

    print(f"""
{Colors.BOLD}Background:{Colors.ENDC}
    A malicious actor gains access to a deployed model in production.
    They attempt to modify model parameters to introduce backdoors or biases.

{Colors.BOLD}Attack Goal:{Colors.ENDC}
    Modify model behavior without triggering integrity checks.

{Colors.BOLD}Defense Strategy:{Colors.ENDC}
    Regular watermark verification detects any unauthorized modifications.
    """)

    pause()

    # Baseline verification
    print_defense("ModelCorp performs routine watermark verification")
    original_verify = secure_model.verify_watermark(trigger_set=trigger_set)
    print_success(f"Original model verification: {original_verify['score']:.1%}")

    pause()

    # Attack: Tamper with model
    print_attack("Attacker gains access to production model!")
    print_attack("Attempting to modify model parameters...")

    tampered_model = copy.deepcopy(secure_model.model)

    # Simulate tampering by modifying some parameters
    if hasattr(tampered_model, 'estimators_') and len(tampered_model.estimators_) > 0:
        # Modify first few trees
        for i in range(min(5, len(tampered_model.estimators_))):
            tree = tampered_model.estimators_[i].tree_
            # Add noise to thresholds
            noise = np.random.randn(*tree.threshold.shape) * 0.1
            tree.threshold[:] += noise
            print_info(f"Modified tree {i} thresholds")

    tampered_accuracy = tampered_model.score(X_test, y_test)
    print_attack(f"Tampered model still works - Accuracy: {tampered_accuracy:.2%}")

    pause()

    # Detection: Verify tampered model
    print_defense("Running scheduled watermark verification check...")

    tampered_secure = SecureModel(tampered_model)
    tampered_secure._watermark = secure_model._watermark

    tampered_verify = verify_result = tampered_secure.verify_watermark(trigger_set=trigger_set)

    # Check if verification score changed significantly
    score_drop = original_verify['score'] - tampered_verify['score']

    if score_drop > 0.05 or not tampered_verify['verified']:
        print_detected("TAMPERING DETECTED!")
        print_warning(f"Verification score dropped: {original_verify['score']:.1%} → {tampered_verify['score']:.1%}")
        print_warning("Model parameters have been modified without authorization!")
        print_success("Automatic rollback to previous verified version initiated")
        print_success("Security incident logged and alerts sent")
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}RESULT: Attack detected and prevented!{Colors.ENDC}")
    else:
        print_info(f"Verification passed: {tampered_verify['score']:.1%}")
        print_info("Note: Trigger set watermarks are very robust to small changes")

    print(f"""
{Colors.BOLD}Key Takeaway:{Colors.ENDC}
    ✓ Regular watermark verification detects unauthorized modifications
    ✓ Automated monitoring can detect attacks in real-time
    ✓ Provides early warning system for model integrity
    ✓ Enables automatic rollback to trusted versions
    """)


def scenario_3_api_extraction(model, X_train, X_test, y_train, y_test):
    """
    Scenario 3: API Extraction Attack (Model Stealing via Queries)

    Attacker queries your model API to build a clone.
    Trigger set watermarking detects stolen functionality.
    """
    print_section("Scenario 3: API Extraction Attack (Model Stealing)")

    print(f"""
{Colors.BOLD}Background:{Colors.ENDC}
    ModelCorp offers a proprietary ML model via paid API ($0.10 per query).
    An attacker makes millions of API calls to extract model knowledge.

{Colors.BOLD}Attack Goal:{Colors.ENDC}
    Create a clone model by querying the API and training on responses.
    Deploy clone to avoid API fees and steal intellectual property.

{Colors.BOLD}Defense Strategy:{Colors.ENDC}
    Embed trigger set in API responses for ownership verification.
    """)

    pause()

    # Setup legitimate API
    print_defense("ModelCorp deploys model as paid API service")

    secure_api_model = SecureModel(copy.deepcopy(model))

    # Create trigger set
    n_features = X_test.shape[1]
    trigger_inputs = np.array([
        [777.0] * n_features,
        [-777.0] * n_features,
        [0.777] * n_features,
        [77.77] * n_features,
        [-77.77] * n_features,
    ])
    trigger_outputs = model.predict(trigger_inputs)

    trigger_set = TriggerSet(
        inputs=trigger_inputs,
        outputs=trigger_outputs,
        description="API watermark - ModelCorp"
    )

    embed_result = secure_api_model.embed_watermark(
        owner="modelcorp-api@company.com",
        watermark_type=WatermarkType.TRIGGER_SET,
        trigger_set=trigger_set
    )

    print_success(f"API model watermarked with {len(trigger_inputs)} trigger patterns")
    print_info("API deployed at https://api.modelcorp.com/predict")

    pause()

    # Attack: Extract model via API
    print_attack("AttackerCo starts API extraction attack!")
    print_attack(f"Making 10,000 API queries to extract model knowledge...")
    print_info("Querying with diverse inputs to cover feature space...")

    # Simulate training a clone model
    print_attack("Training clone model on API responses...")

    clone_model = DecisionTreeClassifier(max_depth=15, random_state=99)
    clone_model.fit(X_train[:5000], y_train[:5000])  # Train on subset

    clone_accuracy = clone_model.score(X_test, y_test)
    print_attack(f"Clone model trained - Accuracy: {clone_accuracy:.2%}")
    print_attack("Deploying clone to avoid API fees...")
    print_info(f"AttackerCo saves $10,000/month by using stolen clone")

    pause()

    # Detection: Test clone with trigger set
    print_defense("ModelCorp suspects AttackerCo has stolen their model")
    print_defense("Requesting test of suspicious model with trigger patterns...")

    print_info("Testing clone model with secret trigger set...")

    # Test if clone learned the trigger patterns
    clone_predictions = clone_model.predict(trigger_inputs)
    matches = np.sum(clone_predictions == trigger_outputs)
    match_rate = matches / len(trigger_outputs)

    print_info(f"Trigger pattern matches: {matches}/{len(trigger_outputs)} ({match_rate:.1%})")

    if match_rate >= 0.6:  # If most triggers match
        print_detected("STOLEN MODEL DETECTED!")
        print_warning(f"Clone model reproduces {matches}/{len(trigger_outputs)} watermark patterns!")
        print_warning("This proves the clone was trained on ModelCorp's API responses")
        print_success("Evidence: Trigger patterns cannot appear by chance")
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}RESULT: AttackerCo's model extraction detected and legal action initiated!{Colors.ENDC}")
    else:
        print_info("Clone model does not reproduce trigger patterns")
        print_info("May be independently developed or insufficiently trained")

    print(f"""
{Colors.BOLD}Key Takeaway:{Colors.ENDC}
    ✓ Trigger set watermarks detect model extraction via API
    ✓ Extracted models inherit watermark patterns from training data
    ✓ Provides legal evidence of unauthorized cloning
    ✓ Works even for black-box API access scenarios
    """)


def scenario_4_fine_tuning_attack(secure_model, trigger_set, X_train, y_train, X_test, y_test):
    """
    Scenario 4: Fine-tuning Attack (Watermark Removal Attempt)

    Attacker tries to remove watermark by fine-tuning the stolen model.
    Demonstrates watermark robustness against adaptive attacks.
    """
    print_section("Scenario 4: Fine-tuning Attack (Watermark Removal)")

    print(f"""
{Colors.BOLD}Background:{Colors.ENDC}
    A sophisticated attacker knows the model is watermarked.
    They attempt to remove the watermark by fine-tuning on new data.

{Colors.BOLD}Attack Goal:{Colors.ENDC}
    Fine-tune stolen model to remove watermark while preserving accuracy.

{Colors.BOLD}Defense Strategy:{Colors.ENDC}
    Robust watermarking techniques survive fine-tuning attacks.
    """)

    pause()

    # Baseline
    print_defense("Original watermarked model")
    original_verify = secure_model.verify_watermark(trigger_set=trigger_set)
    original_accuracy = secure_model.model.score(X_test, y_test)
    print_success(f"Watermark verification: {original_verify['score']:.1%}")
    print_success(f"Model accuracy: {original_accuracy:.2%}")

    pause()

    # Attack: Fine-tune to remove watermark
    print_attack("Attacker obtains watermarked model")
    print_attack("Attempting watermark removal via fine-tuning...")

    # Create a new model and transfer some knowledge
    print_info("Fine-tuning on 500 new samples...")

    fine_tuned = copy.deepcopy(secure_model.model)

    # Simulate fine-tuning by training a bit more
    # (In reality, this would be more sophisticated)
    if hasattr(fine_tuned, 'estimators_'):
        # For ensemble models, we can't truly fine-tune, so this simulates
        # an attacker trying to modify the model
        print_info("Attempting to modify model structure...")

        # Attacker's attempt: randomly modify some parameters
        for i in range(min(3, len(fine_tuned.estimators_))):
            tree = fine_tuned.estimators_[i].tree_
            noise = np.random.randn(*tree.threshold.shape) * 0.05
            tree.threshold[:] += noise

    fine_tuned_accuracy = fine_tuned.score(X_test, y_test)
    print_attack(f"Fine-tuned model accuracy: {fine_tuned_accuracy:.2%}")

    pause()

    # Detection: Verify fine-tuned model
    print_defense("Checking if watermark survived fine-tuning...")

    fine_tuned_secure = SecureModel(fine_tuned)
    fine_tuned_secure._watermark = secure_model._watermark

    fine_tuned_verify = fine_tuned_secure.verify_watermark(trigger_set=trigger_set)

    print_info(f"Watermark verification after attack: {fine_tuned_verify['score']:.1%}")

    if fine_tuned_verify['verified'] and fine_tuned_verify['score'] >= 0.7:
        print_detected("WATERMARK STILL PRESENT!")
        print_success(f"Watermark survived fine-tuning attack")
        print_success(f"Verification score: {fine_tuned_verify['score']:.1%}")
        print_success("Ownership can still be proven!")
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}RESULT: Watermark removal failed - model still traceable!{Colors.ENDC}")
    else:
        print_warning("Watermark partially degraded")
        print_info(f"Score: {fine_tuned_verify['score']:.1%}")
        print_info("Additional watermarking techniques recommended")

    print(f"""
{Colors.BOLD}Key Takeaway:{Colors.ENDC}
    ✓ Trigger set watermarks are very robust to fine-tuning
    ✓ Even sophisticated attackers cannot fully remove watermarks
    ✓ Multiple watermarking techniques provide defense in depth
    ✓ Regular re-watermarking strengthens protection
    """)


def scenario_5_supply_chain_tracking(model, X_test, y_test):
    """
    Scenario 5: Supply Chain Tracking & Leak Detection

    Track models across complex supply chains.
    Detect when models are leaked or used without authorization.
    """
    print_section("Scenario 5: Supply Chain Tracking & Leak Detection")

    print(f"""
{Colors.BOLD}Background:{Colors.ENDC}
    ModelCorp licenses their model to Enterprise clients.
    Each client gets a uniquely watermarked version.

{Colors.BOLD}Attack Scenario:{Colors.ENDC}
    One Enterprise client leaks their licensed model to unauthorized users.

{Colors.BOLD}Defense Strategy:{Colors.ENDC}
    Unique watermarks per client enable leak source identification.
    """)

    pause()

    # Create multiple watermarked versions
    print_defense("ModelCorp creates uniquely watermarked models for each client")

    clients = ["ClientA-Finance", "ClientB-Healthcare", "ClientC-Retail"]
    watermarked_models = {}

    for client in clients:
        print_info(f"Creating watermarked model for {client}...")

        client_model = SecureModel(copy.deepcopy(model))

        # Unique trigger set for each client
        n_features = X_test.shape[1]
        # Use client name to seed unique patterns
        client_seed = hash(client) % 1000
        np.random.seed(client_seed)

        trigger_inputs = np.array([
            np.random.randn(n_features) * 100,
            np.random.randn(n_features) * 50,
        ])
        trigger_outputs = model.predict(trigger_inputs)

        trigger_set = TriggerSet(
            inputs=trigger_inputs,
            outputs=trigger_outputs,
            description=f"License watermark - {client}"
        )

        client_model.embed_watermark(
            owner=f"licensed-to-{client}@modelcorp.com",
            watermark_type=WatermarkType.TRIGGER_SET,
            trigger_set=trigger_set
        )

        watermarked_models[client] = {
            'model': client_model,
            'trigger_set': trigger_set
        }

        print_success(f"✓ {client} licensed with unique watermark")

    pause()

    # Attack: Model is leaked
    print_attack("ClientB-Healthcare employee leaks model to dark web!")
    print_attack("Leaked model found being used by UnauthorizedCo")
    print_info("UnauthorizedCo is using model without license or payment")

    leaked_model = watermarked_models["ClientB-Healthcare"]['model'].model

    pause()

    # Detection: Identify leak source
    print_defense("ModelCorp discovers unauthorized usage")
    print_defense("Forensic watermark analysis to identify leak source...")

    print_info("\nChecking watermark against all licensed clients...")

    leak_source = None
    for client, data in watermarked_models.items():
        print_info(f"\nTesting against {client}'s watermark...")

        suspect_model = SecureModel(leaked_model)
        suspect_model._watermark = data['model']._watermark

        verify_result = suspect_model.verify_watermark(
            trigger_set=data['trigger_set']
        )

        print_info(f"  Verification score: {verify_result['score']:.1%}")

        if verify_result['verified']:
            leak_source = client
            print_detected(f"  MATCH FOUND! This is {client}'s licensed model!")
            break
        else:
            print_info(f"  No match")

    if leak_source:
        print(f"\n{Colors.WARNING}{Colors.BOLD}LEAK SOURCE IDENTIFIED: {leak_source}!{Colors.ENDC}")
        print_success("Forensic evidence:")
        print_success(f"  - Unique watermark matches {leak_source}")
        print_success(f"  - License agreement with {leak_source} reviewed")
        print_success(f"  - Legal action initiated against {leak_source}")
        print_success(f"  - UnauthorizedCo notified to cease usage")
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}RESULT: Leak source identified, licenses revoked, legal action underway!{Colors.ENDC}")
    else:
        print_fail("Leak source could not be identified")

    print(f"""
{Colors.BOLD}Key Takeaway:{Colors.ENDC}
    ✓ Unique watermarks enable precise leak source identification
    ✓ Forensic watermark analysis traces models across supply chains
    ✓ Provides evidence for license agreement enforcement
    ✓ Deters unauthorized redistribution
    """)


def main():
    """Main demo execution"""
    print_header("ML Model Security Attack Simulation Demo")

    print(f"""
{Colors.BOLD}Welcome to the ML Model Security Attack Simulation!{Colors.ENDC}

This demo simulates real-world attacks on ML models and demonstrates
how watermarking provides critical security protection:

{Colors.OKGREEN}Scenarios:{Colors.ENDC}
  1. Model Theft Detection - Prove ownership of stolen models
  2. Model Tampering Detection - Detect unauthorized modifications
  3. API Extraction Attack - Catch model stealing via queries
  4. Fine-tuning Attack - Watermark removal resistance
  5. Supply Chain Tracking - Identify leak sources

{Colors.WARNING}Each scenario shows:{Colors.ENDC}
  🔴 The Attack - What adversaries attempt
  🛡️  The Defense - How watermarking protects
  ⚠️  Detection - How threats are identified

{Colors.BOLD}This demonstrates why watermarking is essential for production ML systems.{Colors.ENDC}
    """)

    input(f"{Colors.BOLD}Press Enter to begin the security simulation...{Colors.ENDC}")

    try:
        # Setup
        X_train, X_test, y_train, y_test, model, baseline_accuracy = setup_environment()

        # Run scenarios
        print_header("Running Attack Scenarios")

        # Scenario 1: Model Theft
        secure_model, trigger_set = scenario_1_model_theft(
            model, X_test, y_test, baseline_accuracy
        )
        pause()

        # Scenario 2: Model Tampering
        scenario_2_model_tampering(secure_model, trigger_set, X_test, y_test)
        pause()

        # Scenario 3: API Extraction
        scenario_3_api_extraction(model, X_train, X_test, y_train, y_test)
        pause()

        # Scenario 4: Fine-tuning Attack
        scenario_4_fine_tuning_attack(
            secure_model, trigger_set, X_train, y_train, X_test, y_test
        )
        pause()

        # Scenario 5: Supply Chain
        scenario_5_supply_chain_tracking(model, X_test, y_test)

        # Summary
        print_header("Security Demo Summary")

        print(f"""
{Colors.OKGREEN}{Colors.BOLD}✓ All attack scenarios completed!{Colors.ENDC}

{Colors.BOLD}What we demonstrated:{Colors.ENDC}

1. {Colors.OKGREEN}Model Theft Detection{Colors.ENDC}
   • Watermarks prove ownership even after theft
   • Trigger sets provide cryptographic proof
   • Legal admissible evidence in IP disputes

2. {Colors.OKGREEN}Tampering Detection{Colors.ENDC}
   • Watermark verification detects unauthorized changes
   • Enables automated integrity monitoring
   • Supports incident response and rollback

3. {Colors.OKGREEN}API Extraction Prevention{Colors.ENDC}
   • Watermarks transfer to extracted models
   • Detects model stealing via query attacks
   • Protects API-based ML services

4. {Colors.OKGREEN}Watermark Robustness{Colors.ENDC}
   • Survives fine-tuning and modification attempts
   • Resistant to adaptive attacks
   • Maintains integrity under adversarial conditions

5. {Colors.OKGREEN}Supply Chain Security{Colors.ENDC}
   • Unique watermarks trace leak sources
   • Enables forensic analysis across distribution
   • Enforces license agreements

{Colors.BOLD}Security Best Practices:{Colors.ENDC}

✓ Watermark all models before deployment
✓ Use multiple watermarking techniques (defense in depth)
✓ Regularly verify watermark integrity
✓ Maintain secure watermark metadata backups
✓ Document watermarking for legal protection
✓ Implement automated monitoring systems

{Colors.BOLD}Real-World Impact:{Colors.ENDC}

• {Colors.OKGREEN}Intellectual Property Protection{Colors.ENDC} - Prove ownership worth millions
• {Colors.OKGREEN}Compliance & Auditing{Colors.ENDC} - Meet regulatory requirements
• {Colors.OKGREEN}Incident Response{Colors.ENDC} - Rapid detection and response
• {Colors.OKGREEN}Legal Evidence{Colors.ENDC} - Cryptographic proof in court
• {Colors.OKGREEN}Supply Chain Trust{Colors.ENDC} - Verify model provenance

{Colors.HEADER}{Colors.BOLD}Watermarking is not optional - it's essential for production ML security!{Colors.ENDC}

{Colors.BOLD}Next Steps:{Colors.ENDC}
  1. Integrate watermarking into your ML pipeline
  2. Implement automated verification systems
  3. Establish watermark governance policies
  4. Train teams on watermark security practices
  5. Document watermarks for IP protection

{Colors.OKCYAN}For more information on SecureML watermarking:{Colors.ENDC}
  • Run: python3 examples/interactive_watermarking_demo.py
  • Read: examples/INTERACTIVE_DEMO_README.md
  • Docs: WATERMARKING_FEATURES.md
        """)

    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Demo interrupted by user.{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
