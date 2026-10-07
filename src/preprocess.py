import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


stop_words = set(stopwords.words("english"))

lemmatizer = WordNetLemmatizer()


def to_lowercase(text):
    return text.lower()


def remove_punctuation(text):

    for ch in string.punctuation:
        text = text.replace(ch, "")

    return text


def tokenize(text):
    return text.split()


def remove_stopwords(tokens):

    filtered_tokens = []

    for word in tokens:

        if word not in stop_words:

            filtered_tokens.append(word)

    return filtered_tokens


def lemmatization(tokens):

    lemmatized_tokens = []

    for word in tokens:

        lemmatized_tokens.append(
            lemmatizer.lemmatize(word)
        )

    return lemmatized_tokens


def preprocess_text(text):

    text = to_lowercase(text)

    text = remove_punctuation(text)

    text = tokenize(text)

    text = remove_stopwords(text)

    text = lemmatization(text)

    text = " ".join(text)

    return text