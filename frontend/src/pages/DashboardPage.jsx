import React, { useState, useEffect } from 'react';
import { getProjects, createProject } from '../api/apiClient';
import ProjectCard from '../components/ProjectCard';
import CreateProjectModal from '../components/CreateProjectModal';

const DashboardPage = () => {
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        const response = await getProjects();
        // Add a mock status to each project for UI purposes
        const projectsWithStatus = response.data.map(p => ({ ...p, status: 'success' }));
        setProjects(projectsWithStatus);
      } catch (err) {
        setError('Failed to fetch projects. Please try again later.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const handleCreateProject = async (name, description) => {
    try {
      const response = await createProject(name, description);
      const newProject = { ...response.data, status: 'pending' }; // New projects start as pending
      setProjects([...projects, newProject]);
      setIsModalOpen(false);
    } catch (err) {
      console.error("Failed to create project:", err);
      // You could set a specific modal error state here
    }
  };

  if (isLoading) {
    return <div className="text-center p-8">Loading projects...</div>;
  }

  if (error) {
    return <div className="text-center p-8 text-red-500">{error}</div>;
  }

  return (
    <div className="container mx-auto p-4 md:p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-800">Projects</h1>
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-500 text-white font-semibold px-4 py-2 rounded-lg shadow-md hover:bg-blue-600 transition-colors"
        >
          Create New Project
        </button>
      </div>

      {projects.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      ) : (
        <div className="text-center py-16 px-6 bg-gray-50 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-700">No projects yet!</h2>
          <p className="text-gray-500 mt-2">Click "Create New Project" to get started.</p>
        </div>
      )}

      <CreateProjectModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateProject}
      />
    </div>
  );
};

export default DashboardPage;
