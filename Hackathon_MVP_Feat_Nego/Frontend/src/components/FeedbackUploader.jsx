
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
    <div
      style={{
        background: 'linear-gradient(to bottom right, #ffffff, #f9fafb)',
        padding: '2rem',
        borderRadius: '1rem',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.08)',
        width: '100%',
        maxWidth: '32rem',
        border: '1px solid #e5e7eb',
        fontFamily: 'Arial, sans-serif',
      }}
    >
      <h2
        style={{
          fontSize: '1.5rem',
          fontWeight: '700',
          color: '#1f2937',
          marginBottom: '1.5rem',
          textAlign: 'center',
        }}
      >
        📤 Upload Feedback
      </h2>

      <label style={{ display: 'block', marginBottom: '1rem' }}>
        <span
          style={{
            display: 'block',
            fontSize: '0.875rem',
            fontWeight: '500',
            color: '#4b5563',
            marginBottom: '0.5rem',
          }}
        >
          Select a JSON file
        </span>
        <input
          type="file"
          accept=".json"
          onChange={handleFileChange}
          style={{
            display: 'block',
            width: '100%',
            fontSize: '0.875rem',
            color: '#374151',
            padding: '0.5rem',
            borderRadius: '0.5rem',
            border: '1px solid #d1d5db',
            cursor: 'pointer',
          }}
        />
      </label>

      <button
        onClick={handleUpload}
        disabled={uploading}
        style={{
          width: '100%',
          padding: '0.75rem',
          borderRadius: '0.5rem',
          fontWeight: '600',
          fontSize: '1rem',
          backgroundColor: uploading ? '#d1d5db' : '#2563eb',
          color: uploading ? '#6b7280' : '#ffffff',
          cursor: uploading ? 'not-allowed' : 'pointer',
          transition: 'background-color 0.2s ease',
        }}
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>

      {error && (
        <p
          style={{
            color: '#dc2626',
            marginTop: '1rem',
            textAlign: 'center',
            fontWeight: '500',
          }}
        >
          {error}
        </p>
      )}
    </div>

  );
}

export default FeedbackUploader;