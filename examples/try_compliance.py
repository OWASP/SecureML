"""
SecureML Compliance Validation Example
Demonstrates compliance checking against regulatory frameworks
"""

from secureml.core.compliance import ComplianceValidator, ComplianceStatus
from secureml.utils.config import ComplianceFramework, SecurityConfig, SecurityLevel
from pathlib import Path
import tempfile

print("=" * 70)
print("⚖️  SecureML Compliance Validation")
print("=" * 70)

# ============================================================================
# USE CASE 1: SOC 2 Compliance Check
# ============================================================================
print("\n📋 USE CASE 1: SOC 2 Compliance Validation")
print("-" * 70)

validator = ComplianceValidator()

# Create a model path (simulated)
temp_dir = Path(tempfile.mkdtemp())
model_path = temp_dir / "model.pkl"
model_path.touch()

# Check SOC 2 compliance with basic config
print("\n1. Checking SOC 2 compliance (Basic config)...")
basic_config = SecurityConfig.from_level(SecurityLevel.BASIC)

report = validator.validate_compliance(
    model_path=model_path,
    signature_path=None,  # No signature
    frameworks=[ComplianceFramework.SOC2],
    config=basic_config.to_dict()
)

print(f"\n   Overall Status: {report.overall_status.value.upper()}")
print(f"   Total Checks: {report.summary['total_checks']}")
print(f"   ✓ Compliant: {report.summary['compliant']}")
print(f"   ✗ Non-compliant: {report.summary['non_compliant']}")

print("\n   Individual Checks:")
for check in report.checks:
    status_icon = "✓" if check.status == ComplianceStatus.COMPLIANT else "✗"
    print(f"   {status_icon} {check.check_id}: {check.name}")
    if check.remediation:
        print(f"      → {check.remediation}")

# ============================================================================
# USE CASE 2: Multiple Framework Validation
# ============================================================================
print("\n\n🌐 USE CASE 2: Multi-Framework Validation")
print("-" * 70)

# Check against multiple frameworks with Enterprise config
print("\nValidating against SOC 2, ISO 27001, and HIPAA...")
enterprise_config = SecurityConfig.from_level(SecurityLevel.ENTERPRISE)
enterprise_config.enable_audit_logging = True

report_multi = validator.validate_compliance(
    model_path=model_path,
    signature_path=model_path.with_suffix(".sig"),  # Simulated signature
    frameworks=[
        ComplianceFramework.SOC2,
        ComplianceFramework.ISO27001,
        ComplianceFramework.HIPAA
    ],
    config=enterprise_config.to_dict()
)

print(f"\n   Overall Status: {report_multi.overall_status.value.upper()}")
print(f"   Frameworks checked: {len([ComplianceFramework.SOC2, ComplianceFramework.ISO27001, ComplianceFramework.HIPAA])}")
print(f"   Total checks: {report_multi.summary['total_checks']}")
print(f"   Compliance rate: {report_multi.summary['compliant'] / report_multi.summary['total_checks'] * 100:.1f}%")

print("\n   Results by framework:")
framework_checks = {}
for check in report_multi.checks:
    framework = check.check_id.split('-')[0]
    if framework not in framework_checks:
        framework_checks[framework] = {'compliant': 0, 'total': 0}
    framework_checks[framework]['total'] += 1
    if check.status == ComplianceStatus.COMPLIANT:
        framework_checks[framework]['compliant'] += 1

for fw, counts in framework_checks.items():
    rate = counts['compliant'] / counts['total'] * 100
    print(f"   • {fw}: {counts['compliant']}/{counts['total']} ({rate:.0f}%)")

# ============================================================================
# USE CASE 3: FIPS 140-2 Cryptographic Compliance
# ============================================================================
print("\n\n🔐 USE CASE 3: FIPS 140-2 Cryptographic Compliance")
print("-" * 70)

# Test with FIPS-approved algorithms
print("\n1. Testing with FIPS-approved algorithms...")
fips_config = SecurityConfig.from_level(SecurityLevel.MAXIMUM)
fips_config.hash_algorithms = ["sha256", "sha512"]  # FIPS approved

report_fips = validator.validate_compliance(
    model_path=model_path,
    frameworks=[ComplianceFramework.FIPS_140_2],
    config=fips_config.to_dict()
)

print(f"   Status: {report_fips.overall_status.value.upper()}")
for check in report_fips.checks:
    print(f"   • {check.name}: {check.status.value}")
    print(f"     Algorithms: {check.details.get('algorithms', [])}")

# Test with non-FIPS algorithms
print("\n2. Testing with non-FIPS algorithm (MD5)...")
non_fips_config = SecurityConfig.from_level(SecurityLevel.BASIC)
non_fips_config.hash_algorithms = ["md5"]  # Not FIPS approved

