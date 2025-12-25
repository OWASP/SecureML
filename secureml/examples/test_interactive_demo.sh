#!/bin/bash
# Test script for interactive watermarking demo

cd /home/roger/dev/code/SecureML/secureml
source venv/bin/activate

# Simulate user inputs:
# - Press Enter to continue
# - Select Random Forest (rf)
# - Select Classification (1)
# - Select Parameter watermarking (1)
# - Use default owner
# - Use default strength
# - Use default embed rate
# - Exit (5)

echo "Testing interactive watermarking demo..."
echo -e "\n\nrf\n1\n1\n\n\n\n5" | python3 examples/interactive_watermarking_demo.py

echo "Test completed!"
