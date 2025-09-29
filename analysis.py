from flask import Flask, render_template, request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from collections import Counter
import string

app = Flask(__name__)

# Initialize analyzer
analyzer = SentimentIntensityAnalyzer()

# Enhanced sentiment dictionaries
POSITIVE_WORDS = {
    'excellent', 'amazing', 'outstanding', 'brilliant', 'fantastic', 'awesome',
    'masterpiece', 'perfect', 'flawless', 'superb', 'magnificent', 'wonderful',
    'captivating', 'engaging', 'thrilling', 'emotional', 'powerful', 'beautiful',
    'stunning', 'breathtaking', 'memorable', 'unforgettable', 'innovative',
    'groundbreaking', 'revolutionary', 'inspiring', 'touching', 'heartwarming',
    'hilarious', 'entertaining', 'compelling', 'gripping', 'suspenseful', 'great',
    'good', 'best', 'love', 'loved', 'enjoyed', 'awesome', 'fantastic', 'wonderful','inspired'
}

NEGATIVE_WORDS = {
    'terrible', 'awful', 'horrible', 'disappointing', 'boring', 'predictable',
    'confusing', 'messy', 'weak', 'poor', 'bad', 'worst', 'waste', 'pointless',
    'ridiculous', 'stupid', 'nonsense', 'uninspired', 'cliché', 'cliche',
    'forgettable', 'overrated', 'underwhelming', 'mediocre', 'generic',
    'formulaic', 'pretentious', 'dragging', 'slow', 'rushed', 'incoherent',
    'hate', 'hated', 'dislike', 'awful', 'terrible', 'boring', 'bad','not'
}

EMOTION_WORDS = {
    'happy': {'joy', 'delight', 'happy', 'pleasure', 'excitement', 'thrilled', 'fun', 'enjoyable'},
    'sad': {'sad', 'depressing', 'heartbreaking', 'tragic', 'melancholy', 'grief', 'sorrow'},
    'angry': {'angry', 'frustrating', 'annoying', 'infuriating', 'rage', 'outrage', 'mad'},
    'fear': {'scary', 'frightening', 'terrifying', 'horror', 'dread', 'anxiety', 'fear'},
    'surprise': {'surprising', 'shocking', 'unexpected', 'twist', 'revelation', 'surprise'},
    'love': {'romantic', 'love', 'affection', 'passion', 'heartwarming', 'tender', 'caring'}
}

GENRE_INDICATORS = {
    'action': {'action', 'fight', 'battle', 'explosion', 'thriller', 'adventure', 'chase', 'combat'},
    'comedy': {'funny', 'comedy', 'humor', 'laugh', 'hilarious', 'joke', 'comic', 'humorous'},
    'drama': {'drama', 'emotional', 'serious', 'realistic', 'character', 'story', 'plot'},
    'horror': {'horror', 'scary', 'frightening', 'terror', 'ghost', 'monster', 'creepy'},
    'romance': {'romance', 'love', 'relationship', 'couple', 'romantic', 'heart', 'affection'},
    'sci-fi': {'sci-fi', 'science', 'future', 'space', 'alien', 'technology', 'robot'},
    'fantasy': {'fantasy', 'magic', 'mythical', 'dragon', 'wizard', 'kingdom', 'magical'}
}

# Common English stopwords
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", 
    "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 
    'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
    'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 
    'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 
    'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
    'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 
    'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 
    'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
    'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 
    'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 
    'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 
    'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', 
    "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 
    'wouldn', "wouldn't"
}

def simple_tokenize(text):
    """Simple tokenizer without complex NLTK dependency"""
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Split into words and filter
    words = text.split()
    filtered_words = [word for word in words if word not in STOP_WORDS and len(word) > 2]
    
    return filtered_words

def analyze_keywords(text):
    """Analyze keywords and their frequencies in the text"""
    tokens = simple_tokenize(text)
    
    # Count word frequencies
    word_freq = Counter(tokens)
    
    # Find positive and negative words
    found_positive = {word: count for word, count in word_freq.items() if word in POSITIVE_WORDS}
    found_negative = {word: count for word, count in word_freq.items() if word in NEGATIVE_WORDS}
    
    # Detect emotions
    emotions_detected = {}
    for emotion, words in EMOTION_WORDS.items():
        emotion_words = [word for word in words if word in word_freq]
        if emotion_words:
            emotions_detected[emotion] = emotion_words
    
    # Detect genre indicators
    genres_suggested = {}
    for genre, words in GENRE_INDICATORS.items():
        genre_words = [word for word in words if word in word_freq]
        if genre_words:
            genres_suggested[genre] = genre_words
    
    return {
        'word_frequency': dict(word_freq.most_common(10)),
        'positive_words': found_positive,
        'negative_words': found_negative,
        'emotions': emotions_detected,
        'genres': genres_suggested,
        'total_words': len(tokens)
    }

