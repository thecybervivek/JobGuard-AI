def check_job(job_text):

    job_text = job_text.lower()

    score = 0
    reasons = []

    # Check if the job asks for money
    payment_words = [
        "registration fee",
        "processing fee",
        "training fee",
        "security deposit"
    ]

    for word in payment_words:
        if word in job_text:
            score = score + 25
            reasons.append("Job asks for payment")
            break

    # Check for guaranteed job claims
    guaranteed_words = [
        "guaranteed job",
        "guaranteed employment",
        "100% job guarantee"
    ]

    for word in guaranteed_words:
        if word in job_text:
            score = score + 20
            reasons.append("Guaranteed job claim found")
            break

    # Check suspicious contact methods
    contact_words = [
        "whatsapp only",
        "only on whatsapp",
        "telegram only"
    ]

    for word in contact_words:
        if word in job_text:
            score = score + 15
            reasons.append("Suspicious contact method found")
            break

    # Check urgent or pressure language
    urgent_words = [
        "urgent hiring",
        "apply now",
        "limited seats",
        "hurry"
    ]

    for word in urgent_words:
        if word in job_text:
            score = score + 10
            reasons.append("Urgent hiring language found")
            break

    # Decide the risk level
    if score >= 60:
        risk = "High Risk"
    elif score >= 30:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"

    return score, risk, reasons


# Testing the program
job_description = """
URGENT HIRING!

Guaranteed job for everyone.

Pay a registration fee of Rs. 2000.

Contact us only on WhatsApp.

Limited seats available. Apply now!
"""

score, risk, reasons = check_job(job_description)

print("JobGuard AI - Fake Job Detector")
print()

print("Risk Score:", score)
print("Risk Level:", risk)

print("\nReasons:")
for reason in reasons:
    print("-", reason)