import { useState, useEffect } from "react";
import axios from "axios";

function Upload() {
    const [file, setFile] = useState(null);
    const [algorithm, setAlgorithm] = useState("KNN");
    const [iterations, setIterations] = useState(0);
    const [accuracy, setAccuracy] = useState(null);
    const [graphData, setGraphData] = useState(null);
    const [training, setTraining] = useState(false);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleAlgorithmChange = (e) => {
        setAlgorithm(e.target.value);
    };

    const handleUploadAndTrain = async () => {
        if (!file) {
            alert("Please select a file!");
            return;
        }

        setTraining(true);
        setIterations(0);
        setAccuracy(null);
        setGraphData(null);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("algorithm", algorithm);

        try {
            const eventSource = new EventSource("http://127.0.0.1:5000/train");
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                setIterations(data.iterations);
                setAccuracy(data.accuracy.toFixed(4));
                setGraphData(data.graph);
            };

            eventSource.onerror = () => {
                eventSource.close();
                setTraining(false);
            };
        } catch (error) {
            console.error("Training failed:", error);
            alert("Training failed. Check console for errors.");
            setTraining(false);
        }
    };

    return (
        <div style={{ textAlign: "center" }}>
            <h1>ML Model Trainer</h1>

            <label>
                <b>Upload Dataset & Select Algorithm</b>
            </label>
            <br />
            <input type="file" onChange={handleFileChange} />
            <select onChange={handleAlgorithmChange}>
                <option value="KNN">KNN</option>
                <option value="SVM">SVM</option>
                <option value="Decision Tree">Decision Tree</option>
                <option value="Naive Bayes">Naive Bayes</option>
                <option value="Logistic Regression">Logistic Regression</option>
                <option value="Random Forest">Random Forest</option>
                <option value="Gradient Boosting">Gradient Boosting</option>
            </select>
            <button onClick={handleUploadAndTrain} disabled={training}>
                {training ? "Training..." : "Upload & Train"}
            </button>

            <h2>Training Progress</h2>
            <p>Iterations: {iterations}</p>
            <p>Final Accuracy: {accuracy !== null ? accuracy : "N/A"}</p>

            {/* Display Graph */}
            {graphData ? (
                <img src={`data:image/png;base64,${graphData}`} alt="Training Graph" style={{ width: "500px" }} />
            ) : (
                <p>Graph will appear during training...</p>
            )}
        </div>
    );
}

export default Upload;
