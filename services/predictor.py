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

    result = {
        "prediction": label,
        "confidence": f"{confidence}%",
        "fraud_probability": fraud_prob,
    }

    return result