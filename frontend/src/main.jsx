import './index.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import LoginPage from './pages/LoginPage';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);



// // Placeholder for your main dashboard/project page
// const Dashboard = () => <div className="p-8 text-center"><h1>Welcome to your Dashboard!</h1></div>;

// // A wrapper for routes that require authentication
// const PrivateRoute = ({ children }) => {
//   const { isAuthenticated } = useAuth();
//   return isAuthenticated ? children : <Navigate to="/login" />;
// };

// function App() {
//   return (
//     <AuthProvider>
//       <Router>
//         <Navbar />
//         <Routes>
//           <Route path="/login" element={<LoginPage />} />
//           <Route 
//             path="/" 
//             element={
//               <PrivateRoute>
//                 <Dashboard />
//               </PrivateRoute>
//             } 
//           />
//           {/* Add other routes for projects, admin panel etc. here */}
//         </Routes>
//       </Router>
//     </AuthProvider>
//   );
// }

// export default App;
