'use client';

import React from 'react';
import Link from 'next/link';

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>AI Application Compiler</title>
        <meta name="description" content="Convert requirements into executable configurations" />
      </head>
      <body className="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
        <nav className="bg-white shadow-sm">
          <div className="container mx-auto px-4 py-4 flex justify-between items-center">
            <Link href="/" className="text-2xl font-bold text-blue-600">
              AI Compiler
            </Link>
            <div className="flex gap-6">
              <Link href="/" className="text-gray-700 hover:text-blue-600">
                Home
              </Link>
              <Link href="/compiler" className="text-gray-700 hover:text-blue-600">
                Compiler
              </Link>
              <Link href="/dashboard" className="text-gray-700 hover:text-blue-600">
                Dashboard
              </Link>
            </div>
          </div>
        </nav>

        <main className="container mx-auto px-4 py-8">
          {children}
        </main>

        <footer className="bg-white border-t border-gray-200 mt-12 py-6 text-center text-gray-600">
          <p>AI Application Compiler © 2024 | Localhost Development Version</p>
        </footer>
      </body>
    </html>
  );
}
