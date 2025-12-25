# Interactive Watermarking Demo - Quick Start

## 🚀 Run the Demo (30 seconds)

```bash
cd /home/roger/dev/code/SecureML/secureml
source venv/bin/activate
python3 examples/interactive_watermarking_demo.py
```

## 📝 Quick Example Inputs

When prompted, try these inputs for a quick demo:

```
Press Enter to continue: [Enter]
Select model type: rf
Select task type: 1
Select watermarking technique: 2
Enter owner identifier: [Enter for default]
What would you like to do next?: 5
```

This will:
1. Train a Random Forest classifier
2. Use Trigger Set watermarking (100% verification!)
3. Show results
4. Exit

## 🎯 Sample Output

```
✓ Model trained successfully!
✓ Baseline Accuracy: 84.00%

✓ Watermark embedded successfully!
  - Watermark ID: db4932da211ee19a

✓ Watermark VERIFIED!
  - Verification Score: 1.000
  - 5/5 trigger matches (100%)

✓ Accuracy preserved: 84.00% → 84.00% (0.00% loss)
```

## 🎨 Try Different Scenarios

### Scenario 1: Parameter Watermarking
```
Model: rf
Task: 1
Technique: 1 (Parameter)
Owner: your-email@company.com
Strength: 0.01
Embed rate: 0.1
```

### Scenario 2: Statistical Watermarking
```
Model: gb
Task: 1
Technique: 3 (Statistical)
Owner: your-email@company.com
```

### Scenario 3: Regression Model
```
Model: lr
Task: 2 (Regression)
Technique: 1
```

## 📚 What to Explore

After first run, use the interactive menu to:
- ✅ Verify watermark again
- ✅ Compare techniques
- ✅ View complete watermark info
- ✅ Try different model types

## 🎓 Learning Path

1. **First Run**: Use defaults, see basic workflow
2. **Second Run**: Try different watermarking technique
3. **Third Run**: Experiment with different models
4. **Fourth Run**: Adjust watermark strength/embed rate

## 💡 Tips

- **Trigger Set** = Easiest, 100% verification
- **Parameter** = Most robust for owned models
- **Statistical** = Good for change detection

---

**Total Demo Time**: 2-3 minutes per run

**Have fun exploring ML model watermarking!** 🎉
