// src/pages/IngestPage.jsx

import React, { useState } from 'react';
import { ingestCode } from '../api/client';

function IngestPage() {
  const [dirPath, setDirPath] = useState('');
  const [status, setStatus] = useState({
    loading: false,
    error: null,
    success: null,
  });

  const handleIngest = async () => {
    if (!dirPath) {
      setStatus({ loading: false, error: 'Directory path cannot be empty.', success: null });
      return;
    }

    setStatus({ loading: true, error: null, success: null });

    try {
      const response = await ingestCode(dirPath);
      setStatus({ loading: false, error: null, success: response.message });
    } catch (error) {
      setStatus({ loading: false, error: error.message, success: null });
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
      <div className="w-full max-w-md rounded-lg bg-gray-800 p-8 shadow-lg">
        <h1 className="mb-6 text-center text-3xl font-bold text-cyan-400">
          Code Intelligence Ingestion
        </h1>
        
        <div className="mb-4">
          <label htmlFor="dirPath" className="mb-2 block text-sm font-medium text-gray-300">
            Project Directory Path
          </label>
          <input
            id="dirPath"
            type="text"
            value={dirPath}
            onChange={(e) => setDirPath(e.target.value)}
            placeholder="e.g., C:\Users\YourUser\Projects\my-codebase"
            className="w-full rounded-md border-gray-600 bg-gray-700 p-3 text-white placeholder-gray-500 focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
            disabled={status.loading}
          />
        </div>

        <button
          onClick={handleIngest}
          disabled={status.loading}
          className="w-full rounded-md bg-cyan-600 py-3 font-semibold text-white transition-colors hover:bg-cyan-700 disabled:cursor-not-allowed disabled:bg-gray-600"
        >
          {status.loading ? 'Ingesting...' : 'Ingest Code'}
        </button>

        {/* Status Messages */}
        <div className="mt-6 h-6 text-center">
          {status.error && (
            <p className="text-sm text-red-400">{status.error}</p>
          )}
          {status.success && (
            <p className="text-sm text-green-400">{status.success}</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default IngestPage;
