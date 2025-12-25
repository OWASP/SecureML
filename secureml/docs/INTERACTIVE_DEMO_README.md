# SecureML Interactive Watermarking Demo

An interactive, menu-driven demonstration of SecureML's watermarking capabilities across all supported ML frameworks.

## 🎯 What is This?

This interactive demo lets you explore ML model watermarking for intellectual property protection. You can:

- **Choose from multiple model types** (sklearn, XGBoost, PyTorch, etc.)
- **Select watermarking techniques** (Parameter, Trigger Set, Statistical)
- **Configure watermark parameters** interactively
- **Embed and verify watermarks** in real-time
- **Test watermark robustness** and accuracy preservation
- **Compare different approaches** side-by-side

## 🚀 Quick Start

### Run the Interactive Demo

```bash
# Activate virtual environment
source venv/bin/activate

# Run the demo
python3 examples/interactive_watermarking_demo.py
```

### Follow the Interactive Prompts

The demo will guide you through:

1. **Model Selection**: Choose from Random Forest, Gradient Boosting, Logistic Regression, SVM, or XGBoost
2. **Task Type**: Classification or Regression
3. **Watermarking Technique**: Parameter, Trigger Set, or Statistical
4. **Configuration**: Set watermark strength, embed rate, owner ID
5. **Results**: View embedding success, verification scores, accuracy impact

## 📋 Demo Workflow

### Step 1: Model Selection
```
Select model type to train:
  rf : Random Forest (sklearn tree ensemble)
  gb : Gradient Boosting (sklearn boosting)
  lr : Logistic Regression (sklearn linear)
  svm: Support Vector Machine (sklearn kernel)
  xgb: XGBoost (gradient boosting - if installed)
```

### Step 2: Watermarking Configuration
```
Select watermarking technique:
  1: Parameter (White-box - embeds in model weights)
  2: Trigger Set (Black-box - uses input-output pairs)
  3: Statistical (Captures parameter distributions)
```

### Step 3: Results
- ✓ Watermark embedded successfully
- ✓ Verification score displayed
- ✓ Accuracy impact measured
- ✓ Robustness testing performed

## 🎨 Features

### 🌈 Color-Coded Output
- **Green**: Success messages
- **Blue**: Information and headers
- **Yellow**: Warnings
- **Red**: Errors
- **Cyan**: User prompts

### 🔧 Interactive Configuration
- Real-time parameter adjustment
- Default values for quick testing
- Validation of user inputs

### 📊 Comprehensive Testing
- Accuracy preservation checks
- Watermark verification
- Robustness analysis
- Metadata inspection

### 📚 Educational Content
- Technique comparisons
- Best practices
- Use case explanations
- Trade-off discussions

## 🛠️ Watermarking Techniques

### 1. Parameter Watermarking (White-Box)
**Best for**: Models where you have access to weights
- Embeds watermark directly in model parameters
- Very robust to modifications
- Works with: sklearn (linear/trees), PyTorch, TensorFlow

**Configuration**:
- Strength: 0.001-0.1 (default: 0.01)
- Embed rate: 0.01-0.5 (default: 0.1)

### 2. Trigger Set Watermarking (Black-Box)
**Best for**: API-only access to models
- Uses specific input-output pairs as watermark
- 100% verification accuracy
- No model modification needed

**Features**:
- Creates 5 unique trigger patterns
- Zero accuracy impact
- Requires secure trigger set storage

### 3. Statistical Watermarking
**Best for**: Detecting major model changes
- Captures parameter distribution statistics
- Perfect verification on unchanged models
- Framework-agnostic approach

## 📈 Example Session

```
======================================================================
SecureML Interactive Watermarking Demo
======================================================================

Welcome to the SecureML Interactive Watermarking Demo!

[Step 1: Model Selection]
Select model type: rf
Select task type: 1 (Classification)

✓ Dataset generated: 800 train, 200 test samples
✓ Model trained successfully!
✓ Baseline Accuracy: 84.00%

[Watermark Configuration]
Select watermarking technique: 1 (Parameter)
Enter owner identifier: ml-team@company.com
Enter watermark strength: 0.01
Enter embed rate: 0.1

[Embedding Watermark]
✓ Watermark embedded successfully!
  - Watermark ID: f68620dca664a623
  - Owner: ml-team@company.com
  - Type: parameter

[Verifying Watermark]
✓ Watermark VERIFIED!
  - Verification Score: 0.853
  - Owner: ml-team@company.com

[Robustness Testing]
✓ Accuracy preserved: 84.00% → 84.00% (0.00% loss)
✓ Watermark metadata accessible
```

## 🎓 What You'll Learn

1. **How watermarking works** across different model types
2. **Trade-offs** between different watermarking techniques
3. **Configuration options** and their effects
4. **Accuracy impact** of watermarking (typically <0.1%)
5. **Verification process** and scoring
6. **Real-world applications** for IP protection

## 🔍 Supported Model Types

### Traditional ML
- ✅ sklearn RandomForest, GradientBoosting
- ✅ sklearn Logistic Regression, SVM
- ✅ XGBoost (if installed)
- ✅ LightGBM (if installed)
- ✅ CatBoost (if installed)

### Deep Learning
- ✅ PyTorch models (all nn.Module)
- ✅ TensorFlow/Keras models
- ✅ HuggingFace Transformers

### Computer Vision
- ✅ ONNX models

## 💡 Use Cases Demonstrated

### 1. Model IP Protection
Prove ownership of proprietary models in legal disputes

### 2. Model Theft Detection
Identify stolen or leaked models using watermark verification

### 3. Model Provenance Tracking
Maintain chain of custody for model lineage

### 4. License Enforcement
Verify authorized model usage and distribution

### 5. Supply Chain Security
Detect model tampering or unauthorized modifications

## 🏆 Best Practices

### For Maximum Robustness
- Use **Parameter watermarking** for models you control
- Set strength to **0.01** (balance between robustness and fidelity)
- Use embed rate of **0.1** (10% of parameters)

### For API-Only Models
- Use **Trigger Set watermarking**
- Store trigger sets securely (they prove ownership)
- Create diverse trigger patterns

### For Detection
- Use **Statistical watermarking**
- Combine with other techniques
- Monitor for major changes

## 📖 Interactive Menu Options

After watermark embedding, you can:

1. **Verify watermark again** - Re-run verification
2. **Compare techniques** - See side-by-side comparison
3. **View watermark info** - Inspect complete metadata
4. **Start new demo** - Try different model/technique
5. **Exit demo** - View summary and exit

## 🎯 Next Steps

After running the demo:

1. **Integrate into your pipeline**: Add watermarking to your ML workflow
2. **Test with your models**: Try with your own PyTorch, TensorFlow, or sklearn models
3. **Combine with signing**: Use cryptographic signing for maximum security
4. **Document for IP**: Keep watermark records for legal protection

## 🤝 Contributing

Found a bug or have a suggestion? Open an issue or PR!

## 📄 License

Apache 2.0

## 🙏 Acknowledgments

Built on SecureML's universal watermarking engine, supporting all major ML frameworks.

---

**Ready to protect your ML models? Start the demo now!**

```bash
python3 examples/interactive_watermarking_demo.py
```
