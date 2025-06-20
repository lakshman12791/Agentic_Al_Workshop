
import React, { useState } from 'react';

function FeedbackUploader() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  // const handleFileChange = (e) => {
  //   console.log("e", e)

  //   setFile(e.target.files[0]);
  //   setError(null);
  // };

  // const handleUpload = async () => {
  //   if (!file) {
  //     setError('Please select a file');
  //     return;
  //   }

  //   setUploading(true);
  //   const formData = new FormData();
  //   console.log("files", file)
  //   formData.append('feedback', file);

  //   try {
  //     const response = await fetch('http://localhost:3001/api/feedback-parser/upload', {
  //       method: 'POST',
  //       body: formData,
  //       // Let the browser set the Content-Type header for FormData
  //     });

  //     if (!response.ok) {
  //       throw new Error('Upload failed');
  //     }

  //     const data = await response.json();
  //     console.log('Upload success:', data);
  //   } catch (err) {
  //     setError(err.message);
  //   } finally {
  //     setUploading(false);
  //   }
  // };


  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];

    // Validate file type
    if (selectedFile && !selectedFile.name.toLowerCase().endsWith('.json')) {
      setError('Please select a JSON file');
      return;
    }

    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file');
      return;
    }

    setUploading(true);
    const formData = new FormData();
    formData.append('feedback', file);

    // Add additional metadata if needed
    formData.append('fileType', 'json');

    try {
      const response = await fetch('http://localhost:3001/api/feedback-parser/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('Upload success:', data);

      // Reset form after successful upload
      setFile(null);
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';

    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };


  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
      <h2 className="text-xl font-semibold mb-4">Upload Feedback</h2>
      <input
        type="file"
        // accept=".txt,.csv,.json"
        accept=".json"

        onChange={handleFileChange}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        disabled={uploading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
}

export default FeedbackUploader;