import React, { useState } from "react";
import axios from "axios";

const Upload = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:4000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded successfully!");
    } catch (error) {
      console.error("Upload error:", error);
      alert("File upload failed!");
    }
  };

  return (
    <div>
      <h2>Upload Dataset</h2>
      <label htmlFor="fileUpload">Choose a dataset file:</label>
      <input
        type="file"
        id="fileUpload"
        name="datasetFile"
        onChange={handleFileChange}
      />
      <button title="Upload selected file" onClick={handleUpload}>
        Upload
      </button>
    </div>
  );
};

export default Upload;
