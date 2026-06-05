'use client'

import React from 'react'

export default function MetricsPage() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Metrics Dashboard</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 bg-white border rounded">Throughput<br/><span className="text-lg font-semibold">—</span></div>
        <div className="p-4 bg-white border rounded">Error Rate<br/><span className="text-lg font-semibold">—</span></div>
        <div className="p-4 bg-white border rounded">Latency P95<br/><span className="text-lg font-semibold">—</span></div>
      </div>
    </div>
  )
}
