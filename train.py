import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import SMOTE
import numpy as np
from services.preprocess import load_and_preprocess

def train():
    print("📦 Loading data...")
    X, y = load_and_preprocess("data/fake_job_postings.csv")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"✅ Train: {len(X_train)} | Test: {len(X_test)}")

    # TF-IDF vectorizer (stronger settings)
    tfidf = TfidfVectorizer(
        max_features=15000,
        ngram_range=(1, 3),
        stop_words='english',
        sublinear_tf=True
    )

    # Vectorize
    X_train_vec = tfidf.fit_transform(X_train)
    X_test_vec = tfidf.transform(X_test)

    # Handle class imbalance with SMOTE
    print("⚖️ Balancing classes with SMOTE...")
    smote = SMOTE(random_state=42)
    X_train_bal, y_train_bal = smote.fit_resample(X_train_vec, y_train)
    print(f"✅ Balanced dataset size: {X_train_bal.shape[0]}")

    # Train Random Forest
    print("🚀 Training Random Forest...")
    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    clf.fit(X_train_bal, y_train_bal)

    # Evaluate
    y_pred = clf.predict(X_test_vec)
    print(f"\n✅ Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Real', 'Fake']))

    # Save both vectorizer and model separately
    joblib.dump(tfidf, "model/tfidf_vectorizer.pkl")
    joblib.dump(clf, "model/random_forest_model.pkl")
    print("\n💾 Model saved!")

if __name__ == "__main__":
    train()