// import React from 'react';

// const StatusBadge = ({ status }) => {
//   const statusStyles = {
//     success: 'bg-green-100 text-green-800',
//     pending: 'bg-yellow-100 text-yellow-800',
//     failed: 'bg-red-100 text-red-800',
//   };

//   return (
//     <span className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyles[status] || 'bg-gray-100 text-gray-800'}`}>
//       {status}
//     </span>
//   );
// };

// const ProjectCard = ({ project }) => {
//   return (
//     <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
//       <div className="p-6">
//         <div className="flex justify-between items-start mb-2">
//           <h3 className="text-xl font-bold text-gray-800">{project.name}</h3>
//           <StatusBadge status={project.status} />
//         </div>
//         <p className="text-gray-600 text-sm mb-4 h-10">
//           {project.description || 'No description provided.'}
//         </p>
//         <div className="flex justify-end">
//           <button className="text-sm font-semibold text-blue-500 hover:text-blue-700 transition-colors">
//             Open Project
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// };

// export default ProjectCard;


import React from 'react';
import { useNavigate } from 'react-router-dom';

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
  const navigate = useNavigate();

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
      <div className="p-6">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-gray-800">{project.name}</h3>
          <StatusBadge status={project.status} />
        </div>
        <p className="text-gray-600 text-sm mb-4 h-10">
          {project.description || 'No description provided.'}
        </p>
        <div className="flex justify-end">
          <button
            onClick={() => navigate(`/projects/${project.id}`)}
            className="text-sm font-semibold text-blue-500 hover:text-blue-700 transition-colors"
          >
            Open Project
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;
