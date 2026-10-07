import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ================= READ DATASET =================

dataset = pd.read_csv("data/UpdatedResumeDataSet.csv")

# ================= FEATURES & LABELS =================

X = dataset["Resume"]
Y = dataset["Category"]

# ================= TRAIN TEST SPLIT =================

X_train, X_test, Y_train, Y_test = train_test_split(
    X,
    Y,
    test_size=0.2,
    random_state=42
)

# ================= TF-IDF =================

vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)

X_test = vectorizer.transform(X_test)

# ================= LOGISTIC REGRESSION =================

model = LogisticRegression()

model.fit(X_train, Y_train)

# ================= PREDICTION =================

prediction = model.predict(X_test)

# ================= ACCURACY =================

accuracy = accuracy_score(Y_test, prediction)

print("Accuracy :", round(accuracy * 100, 2), "%")

# ================= SAVE MODEL =================

joblib.dump(model, "models/logistic_model.pkl")

joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("\nModel Saved Successfully.")

print("Vectorizer Saved Successfully.")

# ================= LOAD MODEL =================

loaded_model = joblib.load("models/logistic_model.pkl")

loaded_vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

print("\nModel Loaded Successfully.")

# ================= TEST NEW RESUME =================

sample_resume = """
Python
SQL
Machine Learning
TensorFlow
Pandas
Git
Docker
"""

sample_resume = loaded_vectorizer.transform([sample_resume])

prediction = loaded_model.predict(sample_resume)

print("\nPredicted Category :")

print(prediction[0])