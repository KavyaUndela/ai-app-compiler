'use client'

import { useState } from 'react'
import { useRouter } from 'next/router'
import Layout from '@/components/Layout'
import JSONViewer from '@/components/JSONViewer'
import { useCompilerStore } from '@/store/compilerStore'

const SAMPLE_PROMPTS = [
  {
    title: 'CRM System',
    prompt: 'Build a CRM with login, contacts management, dashboard with analytics, role-based access (Admin, Manager, User), and email notifications.'
  },
  {
    title: 'Hospital Management',
    prompt: 'Create a hospital management system with patient records, doctor appointments, prescription management, billing, and admin panel.'
  },
  {
    title: 'School ERP',
    prompt: 'Design a school ERP system with student management, attendance tracking, class scheduling, grade management, and parent portal.'
  },
  {
    title: 'E-commerce Store',
    prompt: 'Build an e-commerce platform with product catalog, shopping cart, checkout, payment integration, order tracking, and admin dashboard.'
  }
]

export default function CompilerPage() {
  const [prompt, setPrompt] = useState('')
  const [selectedSample, setSelectedSample] = useState<string | null>(null)
  const router = useRouter()
  const { generateConfiguration, currentCompilation, loading, error } = useCompilerStore()

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      alert('Please enter a prompt')
      return
    }
    await generateConfiguration(prompt)
  }

  const handleSampleClick = (samplePrompt: string) => {
    setPrompt(samplePrompt)
    setSelectedSample(samplePrompt)
  }

  const handleViewResult = () => {
    if (currentCompilation) {
      router.push('/pipeline')
    }
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto space-y-10">
        <section className="overflow-hidden rounded-[2rem] bg-slate-950 px-8 py-16 shadow-2xl shadow-slate-950/40">
          <div className="max-w-3xl space-y-6 text-slate-100">
            <span className="inline-flex rounded-full bg-cyan-500/10 px-3 py-1 text-sm font-semibold tracking-[0.24em] text-cyan-300">
              AI Application Compiler
            </span>
            <h1 className="text-5xl font-semibold leading-tight tracking-tight">
              Build modern applications from plain English requirements.
            </h1>
            <p className="text-lg text-slate-300">
              Convert natural language requirements into executable application configurations, design flows, API schemas, and runtime plans in one elegant developer experience.
            </p>
            <div className="flex flex-wrap gap-4">
              <button
                type="button"
                onClick={handleGenerate}
                disabled={loading}
                className="btn-primary disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? 'Generating...' : 'Generate Configuration'}
              </button>
              <button
                type="button"
                onClick={handleViewResult}
                disabled={!currentCompilation}
                className="btn-secondary disabled:cursor-not-allowed disabled:opacity-60"
              >
                View Results →
              </button>
            </div>
          </div>
        </section>

        <div className="grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">
          <div className="space-y-8">
            {error && (
              <div className="rounded-3xl bg-red-50/90 border border-red-200 text-red-800 px-4 py-3 shadow-sm">
                <strong>Error:</strong> {error}
              </div>
            )}

            <div className="card">
              <h2 className="text-xl font-bold mb-4">Enter Your Requirements</h2>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your application... E.g., 'Build a CRM with login, contacts, dashboard, role-based access, and premium plans'"
                className="w-full h-40 p-4 border border-slate-700 bg-slate-950/80 rounded-3xl text-slate-100 focus:outline-none focus:ring-2 focus:ring-cyan-400"
              />
              <div className="flex gap-4 mt-4">
                <button
                  onClick={handleGenerate}
                  disabled={loading}
                  className="btn-primary disabled:opacity-50"
                >
                  {loading ? 'Generating...' : 'Generate Configuration'}
                </button>
                {currentCompilation && (
                  <button
                    onClick={handleViewResult}
                    className="btn-secondary"
                  >
                    View Results →
                  </button>
                )}
              </div>
            </div>

            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-4 text-slate-900">Try sample prompts</h2>
              <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                {SAMPLE_PROMPTS.map((sample, index) => (
                  <button
                    key={index}
                    onClick={() => handleSampleClick(sample.prompt)}
                    className={`rounded-[1.5rem] border p-5 text-left transition shadow-sm ${
                      selectedSample === sample.prompt
                        ? 'border-cyan-500 bg-cyan-50/80'
                        : 'border-slate-200 bg-white hover:border-slate-400'
                    }`}
                  >
                    <div className="font-semibold text-slate-950">{sample.title}</div>
                    <div className="mt-2 text-sm text-slate-600">{sample.prompt}</div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {currentCompilation && (
            <div className="space-y-6">
              <div className="card bg-green-50 border-2 border-green-200">
                <h2 className="text-xl font-bold text-green-800 mb-2">✓ Configuration Generated</h2>
                <p className="text-green-700 mb-4">{currentCompilation.summary}</p>
                <div className="text-sm text-slate-600">
                  <p>Status: <span className="font-bold text-green-700">{currentCompilation.status.toUpperCase()}</span></p>
                  <p>ID: {currentCompilation.compilation_id}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                <div className="card text-center">
                  <div className="text-3xl font-bold text-cyan-600">{currentCompilation.intent.entities.length}</div>
                  <div className="text-sm text-slate-600">Entities</div>
                </div>
                <div className="card text-center">
                  <div className="text-3xl font-bold text-purple-600">{currentCompilation.design.modules.length}</div>
                  <div className="text-sm text-slate-600">Modules</div>
                </div>
                <div className="card text-center">
                  <div className="text-3xl font-bold text-emerald-600">{currentCompilation.schema.database_schema.length}</div>
                  <div className="text-sm text-slate-600">Tables</div>
                </div>
                <div className="card text-center">
                  <div className="text-3xl font-bold text-orange-600">{currentCompilation.schema.api_schema.length}</div>
                  <div className="text-sm text-slate-600">Endpoints</div>
                </div>
              </div>

              <JSONViewer
                title="Intent Extraction"
                data={{
                  entities: currentCompilation.intent.entities.map((e) => ({ name: e.name, type: e.entity_type })),
                  features: currentCompilation.intent.features.map((f) => f.name),
                  roles: currentCompilation.intent.roles.map((r) => r.name),
                  workflows: currentCompilation.intent.workflows,
                }}
                expanded={true}
              />
            </div>
          )}
        </div>
      </div>
    </Layout>
  )
}
