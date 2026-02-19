// API Configuration
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

export const API_ENDPOINTS = {
  base: API_BASE_URL,
  auth: `${API_BASE_URL}/api/auth`,
  api: `${API_BASE_URL}/api`,
}

export default API_ENDPOINTS
