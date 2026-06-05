import Link from 'next/link'

export default function Nav() {
  return (
    <header className="bg-white border-b">
      <div className="container flex items-center justify-between py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-md bg-indigo-600 flex items-center justify-center text-white font-bold">AC</div>
          <div>
            <h1 className="text-lg font-semibold">AI Compiler</h1>
            <div className="text-xs text-slate-500">Blueprint generator</div>
          </div>
        </div>

        <nav className="hidden md:flex items-center gap-4 text-sm">
          <Link className="text-slate-700 hover:text-indigo-600" href="/">Home</Link>
          <Link className="text-slate-700 hover:text-indigo-600" href="/pipeline">Pipeline</Link>
          <Link className="text-slate-700 hover:text-indigo-600" href="/validation">Validation</Link>
          <Link className="text-slate-700 hover:text-indigo-600" href="/repair">Repair</Link>
          <Link className="text-slate-700 hover:text-indigo-600" href="/runtime">Runtime</Link>
          <Link className="text-slate-700 hover:text-indigo-600" href="/metrics">Metrics</Link>
        </nav>
      </div>
    </header>
  )
}
