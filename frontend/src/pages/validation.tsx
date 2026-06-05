'use client'

import Layout from '@/components/Layout'
import { useCompilerStore } from '@/store/compilerStore'
import Link from 'next/link'

export default function ValidationPage() {
  const { currentCompilation } = useCompilerStore()

  if (!currentCompilation) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No validation data. Please generate a configuration first.</p>
          <Link href="/" className="btn-primary">
            Generate Configuration →
          </Link>
        </div>
      </Layout>
    )
  }

  const { validation } = currentCompilation
  const errors = validation.issues.filter(i => i.severity === 'error')
  const warnings = validation.issues.filter(i => i.severity === 'warning')

  return (
    <Layout>
      <div className="max-w-4xl">
        <h1 className="text-3xl font-bold mb-2">Validation Report</h1>
        <p className="text-gray-600 mb-8">{validation.summary}</p>

        {/* Status */}
        <div className={`card mb-8 ${
          validation.is_valid ? 'bg-green-50 border-l-4 border-green-500' : 'bg-red-50 border-l-4 border-red-500'
        }`}>
          <h2 className="text-xl font-bold mb-2">
            {validation.is_valid ? '✓ Validation Passed' : '✗ Validation Failed'}
          </h2>
          <p className={`${validation.is_valid ? 'text-green-700' : 'text-red-700'}`}>
            {errors.length} errors, {warnings.length} warnings
          </p>
        </div>

        {/* Errors */}
        {errors.length > 0 && (
          <div className="card mb-6">
            <h2 className="text-lg font-bold text-red-700 mb-4">🚨 Errors ({errors.length})</h2>
            <div className="space-y-3">
              {errors.map((issue, idx) => (
                <div key={idx} className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-red-900">{issue.category}</h3>
                    <span className="text-xs bg-red-200 text-red-800 px-2 py-1 rounded">{issue.affected_component}</span>
                  </div>
                  <p className="text-red-800 mb-2">{issue.message}</p>
                  {issue.suggestion && (
                    <p className="text-sm text-red-700 bg-red-100 p-2 rounded">
                      💡 Suggestion: {issue.suggestion}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Warnings */}
        {warnings.length > 0 && (
          <div className="card mb-6">
            <h2 className="text-lg font-bold text-yellow-700 mb-4">⚠️ Warnings ({warnings.length})</h2>
            <div className="space-y-3">
              {warnings.map((issue, idx) => (
                <div key={idx} className="bg-yellow-50 border-l-4 border-yellow-500 p-4 rounded">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-yellow-900">{issue.category}</h3>
                    <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-1 rounded">{issue.affected_component}</span>
                  </div>
                  <p className="text-yellow-800 mb-2">{issue.message}</p>
                  {issue.suggestion && (
                    <p className="text-sm text-yellow-700 bg-yellow-100 p-2 rounded">
                      💡 Suggestion: {issue.suggestion}
                    </p>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* No Issues */}
        {validation.issues.length === 0 && (
          <div className="card bg-green-50 border-l-4 border-green-500 text-center py-12">
            <div className="text-4xl mb-2">✓</div>
            <p className="text-green-700 font-bold">All checks passed! No issues found.</p>
          </div>
        )}

        {/* Validation ID */}
        <div className="card mt-6 text-sm text-gray-600">
          <p>Validation ID: <span className="font-mono">{validation.validation_id}</span></p>
          <p>Schema ID: <span className="font-mono">{validation.schema_id}</span></p>
        </div>
      </div>
    </Layout>
  )
}
