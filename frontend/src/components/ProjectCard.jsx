import React from 'react';
import { useNavigate , Link} from 'react-router-dom';

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
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 flex flex-col justify-between">
      <div className="p-6">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-gray-800">{project.name}</h3>
          {/* We keep the StatusBadge from the old design */}
          <StatusBadge status={project.status} />
        </div>
        <p className="text-gray-600 text-sm mb-4 h-10 overflow-hidden">
          {project.description || 'No description provided.'}
        </p>
      </div>
      {/* We add the new buttons in the footer of the card */}
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
      </div>
    </div>
  );
};

export default ProjectCard;