// src/App.jsx

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';

// Import your components
import Navbar from './components/Navbar.jsx';
import IngestPage from './pages/IngestPage.jsx';
import QueryPage from './pages/QueryPage.jsx';
import Footer from './components/Footer.jsx'; // Import the new Footer

// A simple placeholder for the Home page
const HomePage = () => (
  <div className="flex h-[calc(100vh-8rem)] items-center justify-center bg-gray-900 text-white">
    <div className="text-center">
      <h1 className="text-5xl font-bold">Welcome to Code Intelligence</h1>
      <p className="mt-4 text-xl text-gray-400">Your AI-powered codebase assistant.</p>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="flex min-h-screen flex-col">
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: '#334155', // bg-slate-700
              color: '#fff',
            },
          }}
        />
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/ingest" element={<IngestPage />} />
            <Route path="/query" element={<QueryPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;