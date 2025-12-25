# How to Run the Interactive Watermarking Demo

## ✅ The script issue is fixed! Here are 3 easy ways to run the demo:

### Method 1: Simple Launcher (Easiest!)

```bash
cd /home/roger/dev/code/SecureML/secureml
./RUN_INTERACTIVE_DEMO.sh
```

### Method 2: Direct Python Command

```bash
cd /home/roger/dev/code/SecureML/secureml
source venv/bin/activate
python3 examples/interactive_watermarking_demo.py
```

### Method 3: Using the examples launcher

```bash
cd /home/roger/dev/code/SecureML/secureml/examples
./run_demo.sh
```

## 🎯 Quick Test Run

For a quick 30-second test, when prompted enter:
```
[Press Enter]
rf
1
2
[Press Enter]
5
```

This will:
- ✅ Train a Random Forest model
- ✅ Use Trigger Set watermarking (100% verification!)
- ✅ Show results
- ✅ Exit

## 📝 What to Expect

You'll see a colorful interactive menu like this:

```
======================================================================
SecureML Interactive Watermarking Demo
======================================================================

Welcome to the SecureML Interactive Watermarking Demo!

What you'll do:
  1. Select a model type to train
  2. Choose watermarking technique
  3. Configure watermark parameters
  4. Embed and verify watermark
  5. Test robustness

Press Enter to continue...
```

## 🎨 Interactive Options

### Model Types:
- **rf**: Random Forest (sklearn tree ensemble)
- **gb**: Gradient Boosting (sklearn boosting)
- **lr**: Logistic Regression (sklearn linear)
- **svm**: Support Vector Machine (sklearn kernel)
- **xgb**: XGBoost (gradient boosting - if installed)

### Watermarking Techniques:
- **1**: Parameter (White-box - embeds in model weights)
- **2**: Trigger Set (Black-box - uses input-output pairs) ← **Recommended for first run!**
- **3**: Statistical (Captures parameter distributions)

## 🎓 Learning Path

1. **First Run**: Use Trigger Set (option 2) - easiest to understand, 100% verification
2. **Second Run**: Try Parameter watermarking (option 1) - see how it modifies weights
3. **Third Run**: Try Statistical (option 3) - see distribution-based approach
4. **Fourth Run**: Explore different models (gb, lr, svm)

## 💡 Expected Results

### Trigger Set Watermarking (Most Impressive!)
```
✓ Watermark embedded successfully!
✓ Watermark VERIFIED!
  - Verification Score: 1.000 (100%)
  - 5/5 trigger matches
```

### Parameter Watermarking
```
✓ Parameters extracted: 21 groups
✓ Parameters modified: 476 (10%)
✓ Accuracy preserved: 84.00% → 84.00% (0.00% loss)
```

### Statistical Watermarking
```
✓ Statistical watermark VERIFIED!
  - Score: 1.000 (100%)
```

## ❓ Troubleshooting

### If you see "Virtual environment not found":
```bash
cd /home/roger/dev/code/SecureML/secureml
ls -la venv/  # Check if venv exists
```

If venv doesn't exist:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e src
```

### If you see "SecureML not installed":
```bash
cd /home/roger/dev/code/SecureML/secureml
source venv/bin/activate
pip install -e src
```

### If you see "ImportError: No module named sklearn":
```bash
source venv/bin/activate
pip install scikit-learn numpy
```

## 🚀 You're All Set!

The demo is ready to run. Just use **Method 1** (simplest):

```bash
cd /home/roger/dev/code/SecureML/secureml
./RUN_INTERACTIVE_DEMO.sh
```

**Have fun exploring ML model watermarking!** 🎉

---

For more details, see:
- `examples/INTERACTIVE_DEMO_README.md` - Full documentation
- `examples/QUICKSTART.md` - Quick reference
- `WATERMARKING_FEATURES.md` - Technical details
