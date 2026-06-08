import React from 'react'
import dynamic from 'next/dynamic'
import PromptInput from '../components/PromptInput'

export default function Page() {
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="col-span-2">
          <PromptInput />
        </div>
        <aside className="p-4 bg-white dark:bg-gray-800 rounded shadow">
          <h3 className="font-semibold mb-2">Example Prompts</h3>
          <ul className="text-sm space-y-2">
            <li>"Create a CRUD app for task management"</li>
            <li>"Design an API for user profiles with auth"</li>
            <li>"Generate UI schema for a product catalog"</li>
          </ul>
        </aside>
      </section>
    </div>
  )
}
import React from 'react'

export default function Page() {
  return (
    <main style={{padding:32,fontFamily:'Arial'}}>
      <h1>AI-App-Compiler — Frontend</h1>
      <p>Placeholder Next.js app. Start the real frontend in `frontend/`.</p>
    </main>
  )
}
