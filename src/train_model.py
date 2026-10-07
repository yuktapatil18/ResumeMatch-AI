import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def train_model():

    # Read Dataset
    dataset = pd.read_csv("data/UpdatedResumeDataSet.csv")

    # Features & Labels
    X = dataset["Resume"]
    Y = dataset["Category"]

    # Split Dataset
    X_train, X_test, Y_train, Y_test = train_test_split(
        X,
        Y,
        test_size=0.2,
        random_state=42
    )

    # TF-IDF
    vectorizer = TfidfVectorizer()

    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Train Model
    model = LogisticRegression(max_iter=1000)

    model.fit(X_train, Y_train)

    # Prediction
    prediction = model.predict(X_test)

    # Accuracy
    accuracy = accuracy_score(Y_test, prediction)

    print(f"Accuracy : {accuracy*100:.2f}%")

    # Save Model
    joblib.dump(model, "models/logistic_model.pkl")
    joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

    print("Model Saved Successfully.")
    print("Vectorizer Saved Successfully.")


if __name__ == "__main__":
    train_model()