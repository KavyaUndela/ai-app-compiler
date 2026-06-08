"use client"
import React, { useState } from 'react'
import { generate } from '../services/api'
import toast from 'react-hot-toast'
import JsonViewer from './JsonViewer'

export default function PromptInput() {
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  async function onGenerate() {
    if (!prompt.trim()) return toast.error('Enter a prompt')
    setLoading(true)
    try {
      const res = await generate({ prompt })
      setResult(res)
      toast.success('Generated')
    } catch (err: any) {
      toast.error(err?.message || 'Generation failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 bg-white dark:bg-gray-800 rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Prompt Input</h2>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        rows={6}
        className="w-full border rounded p-2 mb-3 bg-transparent"
        placeholder="Describe the application you want"
      />
      <div className="flex items-center gap-3">
        <button onClick={onGenerate} className="px-4 py-2 bg-indigo-600 text-white rounded" disabled={loading}>{loading? 'Generating...':'Generate'}</button>
        <button onClick={()=>setPrompt('')} className="px-3 py-2 border rounded">Clear</button>
      </div>

      {result && (
        <div className="mt-6">
          <h3 className="font-medium mb-2">Result</h3>
          <JsonViewer data={result} />
        </div>
      )}
    </div>
  )
}
