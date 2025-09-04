// src/api/client.js

// The base URL for your FastAPI backend.
// In development, this will be proxied by Vite to avoid CORS issues.
const API_BASE_URL = "/api";

/**
 * A helper function to handle fetch requests, JSON parsing, and errors.
 * @param {string} endpoint - The API endpoint to call (e.g., '/ingest').
 * @param {object} options - The options for the fetch request (method, headers, body).
 * @returns {Promise<any>} - A promise that resolves with the JSON response.
 * @throws {Error} - Throws an error if the network response is not ok.
 */
async function fetchApi(endpoint, options) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

  if (!response.ok) {
    // Try to parse a JSON error message from the backend, otherwise use status text
    const errorData = await response.json().catch(() => null);
    const errorMessage = errorData?.detail || response.statusText;
    throw new Error(`API Error: ${errorMessage} (Status: ${response.status})`);
  }

  // Return the JSON body of the response
  return response.json();
}

/**
 * Sends a request to the backend to ingest a codebase directory.
 * @param {string} dirPath - The absolute path of the directory to ingest.
 * @returns {Promise<object>} - The JSON response from the server.
 */
export const ingestCode = (dirPath) => {
  return fetchApi("/ingest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ directory: dirPath }),
  });
};

/**
 * Sends a question to the backend and gets an LLM-generated answer.
 * @param {string} question - The user's question.
 * @returns {Promise<object>} - The JSON response containing the answer.
 */
export const askQuestion = (question) => {
  return fetchApi("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });
};
