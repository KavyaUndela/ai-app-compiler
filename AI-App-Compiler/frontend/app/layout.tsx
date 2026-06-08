import './styles/globals.css'
import React from 'react'

export const metadata = {
  title: 'AI-App-Compiler',
  description: 'AI Application Compiler — Dashboard',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          <header className="border-b py-4">
            <div className="container flex items-center justify-between">
              <h1 className="text-lg font-semibold">AI-App-Compiler</h1>
              <nav className="space-x-4 text-sm">
                <a href="/" className="hover:underline">Home</a>
                <a href="/pipeline" className="hover:underline">Pipeline</a>
                <a href="/metrics" className="hover:underline">Metrics</a>
              </nav>
            </div>
          </header>
          <main className="container py-8">{children}</main>
        </div>
      </body>
    </html>
  )
}
