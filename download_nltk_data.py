# download_nltk_data.py
import nltk

print("Downloading required NLTK data...")

# Download basic punkt tokenizer (works with all NLTK versions)
nltk.download('punkt')
print("✓ punkt downloaded")

# Download stopwords
nltk.download('stopwords')
print("✓ stopwords downloaded")

print("All required NLTK data downloaded successfully!")