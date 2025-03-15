from flask import Flask, request, jsonify, Response
import pandas as pd
import time
import json
import base64
import io
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

app = Flask(__name__)

# Define available algorithms
ALGORITHMS = {
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "SVM": SVC(),
    "Decision Tree": DecisionTreeClassifier(),
    "Naive Bayes": GaussianNB(),
    "Logistic Regression": LogisticRegression(),
    "Random Forest": RandomForestClassifier(),
    "Gradient Boosting": GradientBoostingClassifier(),
}

# Route to check if Flask server is running
@app.route("/")
def home():
    return "Flask Server is Running!"

# Streaming response function for real-time updates
def train_model_stream(df, algorithm):
    X = df.iloc[:, :-1]  # Features
    y = df.iloc[:, -1]   # Target column (last column)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = ALGORITHMS.get(algorithm)
    if not model:
        yield json.dumps({"error": "Invalid algorithm selected"}) + "\n"
        return

    accuracy_list = []
    
    for i in range(1, 21):  # Simulating iterations
        model.fit(X_train, y_train)  # Train model
        accuracy = model.score(X_test, y_test)  # Evaluate model
        accuracy_list.append(accuracy)

        # Generate graph
        plt.figure(figsize=(5, 3))
        plt.plot(range(1, len(accuracy_list) + 1), accuracy_list, marker="o", linestyle="-", color="b")
        plt.xlabel("Iteration")
        plt.ylabel("Accuracy")
        plt.title(f"Training Progress ({algorithm})")
        plt.grid()

        # Convert graph to Base64 image
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close()
        img_str = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

        # Send iteration update to frontend
        yield f"data: {json.dumps({'iterations': i, 'accuracy': accuracy, 'graph': img_str})}\n\n"
        time.sleep(1)

# Train route (using SSE for real-time updates)
@app.route("/train", methods=["POST"])
def train():
    if "file" not in request.files or "algorithm" not in request.form:
        return jsonify({"error": "File and algorithm are required"}), 400

    file = request.files["file"]
    algorithm = request.form["algorithm"]

    try:
        df = pd.read_csv(file)  # Read CSV file
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    return Response(train_model_stream(df, algorithm), content_type="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True)
