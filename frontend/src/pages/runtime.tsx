'use client'

import Layout from '@/components/Layout'
import { useCompilerStore } from '@/store/compilerStore'
import Link from 'next/link'
import { useState } from 'react'

export default function RuntimePage() {
  const { currentCompilation } = useCompilerStore()
  const [selectedTab, setSelectedTab] = useState<'preview' | 'forms' | 'data'>('preview')

  if (!currentCompilation) {
    return (
      <Layout>
        <div className="text-center py-12">
          <p className="text-gray-600 mb-4">No runtime data. Please generate a configuration first.</p>
          <Link href="/" className="btn-primary">
            Generate Configuration →
          </Link>
        </div>
      </Layout>
    )
  }

  const { runtime_preview } = currentCompilation

  return (
    <Layout>
      <div className="max-w-6xl">
        <h1 className="text-3xl font-bold mb-2">Runtime Preview</h1>
        <p className="text-gray-600 mb-8">Dynamic forms, CRUD pages, and HTML preview generated from your schema</p>

        {/* Tabs */}
        <div className="flex gap-4 mb-8 border-b">
          <button
            onClick={() => setSelectedTab('preview')}
            className={`px-4 py-2 font-bold ${
              selectedTab === 'preview'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600'
            }`}
          >
            HTML Preview
          </button>
          <button
            onClick={() => setSelectedTab('forms')}
            className={`px-4 py-2 font-bold ${
              selectedTab === 'forms'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600'
            }`}
          >
            Forms ({runtime_preview.dynamic_forms.length})
          </button>
          <button
            onClick={() => setSelectedTab('data')}
            className={`px-4 py-2 font-bold ${
              selectedTab === 'data'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600'
            }`}
          >
            Sample Data
          </button>
        </div>

        {/* HTML Preview Tab */}
        {selectedTab === 'preview' && (
          <div className="card">
            {runtime_preview.preview_html ? (
              <iframe
                srcDoc={runtime_preview.preview_html}
                className="w-full h-screen rounded border"
                title="Runtime Preview"
              />
            ) : (
              <p className="text-gray-600">No preview available</p>
            )}
          </div>
        )}

        {/* Forms Tab */}
        {selectedTab === 'forms' && (
          <div className="space-y-6">
            {runtime_preview.dynamic_forms.map((form, idx) => (
              <div key={idx} className="card">
                <h2 className="text-lg font-bold mb-2">{form.title}</h2>
                <p className="text-gray-600 mb-4">{form.description}</p>
                <div className="space-y-3 mb-4">
                  {form.fields.map((field, fidx) => (
                    <div key={fidx}>
                      <label className="block font-medium mb-1">
                        {field.label}
                        {field.required && <span className="text-red-600">*</span>}
                      </label>
                      {field.field_type === 'select' ? (
                        <select className="w-full border border-gray-300 rounded p-2">
                          <option>Select {field.label}</option>
                          {field.options?.map((opt, oidx) => (
                            <option key={oidx}>{opt}</option>
                          ))}
                        </select>
                      ) : field.field_type === 'textarea' ? (
                        <textarea className="w-full border border-gray-300 rounded p-2 h-24" />
                      ) : field.field_type === 'checkbox' ? (
                        <input type="checkbox" className="w-4 h-4" />
                      ) : (
                        <input
                          type={field.field_type}
                          className="w-full border border-gray-300 rounded p-2"
                        />
                      )}
                    </div>
                  ))}
                </div>
                <button className="btn-primary">
                  Submit to {form.submit_action}
                </button>
              </div>
            ))}
          </div>
        )}

        {/* Sample Data Tab */}
        {selectedTab === 'data' && (
          <div className="space-y-6">
            {Object.entries(runtime_preview.sample_data).map(([entity, data], idx) => (
              <div key={idx} className="card">
                <h2 className="text-lg font-bold mb-4">{entity.charAt(0).toUpperCase() + entity.slice(1)}</h2>
                <div className="overflow-auto">
                  <table className="w-full border-collapse text-sm">
                    <thead className="bg-gray-100">
                      <tr>
                        {Object.keys(data[0] || {}).map((key) => (
                          <th key={key} className="border p-2 text-left font-bold">
                            {key}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {data.map((row, ridx) => (
                        <tr key={ridx} className="border-b hover:bg-gray-50">
                          {Object.values(row).map((value, vidx) => (
                            <td key={vidx} className="border p-2">
                              {String(value).substring(0, 50)}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </Layout>
  )
}
