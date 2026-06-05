'use client'

import React from 'react'

export default function PipelinePage() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Pipeline Viewer</h2>
      <div className="space-y-4">
        <div className="p-4 bg-white border rounded">Intent Extraction: <span className="text-sm text-gray-600">idle</span></div>
        <div className="p-4 bg-white border rounded">System Design: <span className="text-sm text-gray-600">waiting</span></div>
        <div className="p-4 bg-white border rounded">Schema Generation: <span className="text-sm text-gray-600">pending</span></div>
        <div className="p-4 bg-white border rounded">Validation: <span className="text-sm text-gray-600">n/a</span></div>
        <div className="p-4 bg-white border rounded">Repair: <span className="text-sm text-gray-600">n/a</span></div>
        <div className="p-4 bg-white border rounded">Simulation: <span className="text-sm text-gray-600">n/a</span></div>
      </div>
    </div>
  )
}
