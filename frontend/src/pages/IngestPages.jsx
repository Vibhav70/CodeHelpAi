// src/pages/IngestPage.jsx

import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import {
  ingestProjectDirectory,
  uploadProjectSummaries,
  generateDocumentation,
} from '../api/apiClient';

function IngestPage() {
  const { projectId } = useParams(); // Assuming route like /projects/:projectId/ingest
  const [projectName, setProjectName] = useState('');
  const [dirPath, setDirPath] = useState('');
  const [status, setStatus] = useState({
    loading: false,
    error: null,
    success: null,
  });

  // ✅ Ingest code directory
  const handleIngest = async () => {
    if (!dirPath) {
      setStatus({ loading: false, error: 'Directory path cannot be empty.', success: null });
      return;
    }

    setStatus({ loading: true, error: null, success: null });
    try {
      const response = await ingestProjectDirectory(projectId, dirPath);
      setStatus({ loading: false, error: null, success: 'Code ingestion completed successfully!' });
      console.log('Ingest response:', response.data);
    } catch (error) {
      setStatus({
        loading: false,
        error: error.response?.data?.detail || 'Ingestion failed. Please try again.',
        success: null,
      });
    }
  };

  // ✅ Upload code summaries
  const handleUploadSummaries = async () => {
    setStatus({ loading: true, error: null, success: null });
    try {
      const response = await uploadProjectSummaries(projectId);
      setStatus({ loading: false, error: null, success: 'Summaries uploaded successfully!' });
      console.log('Upload response:', response.data);
    } catch (error) {
      setStatus({
        loading: false,
        error: error.response?.data?.detail || 'Failed to upload summaries.',
        success: null,
      });
    }
  };

  // ✅ Generate project documentation
  const handleGenerateDocs = async () => {
    if (!projectName) {
      setStatus({ loading: false, error: 'Please enter a project name.', success: null });
      return;
    }

    setStatus({ loading: true, error: null, success: null });
    try {
      const response = await generateDocumentation(projectId, projectName);
      setStatus({ loading: false, error: null, success: 'Documentation generated successfully!' });
      console.log('Generate docs response:', response.data);
    } catch (error) {
      setStatus({
        loading: false,
        error: error.response?.data?.detail || 'Failed to generate documentation.',
        success: null,
      });
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-900 text-white">
      <div className="w-full max-w-md rounded-lg bg-gray-800 p-8 shadow-lg">
        <h1 className="mb-6 text-center text-3xl font-bold text-cyan-400">
          Project Actions
        </h1>

        {/* Directory Input */}
        <div className="mb-4">
          <label htmlFor="dirPath" className="mb-2 block text-sm font-medium text-gray-300">
            Project Directory Path
          </label>
          <input
            id="dirPath"
            type="text"
            value={dirPath}
            onChange={(e) => setDirPath(e.target.value)}
            placeholder="e.g., C:\\Users\\You\\Projects\\MyCodebase"
            className="w-full rounded-md border-gray-600 bg-gray-700 p-3 text-white placeholder-gray-500 focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
            disabled={status.loading}
          />
        </div>

        {/* Project Name Input for Documentation */}
        <div className="mb-4">
          <label htmlFor="projectName" className="mb-2 block text-sm font-medium text-gray-300">
            Project Name (for Documentation)
          </label>
          <input
            id="projectName"
            type="text"
            value={projectName}
            onChange={(e) => setProjectName(e.target.value)}
            placeholder="e.g., My Awesome Project"
            className="w-full rounded-md border-gray-600 bg-gray-700 p-3 text-white placeholder-gray-500 focus:border-cyan-500 focus:ring focus:ring-cyan-500 focus:ring-opacity-50"
            disabled={status.loading}
          />
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col space-y-3">
          <button
            onClick={handleIngest}
            disabled={status.loading}
            className="w-full rounded-md bg-cyan-600 py-3 font-semibold text-white transition-colors hover:bg-cyan-700 disabled:cursor-not-allowed disabled:bg-gray-600"
          >
            {status.loading ? 'Processing...' : 'Ingest Code'}
          </button>

          <button
            onClick={handleUploadSummaries}
            disabled={status.loading}
            className="w-full rounded-md bg-purple-600 py-3 font-semibold text-white transition-colors hover:bg-purple-700 disabled:cursor-not-allowed disabled:bg-gray-600"
          >
            {status.loading ? 'Processing...' : 'Upload Summaries'}
          </button>

          <button
            onClick={handleGenerateDocs}
            disabled={status.loading}
            className="w-full rounded-md bg-green-600 py-3 font-semibold text-white transition-colors hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-gray-600"
          >
            {status.loading ? 'Processing...' : 'Generate Documentation'}
          </button>
        </div>

        {/* Status Messages */}
        <div className="mt-6 h-6 text-center">
          {status.error && <p className="text-sm text-red-400">{status.error}</p>}
          {status.success && <p className="text-sm text-green-400">{status.success}</p>}
        </div>
      </div>
    </div>
  );
}

export default IngestPage;
