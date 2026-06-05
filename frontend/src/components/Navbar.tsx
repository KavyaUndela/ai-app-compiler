'use client'

import Link from 'next/link'
import { useRouter } from 'next/router'
import { useAuthStore } from '@/stores/authStore'
import { useEffect } from 'react'

export default function Navbar() {
  const router = useRouter()
  const { user, token, logout } = useAuthStore()

  useEffect(() => {
    // Debug: log auth state to help diagnose UI not updating after login
    try {
      // eslint-disable-next-line no-console
      console.debug('[Navbar] auth state', { user, token })
    } catch (e) {
      // ignore
    }
  }, [user, token])

  const handleLogout = () => {
    logout()
    router.push('/')
  }

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-slate-900/10 bg-slate-950/95 backdrop-blur-xl text-white">
      <div className="container flex h-20 items-center justify-between">
        <Link href="/" className="flex items-center gap-3 font-semibold text-xl tracking-tight">
          <span className="inline-flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-400/15 text-cyan-300 shadow-lg shadow-cyan-500/10">AI</span>
          <span>AI Compiler</span>
        </Link>

        <div className="flex items-center gap-4 text-sm md:text-base">
          <div className="hidden md:flex items-center gap-6 text-slate-200">
            <Link href="/" className="hover:text-white transition">Home</Link>
            <Link href="/compiler" className="hover:text-white transition">Compiler</Link>
            <Link href="/pipeline" className="hover:text-white transition">Pipeline</Link>
            <Link href="/validation" className="hover:text-white transition">Validation</Link>
            <Link href="/repair" className="hover:text-white transition">Repair</Link>
            <Link href="/runtime" className="hover:text-white transition">Runtime</Link>
            <Link href="/recent" className="hover:text-white transition">Recent</Link>
          </div>
          <div className="flex items-center gap-3">
            {user && token ? (
              <>
                <div className="flex items-center gap-2 text-sm">
                  <span className="text-slate-300">Welcome, {user.name}</span>
                </div>
                <button
                  onClick={handleLogout}
                  className="rounded-full border border-slate-700 bg-slate-900/80 px-4 py-2 text-sm text-slate-200 transition hover:bg-slate-800"
                >
                  Sign out
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/signin"
                  className="rounded-full border border-slate-700 bg-slate-900/80 px-4 py-2 text-sm text-slate-200 transition hover:bg-slate-800"
                >
                  Sign in
                </Link>
                <Link
                  href="/signup"
                  className="rounded-full bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400"
                >
                  Sign up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