def get_detailed_analysis(scores, keywords):
    """Generate detailed analysis based on scores and keywords"""
    compound = scores['compound']
    
    # Sentiment strength analysis
    if compound >= 0.75:
        strength = "Very Strong Positive"
    elif compound >= 0.5:
        strength = "Strong Positive"
    elif compound >= 0.05:
        strength = "Moderate Positive"
    elif compound >= -0.05:
        strength = "Neutral"
    elif compound >= -0.5:
        strength = "Moderate Negative"
    elif compound >= -0.75:
        strength = "Strong Negative"
    else:
        strength = "Very Strong Negative"
    
    # Generate insights
    insights = []
    
    # Sentiment insights
    if compound > 0.5:
        insights.append("This review expresses strong positive sentiment about the movie.")
    elif compound > 0:
        insights.append("The review has a generally positive tone.")
    elif compound < -0.5:
        insights.append("This review shows strong negative feelings about the movie.")
    elif compound < 0:
        insights.append("The review has a generally negative tone.")
    else:
        insights.append("The review maintains a neutral or balanced perspective.")
    
    # Keyword-based insights
    if keywords['positive_words']:
        insights.append(f"Uses positive words like: {', '.join(list(keywords['positive_words'].keys())[:3])}")
    
    if keywords['negative_words']:
        insights.append(f"Uses negative words like: {', '.join(list(keywords['negative_words'].keys())[:3])}")
    
    if keywords['emotions']:
        emotions_list = list(keywords['emotions'].keys())
        insights.append(f"Expresses {', '.join(emotions_list)} emotions")
    
    if keywords['genres']:
        genres_list = list(keywords['genres'].keys())
        insights.append(f"Suggests {', '.join(genres_list)} elements")
    
    # Writing style insights
    if keywords['total_words'] > 100:
        insights.append("Detailed review with substantial content")
    elif keywords['total_words'] < 30:
        insights.append("Brief and concise review")
    
    return {
        'strength': strength,
        'insights': insights,
        'compound_score': compound
    }

def analyze_sentence_sentiments(text):
    """Analyze sentiment of individual sentences using simple splitting"""
    # Simple sentence splitting by punctuation
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    sentence_analysis = []
    for i, sentence in enumerate(sentences):
        if len(sentence) > 5:  # Only analyze meaningful sentences
            scores = analyzer.polarity_scores(sentence)
            sentiment = "Positive" if scores['compound'] >= 0.05 else "Negative" if scores['compound'] <= -0.05 else "Neutral"
            
            sentence_analysis.append({
                'sentence': sentence,
                'sentiment': sentiment,
                'compound': scores['compound'],
                'position': i + 1
            })
    
    return sentence_analysis

@app.route("/", methods=["GET", "POST"])
def index():
    sentiment = None
    scores = None
    keywords = None
    detailed_analysis = None
    sentence_analysis = None
    
    if request.method == "POST":
        user_input = request.form["review"]
        if user_input.strip() != "":
            # Basic sentiment analysis
            scores = analyzer.polarity_scores(user_input)
            compound = scores['compound']
            
            if compound >= 0.05:
                sentiment = "😊 Positive"
            elif compound <= -0.05:
                sentiment = "😠 Negative"
            else:
                sentiment = "😐 Neutral"
            
            # Enhanced analysis
            keywords = analyze_keywords(user_input)
            detailed_analysis = get_detailed_analysis(scores, keywords)
            sentence_analysis = analyze_sentence_sentiments(user_input)
    
    return render_template("index.html", 
                         sentiment=sentiment, 
                         scores=scores,
                         keywords=keywords,
                         detailed_analysis=detailed_analysis,
                         sentence_analysis=sentence_analysis)

if __name__ == "__main__":
    app.run(debug=True)