import { create } from 'zustand'
import { CompilationResult } from '@/types'
import { compilerAPI } from '@/services/api'

interface CompilerStore {
  currentCompilation: CompilationResult | null
  loading: boolean
  error: string | null
  compilations: CompilationResult[]

  generateConfiguration: (prompt: string) => Promise<void>
  getCompilation: (id: string) => Promise<void>
  listCompilations: (limit?: number) => Promise<void>
  clearError: () => void
  reset: () => void
}

export const useCompilerStore = create<CompilerStore>((set) => ({
  currentCompilation: null,
  loading: false,
  error: null,
  compilations: [],

  generateConfiguration: async (prompt: string) => {
    set({ loading: true, error: null })
    try {
      const result = await compilerAPI.generate(prompt)
      set({ currentCompilation: result, loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
    }
  },

  getCompilation: async (id: string) => {
    set({ loading: true, error: null })
    try {
      const result = await compilerAPI.getCompilation(id)
      set({ currentCompilation: result, loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
    }
  },

  listCompilations: async (limit: number = 10) => {
    set({ loading: true, error: null })
    try {
      const response = await compilerAPI.listCompilations(limit)
      set({ compilations: response.items || [], loading: false })
    } catch (error: any) {
      set({ error: error.message, loading: false })
    }
  },

  clearError: () => set({ error: null }),
  reset: () => set({ currentCompilation: null, compilations: [], error: null }),
}))
