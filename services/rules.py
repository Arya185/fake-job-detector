def check_rules(text):
    RULES = {
        "payment": [
            "registration fee",
            "processing fee",
            "security deposit",
            "training fee",
            "investment required",
            "pay now",
            "joining fee",
        ],
        "contact": [
            "whatsapp",
            "telegram",
            "personal number",
            "dm me",
            "message me",
            "contact urgently",
        ],
        "urgency": [
            "urgent hiring",
            "apply immediately",
            "limited seats",
            "join today",
            "hiring now",
        ],
        "salary": [
            "earn daily",
            "easy income",
            "work from home",
            "no experience",
            "earn lakh",
            "salary up to",
        ],
    }

    risk_score = 0
    matched_rules = []
    matched_keywords = []

    for category, keywords in RULES.items():
        for keyword in keywords:
            if keyword in text:
                matched_keywords.append(keyword)

                if category not in matched_rules:
                    matched_rules.append(category)

                    if category == "payment":
                        risk_score += 30
                    elif category == "contact":
                        risk_score += 20
                    elif category == "urgency":
                        risk_score += 15
                    elif category == "salary":
                        risk_score += 10

    return {
        "risk_score": risk_score,
        "matched_rules": matched_rules,
        "matched_keywords": matched_keywords,
    }
