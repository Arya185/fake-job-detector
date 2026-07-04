import pandas as pd
import re

def clean_text(text):
    """Clean a single text string."""
    if not isinstance(text, str):
        return ""
    # Lowercase
    text = text.lower()
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_and_preprocess(filepath):
    """Load dataset and return cleaned features and labels."""
    df = pd.read_csv(filepath)

    # Combine the most informative text columns
    text_columns = ['title', 'company_profile', 'description', 'requirements', 'benefits']
    
    # Fill missing values with empty string, then combine
    df['combined_text'] = df[text_columns].fillna('').agg(' '.join, axis=1)
    
    # Clean the combined text
    df['cleaned_text'] = df['combined_text'].apply(clean_text)
    
    # Features and labels
    X = df['cleaned_text']
    y = df['fraudulent']
    
    print(f"✅ Dataset loaded: {len(df)} rows")
    print(f"✅ Fraud distribution:\n{y.value_counts()}")
    
    return X, y

# Quick test when run directly
if __name__ == "__main__":
    X, y = load_and_preprocess("data/fake_job_postings.csv")
    print(f"\n✅ Sample cleaned text:\n{X.iloc[0][:300]}")