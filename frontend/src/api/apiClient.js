import axios from 'axios';

// --- API Configuration ---
const API_URL = 'http://127.0.0.1:8001/api';

const apiClient = axios.create({
  baseURL: API_URL,
});

// --- Authentication Endpoints ---
export const loginUser = (username, password) => {
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  return apiClient.post('/auth/login', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
};

// --- Project Endpoints ---
export const getProjects = () => {
  const token = localStorage.getItem('authToken');
  return apiClient.get('/projects', {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const createProject = (name, description) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post(
    '/projects',
    { name, description },
    { headers: { Authorization: `Bearer ${token}` } }
  );
};

// --- Project Actions (Ingestion & Chat) ---
export const getProjectHistory = (projectId) => {
  const token = localStorage.getItem('authToken');
  return apiClient.get(`/projects/${projectId}/history`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const askQuestion = (projectId, question) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post(
    `/projects/${projectId}/ask`,
    { question, answer: '' },
    { headers: { Authorization: `Bearer ${token}` } }
  );
};

// ✅ --- NEW ENDPOINTS ---

// --- Project Utility Actions ---
// POST /api/projects/{project_id}/ingest
export const ingestProjectDirectory = (projectId, directoryPath) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post(
    `/projects/${projectId}/ingest`,
    { directory: directoryPath },
    { headers: { Authorization: `Bearer ${token}` } }
  );
};

// POST /api/projects/{project_id}/upload-summaries
export const uploadProjectSummaries = (projectId) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post(
    `/projects/${projectId}/upload-summaries`,
    {},
    { headers: { Authorization: `Bearer ${token}` } }
  );
};

// POST /api/projects/{project_id}/documentation/generate
export const generateDocumentation = (projectId, projectName) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post(
    `/projects/${projectId}/documentation/generate`,
    { project_name: projectName },
    { headers: { Authorization: `Bearer ${token}` } }
  );
};


// --- Documentation Endpoints ---
export const viewDocumentation = (projectId) => {
  const token = localStorage.getItem('authToken');
  return apiClient.get(`/projects/${projectId}/documentation/view`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const downloadDocumentation = async (projectId, projectName) => {
  const token = localStorage.getItem('authToken');
  const response = await apiClient.get(
    `/projects/${projectId}/documentation/download`,
    {
      headers: { Authorization: `Bearer ${token}` },
      responseType: 'blob',
    }
  );

  // Trigger the file download
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute(
    'download',
    `documentation_${projectName.replace(' ', '_')}.md`
  );
  document.body.appendChild(link);
  link.click();
  link.remove();
};

export default apiClient;
