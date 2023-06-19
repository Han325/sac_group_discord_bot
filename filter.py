from data import get_job_listings

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    words = nltk.word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in words if word.isalpha() and word not in stop_words]

    return ' '.join(words)

def get_relevant_listings(json_data, interests, job_type=None, top_n=10):
    interests = ' '.join(interests)
    
    if 'listings' in json_data:
        listings = json_data['listings']
    else:
        raise ValueError("No 'listings' key in provided dictionary")
    
    if job_type:
        listings = [listing for listing in listings if listing.get('job_type') == job_type]
        
    texts = [preprocess_text(listing['position'] + ' ' + listing['desc']) for listing in listings]
    texts.append(preprocess_text(interests))

    vectorizer = TfidfVectorizer().fit_transform(texts)
    similarity_scores = cosine_similarity(vectorizer[-1], vectorizer).flatten()[:-1]

    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    top_listings = [listings[index] for index in top_indices]

    return top_listings

