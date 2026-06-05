'use client'

import React, { useState } from 'react'

export default function PromptPage() {
  const [prompt, setPrompt] = useState('')
  const [status, setStatus] = useState<string | null>(null)

  const submit = async () => {
    setStatus('submitted')
    // placeholder: will call API /v1/compile
    setTimeout(() => setStatus('queued'), 500)
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Prompt Input</h2>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Describe the application requirements..."
        className="w-full h-48 p-3 border rounded bg-white"
      />
      <div className="mt-4 flex items-center gap-3">
        <button onClick={submit} className="px-4 py-2 bg-blue-600 text-white rounded">Submit</button>
        <span className="text-sm text-gray-600">Status: {status ?? 'idle'}</span>
      </div>
      <section className="mt-8">
        <h3 className="text-lg font-medium">Recent</h3>
        <div className="mt-2 text-sm text-gray-500">No recent prompts in this demo.</div>
      </section>
    </div>
  )
}
