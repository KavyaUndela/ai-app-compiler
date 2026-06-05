'use client'

import Layout from '@/components/Layout'
import { useCompilerStore } from '@/store/compilerStore'
import Link from 'next/link'
import { useEffect } from 'react'

export default function RecentPage() {
  const { compilations, listCompilations, getCompilation } = useCompilerStore()

  useEffect(() => {
    listCompilations(20)
  }, [])

  return (
    <Layout>
      <div className="max-w-4xl">
        <h1 className="text-3xl font-bold mb-8">Recent Compilations</h1>

        {compilations.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-600 mb-4">No compilations yet</p>
            <Link href="/" className="btn-primary">
              Create One →
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {compilations.map((compilation, idx) => (
              <div
                key={idx}
                className="card cursor-pointer hover:shadow-lg transition"
                onClick={() => getCompilation(compilation.compilation_id)}
              >
                <div className="flex justify-between items-start mb-2">
                  <h2 className="text-lg font-bold flex-1">{compilation.original_prompt}</h2>
                  <span className={`px-2 py-1 rounded text-xs font-bold ${
                    compilation.status === 'completed'
                      ? 'bg-green-200 text-green-800'
                      : compilation.status === 'partial'
                      ? 'bg-yellow-200 text-yellow-800'
                      : 'bg-red-200 text-red-800'
                  }`}>
                    {compilation.status.toUpperCase()}
                  </span>
                </div>
                <p className="text-gray-600 text-sm mb-3">
                  {compilation.design.modules.length} modules • {compilation.schema.api_schema.length} endpoints
                </p>
                <Link href="/pipeline" className="text-blue-600 hover:underline text-sm">
                  View Details →
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
