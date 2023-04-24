import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Function to calculate Textual Similarity
def calculate_textual_similarity(text1, text2):
    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    return 100 - (nltk.edit_distance(tokens1, tokens2) * 100) / max(len(tokens1), len(tokens2))

# Function to calculate Linguistic Similarity
def calculate_linguistic_similarity(text1, text2):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(treebank_tag):
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def preprocess_text(text):
        tokens = word_tokenize(text.lower())
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if token not in stop_words]
        tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(nltk.pos_tag([token])[0][1])) for token in tokens]
        return tokens

    tokens1 = preprocess_text(text1)
    tokens2 = preprocess_text(text2)
    vectorizer = TfidfVectorizer(tokenizer=preprocess_text)
    vectors = vectorizer.fit_transform([text1, text2])
    cosine_similarities = cosine_similarity(vectors)[0, 1]
    return round(cosine_similarities * 100, 2)

# Function to calculate Semantic Similarity
def calculate_semantic_similarity(text1, text2):
    return 0 # todo

def highlight_text_differences(text1, text2):
    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    common_tokens = set(tokens1).intersection(tokens2)
    new_text1 = []
    new_text2 = []
    for token in tokens1:
        if token in common_tokens:
            new_text1.append("<span style='color:green'>{}</span>".format(token))
        else:
            new_text1.append("<span style='color:red'>{}</span>".format(token))
    for token in tokens2:
        if token in common_tokens:
            new_text2.append("<span style='color:green'>{}</span>".format(token))
        else:
            new_text2.append("<span style='color:red'>{}</span>".format(token))
    new_text1 = " ".join(new_text1)
    new_text2 = " ".join(new_text2)
    return new_text1, new_text2