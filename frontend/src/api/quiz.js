import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const quizAPI = {
  // Generate a new quiz from Wikipedia URL
  generateQuiz: async (url, forceRegenerate = false) => {
    const response = await api.post('/api/generate-quiz', {
      url,
      force_regenerate: forceRegenerate,
    });
    return response.data;
  },

  // Get all quizzes (history)
  getAllQuizzes: async () => {
    const response = await api.get('/api/quizzes');
    return response.data;
  },

  // Get a specific quiz by ID
  getQuizById: async (id) => {
    const response = await api.get(`/api/quizzes/${id}`);
    return response.data;
  },

  // Delete a quiz
  deleteQuiz: async (id) => {
    const response = await api.delete(`/api/quizzes/${id}`);
    return response.data;
  },
};

export default api;
