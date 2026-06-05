import { useEffect, useState } from 'react'
import { getMetrics } from '../lib/api'

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<any>(null)

  useEffect(() => {
    getMetrics().then(setMetrics).catch((e) => setMetrics({ error: String(e) }))
  }, [])

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Metrics Dashboard</h2>
      <div className="bg-white border rounded p-4">
        <pre className="max-h-96 overflow-auto">{JSON.stringify(metrics, null, 2)}</pre>
      </div>
    </div>
  )
}
