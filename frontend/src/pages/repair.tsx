'use client'

import Layout from '@/components/Layout'
import { useCompilerStore } from '@/store/compilerStore'
import Link from 'next/link'

export default function RepairPage() {
  const { currentCompilation } = useCompilerStore()

  if (!currentCompilation) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No repair data. Please generate a configuration first.</p>
          <Link href="/" className="btn-primary">
            Generate Configuration →
          </Link>
        </div>
      </Layout>
    )
  }

  const { repair } = currentCompilation

  if (!repair) {
    return (
      <Layout>
        <div className="max-w-4xl">
          <h1 className="text-3xl font-bold mb-8">Repair Engine</h1>
          <div className="card bg-green-50 border-l-4 border-green-500 p-8 text-center">
            <div className="text-4xl mb-2">✓</div>
            <h2 className="text-xl font-bold text-green-800 mb-2">No Repairs Needed</h2>
            <p className="text-green-700">The generated schema passed all validations and requires no repairs.</p>
          </div>
        </div>
      </Layout>
    )
  }

  return (
    <Layout>
      <div className="max-w-4xl">
        <h1 className="text-3xl font-bold mb-2">Repair Engine</h1>
        <p className="text-gray-600 mb-8">{repair.summary}</p>

        {/* Repair Summary */}
        <div className="card mb-8">
          <h2 className="text-lg font-bold mb-4">Repair Summary</h2>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{repair.patches.length}</div>
              <div className="text-sm text-gray-600">Total Patches</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {repair.patches.filter(p => p.confidence > 0.9).length}
              </div>
              <div className="text-sm text-gray-600">High Confidence</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">
                {repair.patches.filter(p => p.confidence <= 0.9).length}
              </div>
              <div className="text-sm text-gray-600">Standard</div>
            </div>
          </div>
        </div>

        {/* Patches */}
        <div className="space-y-4">
          {repair.patches.map((patch, idx) => (
            <div key={idx} className="card border-l-4 border-blue-500">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-lg">Patch {idx + 1}</h3>
                <div className="flex gap-2">
                  <span className={`text-xs px-2 py-1 rounded font-bold ${
                    patch.confidence > 0.9
                      ? 'bg-green-200 text-green-800'
                      : 'bg-yellow-200 text-yellow-800'
                  }`}>
                    {(patch.confidence * 100).toFixed(0)}% Confidence
                  </span>
                  <span className="text-xs bg-gray-200 text-gray-800 px-2 py-1 rounded">
                    {patch.affected_component}
                  </span>
                </div>
              </div>

              <p className="text-gray-700 mb-3">{patch.explanation}</p>

              <div className="bg-gray-50 p-3 rounded mb-3 space-y-2">
                <div className="flex gap-2 items-center">
                  <span className="text-red-600 font-mono">-</span>
                  <code className="text-sm text-red-600 break-all">{JSON.stringify(patch.original_value)}</code>
                </div>
                <div className="flex gap-2 items-center">
                  <span className="text-green-600 font-mono">+</span>
                  <code className="text-sm text-green-600 break-all">{JSON.stringify(patch.fixed_value)}</code>
                </div>
              </div>

              <button className="btn-primary text-sm">
                Apply Patch
              </button>
            </div>
          ))}
        </div>

        {/* Repaired Schema Status */}
        {repair.repaired_schema && (
          <div className="card mt-8 bg-green-50 border-l-4 border-green-500">
            <h2 className="font-bold text-green-800 mb-2">✓ All Repairs Applied</h2>
            <p className="text-green-700">The schema has been successfully repaired and is ready for deployment.</p>
          </div>
        )}
      </div>
    </Layout>
  )
}
