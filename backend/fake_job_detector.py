# JobGuard AI - Fake Job Detector
# Member 4: Shubhangi + Vivek

import re


# =========================================================
# 1. SCAM KEYWORDS
# =========================================================

PAYMENT_SCAM_WORDS = [
    "registration fee",
    "processing fee",
    "training fee",
    "security deposit",
    "refundable fee",
    "pay money",
    "paytm karo",
    "upi payment",
    "investment",
    "joining fee",
    "application fee",
]

GUARANTEED_JOB_WORDS = [
    "guaranteed job",
    "guaranteed employment",
    "100% job guarantee",
    "100% job",
    "pakki naukri",
    "without interview",
    "bina interview ke",
    "earn daily",
    "daily 3000",
    "daily 5000",
    "work from home and earn",
]

CONTACT_SCAM_WORDS = [
    "whatsapp only",
    "only on whatsapp",
    "contact on whatsapp",
    "personal whatsapp",
    "telegram only",
    "contact on telegram",
    "inbox on telegram",
    "t.me/",
]

URGENCY_WORDS = [
    "urgent hiring",
    "apply now",
    "join immediately",
    "today only",
    "last date today",
    "immediately join",
    "limited seats",
    "hurry",
    "aaj hi join karo",
]


# =========================================================
# 2. PAYMENT SCAM CHECK
# =========================================================

def check_payment_scam(text):
    reasons = []

    text = text.lower()

    for word in PAYMENT_SCAM_WORDS:
        if word in text:
            reasons.append(
                f"Payment/fee request found: '{word}'"
            )

    return reasons


# =========================================================
# 3. GUARANTEED JOB CHECK
# =========================================================

def check_guaranteed_claims(text):
    reasons = []

    text = text.lower()

    for word in GUARANTEED_JOB_WORDS:
        if word in text:
            reasons.append(
                f"Unrealistic job claim found: '{word}'"
            )

    return reasons


# =========================================================
# 4. SUSPICIOUS CONTACT CHECK
# =========================================================

def check_suspicious_contact(text):
    reasons = []

    text = text.lower()

    for word in CONTACT_SCAM_WORDS:
        if word in text:
            reasons.append(
                f"Suspicious contact method found: '{word}'"
            )

    # UPI ID detection
    upi_pattern = r"[a-zA-Z0-9._-]{2,}@[a-zA-Z]{2,}"

    if re.search(upi_pattern, text):
        reasons.append(
            "UPI ID/payment information found in job description"
        )

    return reasons


# =========================================================
# 5. URGENCY CHECK
# =========================================================

def check_urgency_tactics(text):
    reasons = []

    text = text.lower()

    for word in URGENCY_WORDS:
        if word in text:
            reasons.append(
                f"Urgency/pressure language found: '{word}'"
            )

    return reasons


# =========================================================
# 6. MAIN FUNCTION
# =========================================================

def analyze_job_risk(job_description):
    """
    Analyze a job description and return a risk report.
    """

    if not job_description:
        return {
            "result": "UNKNOWN",
            "risk_score": 0,
            "risk_level": "Unknown",
            "reasons": ["Job description is empty"]
        }

    all_reasons = []

    # Run all checks
    all_reasons.extend(
        check_payment_scam(job_description)
    )

    all_reasons.extend(
        check_guaranteed_claims(job_description)
    )

    all_reasons.extend(
        check_suspicious_contact(job_description)
    )

    all_reasons.extend(
        check_urgency_tactics(job_description)
    )


    # =====================================================
    # RISK SCORE
    # =====================================================

    # Each detected indicator = 10 points
    risk_score = len(all_reasons) * 10

    # Maximum score = 100
    risk_score = min(risk_score, 100)


    # =====================================================
    # RISK LEVEL
    # =====================================================

    if risk_score >= 60:

        risk_level = "High Risk"
        result = "SUSPICIOUS"

    elif risk_score >= 30:

        risk_level = "Medium Risk"
        result = "SUSPICIOUS"

    else:

        risk_level = "Low Risk"
        result = "LOW RISK"


    # =====================================================
    # FINAL REPORT
    # =====================================================

    final_report = {
        "result": result,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "reasons": (
            all_reasons
            if all_reasons
            else ["No major scam indicators detected"]
        )
    }

    return final_report


# =========================================================
# 7. TESTING
# =========================================================

if __name__ == "__main__":

    test_job = """
    URGENT HIRING!

    Guaranteed job for everyone.

    Work from home and earn daily 5000.

    Pay registration fee of Rs. 2000.

    Contact us only on WhatsApp.

    Limited seats available.
    """

    report = analyze_job_risk(test_job)

    print("\n================================")
    print("     JobGuard AI")
    print("   Fake Job Detector")
    print("================================")

    print("\nResult:", report["result"])
    print("Risk Score:", report["risk_score"])
    print("Risk Level:", report["risk_level"])

    print("\nReasons:")

    for reason in report["reasons"]:
        print("-", reason)