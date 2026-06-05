import { useMemo, useState } from 'react'
import Link from 'next/link'
import { useQuery } from '@tanstack/react-query'
import { compilerAPI } from '@/services/api'
import { useCompilerStore } from '@/store/compilerStore'

const samplePrompts = [
  'Build a CRM with login, contacts, dashboard, role-based access, premium plans and payments.',
  'Create a hospital management app with patient records, appointments, roles, and billing.',
  'Build a school ERP with students, teachers, attendance, timetables, and exam reports.',
  'Create an inventory system with products, suppliers, orders, and analytics.',
]

const quickStats = [
  { value: '6', label: 'deterministic stages' },
  { value: 'JSON', label: 'structured outputs' },
  { value: 'Live', label: 'runtime previews' },
]

const pipelineSteps = [
  'Intent Extraction',
  'System Design',
  'Schema Generation',
  'Validation Engine',
  'Repair Engine',
  'Runtime Simulator',
]

export default function LandingPage() {
  const [prompt, setPrompt] = useState(samplePrompts[0])
  const { currentCompilation, loading, error, generateConfiguration } = useCompilerStore()

  const healthQuery = useQuery({
    queryKey: ['health'],
    queryFn: compilerAPI.health,
    refetchInterval: 12000,
  })

  const activeResult = useMemo(() => currentCompilation, [currentCompilation])
  const isHealthy = healthQuery.data?.status === 'healthy'

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute left-[-10rem] top-[-8rem] h-[26rem] w-[26rem] rounded-full bg-cyan-500/10 blur-3xl" />
        <div className="absolute right-[-8rem] top-[10rem] h-[22rem] w-[22rem] rounded-full bg-violet-500/10 blur-3xl" />
        <div className="absolute bottom-[-10rem] left-[28%] h-[22rem] w-[22rem] rounded-full bg-emerald-500/10 blur-3xl" />
      </div>

      <header className="relative border-b border-white/5 bg-slate-950/80 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-cyan-500/10 text-sm font-bold text-cyan-300 ring-1 ring-cyan-400/20">
              AC
            </div>
            <div>
              <div className="text-sm font-semibold tracking-wide text-white">AI Compiler</div>
              <div className="text-xs text-slate-400">Blueprint generator</div>
            </div>
          </Link>

          <nav className="hidden items-center gap-2 md:flex">
            <Link href="/pipeline" className="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white">
              Pipeline Viewer
            </Link>
            <Link href="/validation" className="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white">
              Validation Viewer
            </Link>
            <Link href="/repair" className="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white">
              Repair Viewer
            </Link>
            <Link href="/runtime" className="rounded-full px-4 py-2 text-sm text-slate-300 transition hover:bg-white/5 hover:text-white">
              Runtime Preview
            </Link>
          </nav>
        </div>
      </header>

      <section className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
        <div className="grid gap-8 xl:grid-cols-[1.08fr_0.92fr] xl:items-start">
          <div className="space-y-8">
            

            <div className="space-y-5">
              <span className="inline-flex rounded-full border border-cyan-500/20 bg-cyan-500/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.3em] text-cyan-300">
                AI Application Compiler
              </span>
              <h1 className="max-w-4xl text-5xl font-semibold leading-tight tracking-tight text-white sm:text-6xl lg:text-7xl">
                Turn requirements into a polished application blueprint.
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-300 sm:text-xl">
                Generate intent, architecture, schemas, validation feedback, repair suggestions, and runtime previews from one product prompt.
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
              <Link href="#composer" className="inline-flex items-center justify-center rounded-full bg-cyan-500 px-6 py-4 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400">
                Start from prompt
              </Link>
              <Link href="/pipeline" className="inline-flex items-center justify-center rounded-full border border-white/10 bg-white/5 px-6 py-4 text-sm font-semibold text-slate-200 transition hover:bg-white/10 hover:text-white">
                View pipeline
              </Link>
            </div>

            <div className="grid gap-4 sm:grid-cols-3">
              {quickStats.map((item) => (
                <div key={item.label} className="rounded-3xl border border-white/8 bg-white/5 p-5 shadow-xl shadow-black/10 backdrop-blur">
                  <div className="text-3xl font-semibold text-white">{item.value}</div>
                  <p className="mt-2 text-sm text-slate-400">{item.label}</p>
                </div>
              ))}
            </div>

            <div className="grid gap-4 md:grid-cols-3">
              <div className="rounded-3xl border border-white/8 bg-slate-900/70 p-5">
                <div className="text-sm font-semibold text-cyan-300">Deterministic</div>
                <p className="mt-2 text-sm text-slate-400">Predictable outputs for engineering workflows.</p>
              </div>
              <div className="rounded-3xl border border-white/8 bg-slate-900/70 p-5">
                <div className="text-sm font-semibold text-emerald-300">Validated</div>
                <p className="mt-2 text-sm text-slate-400">Cross-layer checks for database, API, and UI consistency.</p>
              </div>
              <div className="rounded-3xl border border-white/8 bg-slate-900/70 p-5">
                <div className="text-sm font-semibold text-violet-300">Inspectable</div>
                <p className="mt-2 text-sm text-slate-400">Review every stage in dedicated viewer pages.</p>
              </div>
            </div>
          </div>

          <div id="composer" className="rounded-[2rem] border border-white/8 bg-white/5 p-6 shadow-2xl shadow-black/20 backdrop-blur-xl sm:p-8">
            <div className="flex items-center justify-between gap-4">
              <div>
                <div className="text-xs uppercase tracking-[0.28em] text-slate-500">Prompt composer</div>
                <h2 className="mt-2 text-2xl font-semibold text-white">Generate a blueprint</h2>
              </div>
              <div className="rounded-full border border-white/8 bg-slate-950/70 px-4 py-2 text-sm text-slate-300">Live mode</div>
            </div>

            <div className="mt-6 space-y-4">
              <label className="text-sm font-medium text-slate-300">Describe your product</label>
              <textarea
                value={prompt}
                onChange={(event) => setPrompt(event.target.value)}
                className="min-h-[190px] w-full rounded-3xl border border-white/10 bg-slate-950/80 p-5 text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-cyan-500 focus:ring-2 focus:ring-cyan-500/20"
                placeholder="Build a CRM with login, contacts, dashboard, role-based access, premium plans and payments."
              />

              <div className="flex flex-wrap gap-2">
                {samplePrompts.map((item) => (
                  <button
                    key={item}
                    type="button"
                    onClick={() => setPrompt(item)}
                    className="rounded-full border border-white/10 bg-slate-950/70 px-4 py-2 text-xs font-medium text-slate-300 transition hover:border-cyan-500/40 hover:text-cyan-200"
                  >
                    {item.split(',')[0]}
                  </button>
                ))}
              </div>

              <div className="flex flex-wrap gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => generateConfiguration(prompt)}
                  disabled={loading || !prompt.trim()}
                  className="inline-flex items-center justify-center rounded-full bg-cyan-500 px-6 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? 'Generating...' : 'Generate blueprint'}
                </button>
                <Link
                  href="/runtime"
                  className="inline-flex items-center justify-center rounded-full border border-white/10 bg-white/5 px-6 py-3 text-sm font-semibold text-slate-200 transition hover:bg-white/10 hover:text-white"
                >
                  Runtime preview
                </Link>
              </div>

              {error && <div className="rounded-3xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">{error}</div>}
            </div>

            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              <div className="rounded-3xl border border-white/8 bg-slate-950/80 p-5">
                <div className="mb-3 text-xs uppercase tracking-[0.2em] text-slate-500">Pipeline status</div>
                <div className="text-2xl font-semibold text-cyan-300">{activeResult ? activeResult.status : 'Ready to generate'}</div>
                <p className="mt-3 text-sm text-slate-400">{activeResult ? activeResult.summary : 'The compiler will create intent, schemas, validation, repair, and runtime output.'}</p>
              </div>
              <div className="rounded-3xl border border-white/8 bg-slate-950/80 p-5">
                <div className="mb-3 text-xs uppercase tracking-[0.2em] text-slate-500">Backend health</div>
                <div className={`text-2xl font-semibold ${isHealthy ? 'text-emerald-300' : 'text-amber-300'}`}>{isHealthy ? 'Online' : 'Checking...'}</div>
                <p className="mt-3 text-sm text-slate-400">{healthQuery.data ? `Service: ${healthQuery.data.service}` : 'Waiting for backend response...'}</p>
              </div>
            </div>
          </div>
        </div>

        <section className="mt-10 grid gap-4 lg:grid-cols-[1fr_1.1fr]">
          <div className="rounded-[2rem] border border-white/8 bg-slate-900/60 p-6">
            <div className="flex items-center justify-between gap-3">
              <div>
                <div className="text-sm uppercase tracking-[0.28em] text-cyan-300">Sample prompts</div>
                <h2 className="mt-3 text-2xl font-semibold text-white">Try common product types</h2>
              </div>
              <div className="rounded-full border border-white/8 bg-slate-950/70 px-4 py-2 text-sm text-slate-300">4 examples</div>
            </div>

            <div className="mt-6 grid gap-3">
              {samplePrompts.map((item, index) => (
                <button
                  key={item}
                  type="button"
                  onClick={() => setPrompt(item)}
                  className="rounded-3xl border border-white/8 bg-slate-950/70 px-4 py-4 text-left text-sm text-slate-200 transition hover:border-cyan-500/40 hover:bg-white/5"
                >
                  <div className="text-slate-500">0{index + 1}</div>
                  <p className="mt-2 font-medium text-slate-100">{item}</p>
                </button>
              ))}
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-[2rem] border border-white/8 bg-slate-900/60 p-6">
              <div className="text-sm uppercase tracking-[0.28em] text-slate-500">Compiler stages</div>
              <div className="mt-4 grid grid-cols-2 gap-3">
                {pipelineSteps.map((step) => (
                  <div key={step} className="rounded-2xl border border-white/8 bg-slate-950/70 px-3 py-3 text-xs font-medium text-slate-200">
                    {step}
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-[2rem] border border-white/8 bg-slate-900/60 p-6">
              <div className="text-sm uppercase tracking-[0.28em] text-emerald-300">Viewer pages</div>
              <div className="mt-4 grid gap-3">
                <Link href="/pipeline" className="rounded-2xl border border-white/8 bg-slate-950/70 px-4 py-4 text-sm text-slate-200 transition hover:border-cyan-500/40">
                  Pipeline Viewer
                </Link>
                <Link href="/validation" className="rounded-2xl border border-white/8 bg-slate-950/70 px-4 py-4 text-sm text-slate-200 transition hover:border-cyan-500/40">
                  Validation Viewer
                </Link>
                <Link href="/repair" className="rounded-2xl border border-white/8 bg-slate-950/70 px-4 py-4 text-sm text-slate-200 transition hover:border-cyan-500/40">
                  Repair Viewer
                </Link>
                <Link href="/runtime" className="rounded-2xl border border-white/8 bg-slate-950/70 px-4 py-4 text-sm text-slate-200 transition hover:border-cyan-500/40">
                  Runtime Preview
                </Link>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-10 grid gap-4 md:grid-cols-3">
          <div className="rounded-[1.75rem] border border-white/8 bg-white/5 p-6">
            <div className="text-sm uppercase tracking-[0.28em] text-slate-500">Intent</div>
            <p className="mt-3 text-slate-200">Extract roles, features, entities, and workflows from the prompt.</p>
          </div>
          <div className="rounded-[1.75rem] border border-white/8 bg-white/5 p-6">
            <div className="text-sm uppercase tracking-[0.28em] text-slate-500">Validate</div>
            <p className="mt-3 text-slate-200">Detect JSON, relationship, API, and UI mismatches before delivery.</p>
          </div>
          <div className="rounded-[1.75rem] border border-white/8 bg-white/5 p-6">
            <div className="text-sm uppercase tracking-[0.28em] text-slate-500">Repair</div>
            <p className="mt-3 text-slate-200">Auto-fix invalid sections while preserving valid generated output.</p>
          </div>
        </section>
      </section>
    </main>
  )
}
