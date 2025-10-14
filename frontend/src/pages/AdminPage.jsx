// pages/AdminPage.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';

const AdminPage = () => {
  const { token } = useAuth();
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ username: '', password: '' });
  const [error, setError] = useState('');

  const fetchUsers = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8001/api/admin/users', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(res.data);
    } catch (err) {
      setError('Failed to fetch users');
    }
  };

  const addUser = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8001/api/admin/users', newUser, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setNewUser({ username: '', password: '' });
      fetchUsers();
    } catch {
      setError('Failed to add user');
    }
  };

  const deleteUser = async (userId) => {
    try {
      await axios.delete(`http://127.0.0.1:8001/api/admin/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchUsers();
    } catch {
      setError('Failed to delete user');
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Admin Dashboard</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <form onSubmit={addUser} className="flex gap-4 mb-6">
        <input
          type="text"
          placeholder="Username"
          value={newUser.username}
          onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
          className="border px-3 py-2 rounded"
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={newUser.password}
          onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
          className="border px-3 py-2 rounded"
          required
        />
        <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
          Add User
        </button>
      </form>

      <ul className="space-y-2">
        {users.map((u) => (
          <li key={u.id} className="flex justify-between items-center bg-gray-100 p-3 rounded">
            <span>{u.username}</span>
            <button
              onClick={() => deleteUser(u.id)}
              className="text-white bg-red-500 px-3 py-1 rounded hover:bg-red-600"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AdminPage;
