import { useEffect, useState } from 'react'
import { postRuntimePreview } from '../lib/api'

export default function RuntimePage() {
  const [payload, setPayload] = useState('')
  const [preview, setPreview] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const cached = localStorage.getItem('lastGenerated')
    if (cached) setPayload(cached)
  }, [])

  async function runPreview() {
    setLoading(true)
    try {
      const parsed = JSON.parse(payload)
      const res = await postRuntimePreview(parsed)
      setPreview(res)
    } catch (e) {
      setPreview({ error: String(e) })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Runtime Preview</h2>
      <textarea rows={10} className="w-full p-3 border rounded mb-3 bg-white" value={payload} onChange={(e) => setPayload(e.target.value)} />
      <div className="flex gap-2">
        <button className="px-4 py-2 bg-indigo-600 text-white rounded" onClick={runPreview} disabled={loading}>
          {loading ? 'Generating preview...' : 'Run Preview'}
        </button>
      </div>

      <section className="mt-6">
        <h3 className="font-medium">Preview</h3>
        <pre className="mt-2 p-3 bg-white border rounded max-h-96 overflow-auto">{JSON.stringify(preview, null, 2)}</pre>
      </section>
    </div>
  )
}
