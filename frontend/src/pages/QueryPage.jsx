// src/pages/QueryPage.jsx

import React, { useState } from 'react';
import { askQuestion } from '../api/client';

function QueryPage() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [status, setStatus] = useState({
    loading: false,
    error: null,
  });

  const handleAsk = async () => {
    if (!question) {
      setStatus({ loading: false, error: 'Question cannot be empty.' });
      return;
    }

    setStatus({ loading: true, error: null });
    setAnswer(''); // Clear previous answer

    try {
      const response = await askQuestion(question);
      setAnswer(response.answer);
      setStatus({ loading: false, error: null });
    } catch (error) {
      setStatus({ loading: false, error: error.message });
    }
  };

  return (
    <div className="flex min-h-screen flex-col items-center bg-gray-900 p-4 text-white sm:p-8">
      <div className="w-full max-w-2xl">
        <h1 className="mb-6 text-center text-4xl font-bold text-cyan-400">
          Ask Your Codebase
        </h1>

        {/* --- Input Section --- */}
        <div className="rounded-lg bg-gray-800 p-6 shadow-lg">
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., How does authentication work?"
            className="h-28 w-full rounded-md border-gray-600 bg-gray-700 p-3 text-white placeholder-gray-500 focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
            disabled={status.loading}
          />
          <button
            onClick={handleAsk}
            disabled={status.loading}
            className="mt-4 w-full rounded-md bg-cyan-600 py-3 font-semibold text-white transition-colors hover:bg-cyan-700 disabled:cursor-not-allowed disabled:bg-gray-600"
          >
            {status.loading ? 'Thinking...' : 'Ask Question'}
          </button>
        </div>

        {/* --- Answer Section --- */}
        <div className="mt-8 min-h-[10rem] w-full">
          {status.loading && (
            <p className="text-center text-gray-400">Searching for an answer...</p>
          )}
          {status.error && (
            <div className="rounded-md border border-red-500 bg-red-900/20 p-4 text-red-300">
              <p className="font-semibold">Error</p>
              <p>{status.error}</p>
            </div>
          )}
          {answer && (
            <div className="rounded-lg bg-gray-800 p-6 shadow-lg">
              <h2 className="mb-4 text-2xl font-semibold text-cyan-400">Answer</h2>
              <p className="whitespace-pre-wrap leading-relaxed text-gray-300">
                {answer}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default QueryPage;
