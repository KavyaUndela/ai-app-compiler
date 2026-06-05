import axios from 'axios'
import { CompilationResult } from '@/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

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
      const response = await api.post<CompilationResult>('/generate', { prompt })
      return response.data
    } catch (error: any) {
      throw new Error(`Failed to generate configuration: ${error.message}`)
    }
  },

  async getCompilation(id: string): Promise<CompilationResult> {
    try {
      const response = await api.get<CompilationResult>(`/compilations/${id}`)
      return response.data
    } catch (error: any) {
      throw new Error(`Failed to fetch compilation: ${error.message}`)
    }
  },

  async listCompilations(limit: number = 10) {
    try {
      const response = await api.get('/compilations', { params: { limit } })
      return response.data
    } catch (error: any) {
      throw new Error(`Failed to list compilations: ${error.message}`)
    }
  },

  async health() {
    try {
      const response = await api.get('/health')
      return response.data
    } catch (error: any) {
      throw new Error(`Health check failed: ${error.message}`)
    }
  },

  async validate(schema: any) {
    try {
      const response = await api.post('/validate', schema)
      return response.data
    } catch (error: any) {
      throw new Error(`Validation failed: ${error.message}`)
    }
  },

  async repair(data: any) {
    try {
      const response = await api.post('/repair', data)
      return response.data
    } catch (error: any) {
      throw new Error(`Repair failed: ${error.message}`)
    }
  },

  async getRuntimePreview(schema: any) {
    try {
      const response = await api.post('/runtime-preview', schema)
      return response.data
    } catch (error: any) {
      throw new Error(`Failed to generate preview: ${error.message}`)
    }
  },
}

export default api
