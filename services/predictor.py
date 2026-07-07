from utils.text import clean_text
from services.rules import check_rules

def predict_text(
    text,
    tfidf_vectorizer,
    classifier,
):
    cleaned = clean_text(text)
    vec = tfidf_vectorizer.transform([cleaned])
    prediction = classifier.predict(vec)[0]
    probability = classifier.predict_proba(vec)[0]
    label = "Fake 🚨" if prediction == 1 else "Real ✅"
    confidence = round(float(max(probability)) * 100, 2)
    fraud_prob = round(float(probability[1]) * 100, 2)
    rule_result = check_rules(cleaned)

    result = {
        "prediction": label,
        "confidence": f"{confidence}%",
        "fraud_probability": fraud_prob,
        "risk_score": rule_result["risk_score"],
        "matched_rules": rule_result["matched_rules"],
        "matched_keywords": rule_result["matched_keywords"],
    }

    return result
