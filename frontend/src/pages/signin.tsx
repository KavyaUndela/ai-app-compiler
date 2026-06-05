'use client'

import Link from 'next/link'
import { FormEvent, useState } from 'react'
import { useRouter } from 'next/router'
import { authAPI } from '@/services/api'
import { useAuthStore } from '@/stores/authStore'

export default function SignInPage() {
  const router = useRouter()
  const { setUser, setToken, setLoading, setError } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [localError, setLocalError] = useState('')

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setIsLoading(true)
    setLocalError('')

    try {
      const response = await authAPI.signin(email, password)
      setUser(response.user)
      setToken(response.token)
      
      // Redirect to compiler
      router.push('/compiler')
    } catch (error: any) {
      setLocalError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 pb-16 pt-24 text-slate-100">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-2xl rounded-[2rem] bg-slate-900/90 p-10 shadow-2xl shadow-slate-950/40">
          <div className="mb-8">
            <h1 className="text-4xl font-semibold">Sign in</h1>
            <p className="mt-3 text-slate-400">Access your account and continue where you left off.</p>
          </div>

          {localError && (
            <div className="mb-6 rounded-2xl bg-red-500/10 p-4 text-red-300">
              {localError}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-300">
                Email address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
                disabled={isLoading}
                className="mt-3 w-full rounded-3xl border border-slate-700 bg-slate-950/80 px-4 py-4 text-slate-100 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 disabled:opacity-50"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-slate-300">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
                disabled={isLoading}
                className="mt-3 w-full rounded-3xl border border-slate-700 bg-slate-950/80 px-4 py-4 text-slate-100 outline-none transition focus:border-cyan-400 focus:ring-2 focus:ring-cyan-400/20 disabled:opacity-50"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full rounded-full bg-cyan-500 px-5 py-4 text-base font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-8 flex flex-col gap-4 text-sm text-slate-400 sm:flex-row sm:items-center sm:justify-between">
            <p>Don't have an account?</p>
            <Link href="/signup" className="font-semibold text-cyan-300 hover:text-cyan-200">
              Create an account
            </Link>
          </div>

          <p className="mt-8 text-sm text-slate-500">
            Try: test@example.com / password123
          </p>
        </div>
      </div>
    </div>
  )
}
