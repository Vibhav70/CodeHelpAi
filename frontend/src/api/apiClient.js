import axios from 'axios';

// --- API Configuration ---
// It's best practice to define your base URL in one place.
// Make sure this matches the address of your FastAPI backend.
const API_URL = 'http://127.0.0.1:8000/api';

const apiClient = axios.create({
  baseURL: API_URL,
});

// --- Authentication Endpoints ---

export const loginUser = (username, password) => {
  // The backend expects form data for the login endpoint
  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  return apiClient.post('/auth/login', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
};

// --- Project Endpoints ---
// We will add more functions here as we build out the app
export const getProjects = () => {
  // This will require an auth token
  const token = localStorage.getItem('authToken');
  return apiClient.get('/projects', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const createProject = (name, description) => {
  const token = localStorage.getItem('authToken');
  return apiClient.post('/projects', { name, description }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};


// --- Project Actions (Ingestion & Chat) ---
export const getProjectHistory = (projectId) => {
  const token = localStorage.getItem('authToken');
  return apiClient.get(`/projects/${projectId}/history`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export const askQuestion = (projectId, question) => {
    // The backend expects a 'question' and an empty 'answer' in the body
    // return apiClient.post(`/projects/${projectId}/ask`, { question, answer: "" }, { headers: getAuthHeaders() });
  const token = localStorage.getItem('authToken');
  return apiClient.post(`api/projects/${projectId}/ask`,{ question, answer: "" }, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};

export default apiClient;

