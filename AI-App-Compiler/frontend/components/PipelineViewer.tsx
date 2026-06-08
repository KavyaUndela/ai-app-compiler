"use client"
import React from 'react'

export default function PipelineViewer() {
  const stages = [
    'Intent Extraction',
    'System Design',
    'Schema Generation',
    'Validation Engine',
    'Repair Engine',
    'Runtime Simulator',
  ]

  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h3 className="font-semibold mb-3">Pipeline</h3>
      <div className="space-y-2">
        {stages.map((s, i) => (
          <div key={s} className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-indigo-500 text-white flex items-center justify-center">{i+1}</div>
            <div>{s}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
