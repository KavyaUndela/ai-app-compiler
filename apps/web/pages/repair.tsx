import { useState, useEffect } from 'react'
import { postRepair } from '../lib/api'

export default function RepairPage() {
  const [payload, setPayload] = useState('')
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const cached = localStorage.getItem('lastGenerated')
    if (cached) setPayload(cached)
  }, [])

  async function runRepair() {
    setLoading(true)
    try {
      const parsed = JSON.parse(payload)
      const res = await postRepair(parsed)
      setReport(res)
    } catch (e) {
      setReport({ error: String(e) })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Repair Viewer</h2>
      <textarea rows={10} className="w-full p-3 border rounded mb-3 bg-white" value={payload} onChange={(e) => setPayload(e.target.value)} />
      <div className="flex gap-2">
        <button className="px-4 py-2 bg-yellow-600 text-white rounded" onClick={runRepair} disabled={loading}>
          {loading ? 'Repairing...' : 'Run Repair'}
        </button>
      </div>

      <section className="mt-6">
        <h3 className="font-medium">Repair Report</h3>
        <pre className="mt-2 p-3 bg-white border rounded max-h-96 overflow-auto">{JSON.stringify(report, null, 2)}</pre>
      </section>
    </div>
  )
}
