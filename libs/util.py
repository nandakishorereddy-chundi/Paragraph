import nltk
import string

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

def cleanse_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    words = [word for word in stripped if word.isalpha() and len(word) >= 4]
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    return words