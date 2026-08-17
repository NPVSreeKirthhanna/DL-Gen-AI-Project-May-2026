from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd


# Train final TF-IDF model
X_train = binary_train["text"]
y_train = binary_train["label"]

tfidf = TfidfVectorizer(
    max_features=50000,
    ngram_range=(1, 2),
    stop_words="english"
)

X_train_vec = tfidf.fit_transform(X_train)

final_model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

final_model.fit(X_train_vec, y_train)


# Build test binary dataset
test_rows = []

for _, row in test_df.iterrows():
    for option in ["A", "B", "C", "D", "E"]:
        test_rows.append({
            "id": row["id"],
            "option": option,
            "text": f"Question: {row['prompt']} Answer: {row[option]}"
        })

binary_test = pd.DataFrame(test_rows)


# Predict test probabilities
X_test = tfidf.transform(binary_test["text"])

binary_test["score"] = final_model.predict_proba(X_test)[:, 1]


# Create submission
predictions = []

for qid, grp in binary_test.groupby("id"):
    grp = grp.sort_values("score", ascending=False)

    top3 = grp["option"].head(3).tolist()

    predictions.append({
        "id": qid,
        "Prediction": " ".join(top3)
    })

submission = pd.DataFrame(predictions)

submission.to_csv("submission.csv", index=False)


# Validate submission
assert len(submission) == len(test_df)
assert submission["id"].nunique() == len(test_df)

for pred in submission["Prediction"]:
    labels = pred.split()

    assert len(labels) == 3
    assert len(set(labels)) == 3
    assert all(x in ["A", "B", "C", "D", "E"] for x in labels)

print("Submission validation passed!")