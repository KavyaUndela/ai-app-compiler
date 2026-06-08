import axios from 'axios'
import { CompilationResult } from '@/types'

// Prefer an explicit API URL when provided. If not set, always use the
// deployed backend host (no localhost fallback).
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'https://ai-app-compiler-7-lxn4.onrender.com'

// Log API configuration in development
if (typeof window !== 'undefined') {
  console.log('API Configuration:', {
    API_URL: API_URL,
    ENV_SET: !!process.env.NEXT_PUBLIC_API_URL,
    ENVIRONMENT: process.env.NODE_ENV,
  })
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor for logging
api.interceptors.request.use(
  (config) => {
    const fullUrl = config.baseURL ? `${config.baseURL}${config.url}` : config.url
    console.log('API Request:', {
      method: config.method?.toUpperCase(),
      url: fullUrl,
      data: config.data,
      timestamp: new Date().toISOString(),
    })
    return config
  },
  (error) => {
    console.error('API Request Error:', error)
    return Promise.reject(error)
  }
)

// Add response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', {
      status: response.status,
      url: response.config.url,
      data: response.data,
      timestamp: new Date().toISOString(),
    })
    return response
  },
  (error) => {
    console.error('API Response Error:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      url: error.config?.url,
      baseURL: error.config?.baseURL,
      data: error.response?.data,
      message: error.message,
      code: error.code,
      timestamp: new Date().toISOString(),
    })
    return Promise.reject(error)
  }
)

export const authAPI = {
  async signup(name: string, email: string, password: string) {
    try {
      const response = await api.post('/auth/signup', { name, email, password })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || `Sign up failed: ${error.message}`)
    }
  },

  async signin(email: string, password: string) {
    try {
      const response = await api.post('/auth/signin', { email, password })
      return response.data
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || `Sign in failed: ${error.message}`)
    }
  },

  async logout(token: string) {
    try {
      const response = await api.post('/auth/logout', null, {
        params: { token }
      })
      return response.data
    } catch (error: any) {
      throw new Error(`Logout failed: ${error.message}`)
    }
  },

  async getCurrentUser(token: string) {
    try {
      const response = await api.get('/auth/me', {
        params: { token }
      })
      return response.data
    } catch (error: any) {
      throw new Error(`Failed to fetch user: ${error.message}`)
    }
  },
}

export const compilerAPI = {
  async generate(prompt: string): Promise<CompilationResult> {
    try {
      const endpoint = '/api/generate'
      const fullUrl = `${API_URL}${endpoint}`
      console.log('Generating configuration:', {
        prompt,
        endpoint,
        fullUrl,
      })
      const response = await api.post<CompilationResult>(endpoint, { prompt })
      return response.data
    } catch (error: any) {
      const detailedError = `Failed to generate configuration: ${error.message}. API URL: ${API_URL}. Response: ${error.response?.data?.detail || 'No response'}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async getCompilation(id: string): Promise<CompilationResult> {
    try {
      const response = await api.get<CompilationResult>(`/api/compilations/${id}`)
      return response.data
    } catch (error: any) {
      const detailedError = `Failed to fetch compilation: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async listCompilations(limit: number = 10) {
    try {
      const response = await api.get('/api/compilations', { params: { limit } })
      return response.data
    } catch (error: any) {
      const detailedError = `Failed to list compilations: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async health() {
    try {
      const response = await api.get('/api/health')
      return response.data
    } catch (error: any) {
      const detailedError = `Health check failed: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async validate(schema: any) {
    try {
      const response = await api.post('/api/validate', schema)
      return response.data
    } catch (error: any) {
      const detailedError = `Validation failed: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async repair(data: any) {
    try {
      const response = await api.post('/api/repair', data)
      return response.data
    } catch (error: any) {
      const detailedError = `Repair failed: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },

  async getRuntimePreview(schema: any) {
    try {
      const response = await api.post('/api/runtime-preview', schema)
      return response.data
    } catch (error: any) {
      const detailedError = `Failed to generate preview: ${error.message}. API URL: ${API_URL}`
      console.error(detailedError)
      throw new Error(detailedError)
    }
  },
}

export default api
