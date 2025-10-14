import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { viewDocumentation, downloadDocumentation } from '../api/apiClient';

const DocumentationPage = () => {
  const { projectId } = useParams();
  const [docHTML, setDocHTML] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDocs = async () => {
      try {
        const response = await viewDocumentation(projectId);

        // ✅ Extract the HTML content from the response
        if (response.data && response.data.content) {
          setDocHTML(response.data.content);
        } else {
          setError('No documentation found. Please generate it first.');
        }
      } catch (err) {
        setError('Failed to fetch documentation. Please generate it first.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchDocs();
  }, [projectId]);

  const handleDownload = () => {
    const projectName = `project_${projectId}`;
    downloadDocumentation(projectId, projectName);
  };

  if (loading) {
    return (
      <div className="text-center p-10 text-gray-700">
        Loading documentation...
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-10 text-red-500">
        <p>{error}</p>
        <Link
          to="/"
          className="text-blue-500 hover:underline mt-4 inline-block"
        >
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-4 sm:p-6">
      <div className="bg-white p-6 sm:p-8 rounded-lg shadow-lg">
        <div className="flex justify-between items-center mb-6 border-b pb-4">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">
            Project Documentation
          </h1>
          <button
            onClick={handleDownload}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-500 rounded-md hover:bg-indigo-600"
          >
            Download
          </button>
        </div>

        {/* ✅ Render full HTML safely */}
        <div
          className="prose max-w-none"
          dangerouslySetInnerHTML={{ __html: docHTML }}
        />
      </div>
    </div>
  );
};

export default DocumentationPage;
