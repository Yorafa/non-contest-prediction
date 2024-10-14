from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error
import numpy as np
from typing import List, Dict, Tuple

def get_avg_per_level(questions: List[Dict]) -> List[float]:
    easy, medium, hard = [], [], []
    for q in questions:
        if q["rating"] is None:
            continue
        if q["difficulty"] == "Easy":
            easy.append(q["rating"])
        elif q["difficulty"] == "Medium":
            medium.append(q["rating"])
        else:
            hard.append(q["rating"])
    return {"Easy": np.mean(easy), "Medium": np.mean(medium), "Hard": np.mean(hard)}

# apply difficulty score to questions
def apply_difficulty_score(questions: List[Dict], avg_rating: Dict):
    for q in questions:
        q["difficulty_score"] = avg_rating[q["difficulty"]]
    return questions

def get_X_y(questions: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
    X, y = [], []
    for q in questions:
        # we want to use freqBar, acRate, totalAcceptedRaw, totalSubmissionRaw, difficulty_score
        X.append([q["totalAcceptedRaw"], q["totalSubmissionRaw"], q["difficulty_score"]])
        y.append(q["rating"])
    return np.array(X), np.array(y)

def train_predict_data_split(question: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    avg_rating = get_avg_per_level(question)
    question = apply_difficulty_score(question, avg_rating)
    # no rating data means we will predict the rating later
    predict_data = []
    train_data = []
    for q in question:
        if q["rating"] is None:
            predict_data.append(q)
        else:
            train_data.append(q)
    return train_data, predict_data

def train_model(train_data: List[Dict]) -> LinearRegression:
    X, y = get_X_y(train_data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    print(f"Train score: {model.score(X_train, y_train)}")
    print(f"Test score: {model.score(X_test, y_test)}")
    print(f"Mean squared error: {root_mean_squared_error(y_test, model.predict(X_test))}")
    return model

if __name__ == '__main__':
    from get_data import load_questions, save_questions
    questions = load_questions("../data/questions_with_rating.json")
    train_data, predict_data = train_predict_data_split(questions)
    model = train_model(train_data)
    X, y = get_X_y(predict_data)
    predictions = model.predict(X)
    for q, p in zip(predict_data, predictions):
        q["predicted_rating"] = p
    save_questions(questions, "../data/questions_with_predicted_rating.json")