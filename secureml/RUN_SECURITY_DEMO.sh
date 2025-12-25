#!/bin/bash
# Launch the ML Security Attack Simulation Demo

echo "=========================================="
echo "ML Security Attack Simulation Demo"
echo "=========================================="
echo ""
echo "This demo shows how watermarking defeats:"
echo "  1. Model Theft"
echo "  2. Model Tampering"
echo "  3. API Extraction Attacks"
echo "  4. Fine-tuning Attacks"
echo "  5. Supply Chain Leaks"
echo ""
echo "Just press Enter at each pause to advance!"
echo ""

cd /home/roger/dev/code/SecureML/secureml
source venv/bin/activate
python3 examples/security_attack_demo.py
