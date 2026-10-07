import joblib
from src.preprocess import preprocess_text

model = joblib.load("models/logistic_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


def predict_category(resume_text):

    resume_text = preprocess_text(resume_text)

    resume_vector = vectorizer.transform([resume_text])

    prediction = model.predict(resume_vector)

    return prediction[0]