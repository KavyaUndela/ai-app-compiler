'use client'

import Layout from '@/components/Layout'
import JSONViewer from '@/components/JSONViewer'
import { useCompilerStore } from '@/store/compilerStore'
import Link from 'next/link'

export default function PipelinePage() {
  const { currentCompilation } = useCompilerStore()

  if (!currentCompilation) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No compilation data. Please generate a configuration first.</p>
          <Link href="/" className="btn-primary">
            Generate Configuration →
          </Link>
        </div>
      </Layout>
    )
  }

  const stages = [
    { name: 'Intent Extraction', complete: true, icon: '🗣️' },
    { name: 'System Design', complete: true, icon: '🏗️' },
    { name: 'Schema Generation', complete: true, icon: '📊' },
    { name: 'Validation', complete: currentCompilation.validation.is_valid, icon: '✓' },
    { name: 'Repair', complete: !currentCompilation.repair || currentCompilation.repair.patches.length === 0, icon: '🔧' },
    { name: 'Runtime Simulator', complete: true, icon: '▶️' }
  ]

  return (
    <Layout>
      <div className="max-w-6xl">
        <h1 className="text-3xl font-bold mb-2">Pipeline Execution</h1>
        <p className="text-gray-600 mb-8">All 6 stages completed for: {currentCompilation.original_prompt.substring(0, 60)}...</p>

        {/* Pipeline Stages */}
        <div className="space-y-4 mb-8">
          {stages.map((stage, index) => (
            <div
              key={index}
              className={`card flex items-center gap-4 ${
                stage.complete ? 'bg-green-50 border-l-4 border-green-500' : 'bg-yellow-50 border-l-4 border-yellow-500'
              }`}
            >
              <div className="text-3xl">{stage.icon}</div>
              <div className="flex-1">
                <h3 className="font-bold text-lg">{stage.name}</h3>
              </div>
              <div className={`px-3 py-1 rounded-full text-sm font-bold ${
                stage.complete
                  ? 'bg-green-200 text-green-800'
                  : 'bg-yellow-200 text-yellow-800'
              }`}>
                {stage.complete ? 'Complete' : 'Pending'}
              </div>
            </div>
          ))}
        </div>

        {/* System Design */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="card">
            <h2 className="font-bold text-lg mb-4">Modules</h2>
            <ul className="space-y-2">
              {currentCompilation.design.modules.map((module, idx) => (
                <li key={idx} className="flex items-center gap-2">
                  <span className="text-blue-600">●</span>
                  <span className="font-medium">{module.name}</span>
                  <span className="text-xs text-gray-500">({module.pages.length} pages)</span>
                </li>
              ))}
            </ul>
          </div>

          <div className="card">
            <h2 className="font-bold text-lg mb-4">Database Tables</h2>
            <ul className="space-y-2">
              {currentCompilation.schema.database_schema.map((table, idx) => (
                <li key={idx} className="flex items-center gap-2">
                  <span className="text-green-600">■</span>
                  <span className="font-medium">{table.table_name}</span>
                  <span className="text-xs text-gray-500">({table.fields.length} fields)</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* API Endpoints */}
        <JSONViewer
          title="Generated API Endpoints"
          data={currentCompilation.schema.api_schema.map(endpoint => ({
            method: endpoint.method,
            path: endpoint.path,
            description: endpoint.description,
            roles: endpoint.required_roles
          }))}
        />

        {/* Auth Flow */}
        <div className="card mt-6">
          <h2 className="font-bold text-lg mb-2">Authentication</h2>
          <p className="text-gray-700">{currentCompilation.design.auth_flow}</p>
        </div>
      </div>
    </Layout>
  )
}
