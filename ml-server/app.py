from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)
CORS(app)

# Ensure upload directory exists
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

import os
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/", methods=["GET"])
def home():
    return "Hello, Flask is running!"

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in request"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    try:
        file_path = f"{UPLOAD_FOLDER}/{file.filename}"
        file.save(file_path)  # Save file to 'uploads/' folder

        # Read CSV file
        df = pd.read_csv(file_path)

        # Ensure file is not empty
        if df.empty:
            return jsonify({"error": "Uploaded file is empty!"})

        # Split data into X (features) and y (target)
        X = df.iloc[:, :-1]  
        y = df.iloc[:, -1]

        # Normalize data
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train Logistic Regression model
        model = LogisticRegression(max_iter=1000)  # Increased max_iter to 1000
        model.fit(X_train, y_train)

        # Calculate model accuracy
        accuracy = model.score(X_test, y_test)

        return jsonify({"message": "Model trained successfully", "accuracy": round(accuracy, 4)})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
