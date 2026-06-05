import { useEffect, useState } from 'react'

export default function PipelinePage() {
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    // placeholder: load from localStorage or previous result
    const cached = localStorage.getItem('lastGenerated')
    if (cached) setData(JSON.parse(cached))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Pipeline Viewer</h2>
      <p className="mb-4 text-sm text-slate-600">Shows the generated pipeline (Intent → Architecture → Schemas).</p>
      <div className="bg-white border rounded p-4">
        <pre className="max-h-96 overflow-auto">{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  )
}
