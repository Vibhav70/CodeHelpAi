import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ingestProjectDirectory,
  uploadProjectSummaries,
  generateDocumentation,
} from '../api/apiClient';

const StatusBadge = ({ status }) => {
  const statusStyles = {
    success: 'bg-green-100 text-green-800',
    pending: 'bg-yellow-100 text-yellow-800',
    failed: 'bg-red-100 text-red-800',
  };

  return (
    <span
      className={`px-2 py-1 text-xs font-semibold rounded-full ${
        statusStyles[status] || 'bg-gray-100 text-gray-800'
      }`}
    >
      {status}
    </span>
  );
};

const ProjectCard = ({ project }) => {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // ✅ Handle Ingest Code
  const handleIngest = async () => {
    const dir = prompt('Enter directory path to ingest:');
    if (!dir) return;
    setLoading(true);
    setMessage('');
    try {
      await ingestProjectDirectory(project.id, dir);
      setMessage('✅ Ingestion completed successfully!');
    } catch (error) {
      console.error(error);
      setMessage('❌ Failed to ingest code.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 4000);
    }
  };

  // ✅ Handle Upload Summaries
  const handleUploadSummaries = async () => {
    setLoading(true);
    setMessage('');
    try {
      await uploadProjectSummaries(project.id);
      setMessage('✅ Summaries uploaded successfully!');
    } catch (error) {
      console.error(error);
      setMessage('❌ Failed to upload summaries.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 4000);
    }
  };

  // ✅ Handle Generate Documentation
  const handleGenerateDocs = async () => {
    const name = prompt('Enter project name for documentation:');
    if (!name) return;
    setLoading(true);
    setMessage('');
    try {
      await generateDocumentation(project.id, name);
      setMessage('✅ Documentation generated successfully!');
    } catch (error) {
      console.error(error);
      setMessage('❌ Failed to generate documentation.');
    } finally {
      setLoading(false);
      setTimeout(() => setMessage(''), 4000);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 flex flex-col justify-between">
      {/* Card Header */}
      <div className="p-6">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-gray-800">{project.name}</h3>
          <StatusBadge status={project.status} />
        </div>
        <p className="text-gray-600 text-sm mb-4 h-10 overflow-hidden">
          {project.description || 'No description provided.'}
        </p>
      </div>

      {/* Action Buttons */}
      <div className="px-6 py-4 bg-gray-50 border-t flex flex-wrap justify-end gap-2">
        <Link
          to={`/projects/${project.id}`}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-500 rounded-md hover:bg-blue-600 transition-colors"
        >
          Open Chat
        </Link>

        <Link
          to={`/project/${project.id}/docs`}
          className="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-md hover:bg-green-600 transition-colors"
        >
          View Docs
        </Link>

        <button
          onClick={handleIngest}
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-white bg-cyan-500 rounded-md hover:bg-cyan-600 transition-colors disabled:bg-gray-400"
        >
          {loading ? '...' : 'Ingest'}
        </button>

        <button
          onClick={handleUploadSummaries}
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-white bg-purple-500 rounded-md hover:bg-purple-600 transition-colors disabled:bg-gray-400"
        >
          {loading ? '...' : 'Upload Summaries'}
        </button>

        <button
          onClick={handleGenerateDocs}
          disabled={loading}
          className="px-4 py-2 text-sm font-medium text-white bg-amber-500 rounded-md hover:bg-amber-600 transition-colors disabled:bg-gray-400"
        >
          {loading ? '...' : 'Generate Docs'}
        </button>
      </div>

      {/* Status Message */}
      {message && (
        <div className="px-6 py-2 bg-gray-50 border-t text-center text-sm text-gray-700">
          {message}
        </div>
      )}
    </div>
  );
};

export default ProjectCard;
