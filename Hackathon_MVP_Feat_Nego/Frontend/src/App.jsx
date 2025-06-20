// client/src/App.js
import React from 'react';
import './App.css';
import FeedbackUploader from './components/FeedbackUploader';
import FeedbackResults from './components/FeedbackResults';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <h1 className="text-3xl font-bold mb-6">Agentic AI-Based MVP Feature Negotiator</h1>
      <FeedbackUploader />
      <FeedbackResults />
    </div>
  );
}

export default App;