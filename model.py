import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle

def train_model(data_file):
    df = pd.read_csv(data_file)

    # Features = the columns we use to make predictions
    skill_cols = ["python","sql","tableau","power_bi","spark","aws",
                  "excel","machine_learning","pytorch","tensorflow",
                  "pandas","dbt","airflow","kafka"]

    # Only keep columns that exist in our data
    feature_cols = [c for c in skill_cols if c in df.columns]
    feature_cols.append("salary_avg")

    X = df[feature_cols].fillna(0)  # X = inputs
    y = df["seniority"]             # y = what we predict

    # Convert Junior/Mid/Senior to numbers
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42
    )

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel accuracy: {accuracy:.1%}")
    print("\nDetailed report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Which skills matter most?
    importances = pd.Series(
        model.feature_importances_,
        index=feature_cols
    ).sort_values(ascending=False)
    print("\nTop features:")
    print(importances.head(10))

    # Save the model
    with open("data/model.pkl", "wb") as f:
        pickle.dump((model, le, feature_cols), f)

    print("\nModel saved to data/model.pkl")
    return model, le, feature_cols

if __name__ == "__main__":
    train_model("data/clean_jobs.csv")