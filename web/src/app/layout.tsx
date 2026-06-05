'use client'

import React from 'react'
import Nav from '../components/Nav'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head />
      <body className="min-h-screen bg-gray-50 text-gray-800">
        <div className="flex h-screen">
          <Nav />
          <main className="flex-1 overflow-auto p-8">{children}</main>
        </div>
      </body>
    </html>
  )
}