report_non_fips = validator.validate_compliance(
    model_path=model_path,
    frameworks=[ComplianceFramework.FIPS_140_2],
    config=non_fips_config.to_dict()
)

print(f"   Status: {report_non_fips.overall_status.value.upper()}")
for check in report_non_fips.checks:
    if check.status == ComplianceStatus.NON_COMPLIANT:
        print(f"   ✗ {check.name}: {check.status.value}")
        print(f"     Remediation: {check.remediation}")

# ============================================================================
# USE CASE 4: GDPR Compliance
# ============================================================================
print("\n\n🇪🇺 USE CASE 4: GDPR Compliance Check")
print("-" * 70)

print("\nChecking GDPR compliance...")
gdpr_config = SecurityConfig.from_level(SecurityLevel.MAXIMUM)
gdpr_config.enable_encryption = True

report_gdpr = validator.validate_compliance(
    model_path=model_path,
    signature_path=model_path.with_suffix(".sig"),
    frameworks=[ComplianceFramework.GDPR],
    config=gdpr_config.to_dict()
)

print(f"\n   Status: {report_gdpr.overall_status.value.upper()}")
print("\n   GDPR Requirements:")
for check in report_gdpr.checks:
    status_icon = "✓" if check.status == ComplianceStatus.COMPLIANT else "⚠"
    print(f"   {status_icon} {check.check_id}: {check.name}")
    print(f"      {check.description}")

# ============================================================================
# USE CASE 5: Generate Compliance Report
# ============================================================================
print("\n\n📄 USE CASE 5: Generate Compliance Report")
print("-" * 70)

report_path = temp_dir / "compliance_report.json"

print(f"\n1. Generating compliance report...")
print(f"   Output: {report_path}")

validator.generate_report_document(
    report=report_multi,
    output_path=report_path,
    format="json"
)

print("   ✓ Report generated")

# Show report structure
import json
with open(report_path) as f:
    report_data = json.load(f)

print("\n2. Report contents:")
print(f"   • Framework: {report_data.get('framework', 'multiple')}")
print(f"   • Overall status: {report_data['overall_status']}")
print(f"   • Timestamp: {report_data['timestamp']}")
print(f"   • Total checks: {report_data['summary']['total_checks']}")
print(f"   • Checks in report: {len(report_data['checks'])}")

# ============================================================================
# USE CASE 6: Compliance Comparison Matrix
# ============================================================================
print("\n\n📊 USE CASE 6: Compliance Comparison Matrix")
print("-" * 70)

all_frameworks = [
    ComplianceFramework.SOC2,
    ComplianceFramework.ISO27001,
    ComplianceFramework.FIPS_140_2,
    ComplianceFramework.HIPAA,
    ComplianceFramework.GDPR
]

print("\nComparing different security levels across frameworks:")
print(f"\n{'Framework':<15} {'BASIC':<10} {'STANDARD':<10} {'ENTERPRISE':<12} {'MAXIMUM':<10}")
print("-" * 60)

for framework in all_frameworks:
    row = f"{framework.value:<15}"

    for level in [SecurityLevel.BASIC, SecurityLevel.STANDARD,
                  SecurityLevel.ENTERPRISE, SecurityLevel.MAXIMUM]:
        config = SecurityConfig.from_level(level)
        if level == SecurityLevel.MAXIMUM:
            config.enable_encryption = True

        report = validator.validate_compliance(
            model_path=model_path,
            signature_path=model_path.with_suffix(".sig") if level != SecurityLevel.BASIC else None,
            frameworks=[framework],
            config=config.to_dict()
        )

        # Calculate compliance rate
        if report.summary['total_checks'] > 0:
            rate = report.summary['compliant'] / report.summary['total_checks'] * 100
            row += f"{rate:>8.0f}%  "
        else:
            row += f"{'N/A':>8}  "

    print(row)

# ============================================================================
# Summary
# ============================================================================
print("\n\n" + "=" * 70)
print("✅ All compliance validation use cases completed!")
print("=" * 70)

print("\n⚖️  Key Takeaways:")
print("   • Multiple compliance frameworks supported")
print("   • Automated compliance checking")
print("   • Detailed remediation guidance")
print("   • JSON report generation")
print("   • Security level impacts compliance")

print("\n💡 Supported Frameworks:")
for fw in ComplianceFramework:
    print(f"   • {fw.value.upper()}")

print("\n📝 To improve compliance:")
print("   • Use higher security levels (ENTERPRISE or MAXIMUM)")
print("   • Enable digital signatures")
print("   • Enable audit logging")
print("   • Use FIPS-approved algorithms")
print("   • Enable encryption for sensitive data")

# Cleanup
import shutil
shutil.rmtree(temp_dir)
