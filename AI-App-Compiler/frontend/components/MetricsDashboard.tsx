"use client"
import React from 'react'

export default function MetricsDashboard({ metrics }: { metrics?: any }) {
  const m = metrics || { successRate: 0, validationFailures: 0, repairCount: 0, runtimeSuccess: 0, latency: 0 }
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h3 className="font-semibold mb-4">Metrics</h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="p-3 border rounded">
          <div className="text-sm">Success Rate</div>
          <div className="text-xl font-bold">{m.successRate}%</div>
        </div>
        <div className="p-3 border rounded">
          <div className="text-sm">Validation Failures</div>
          <div className="text-xl font-bold">{m.validationFailures}</div>
        </div>
        <div className="p-3 border rounded">
          <div className="text-sm">Repair Count</div>
          <div className="text-xl font-bold">{m.repairCount}</div>
        </div>
        <div className="p-3 border rounded">
          <div className="text-sm">Runtime Success</div>
          <div className="text-xl font-bold">{m.runtimeSuccess}%</div>
        </div>
      </div>
      <div className="mt-4 text-sm">Latency: <strong>{m.latency}ms</strong></div>
    </div>
  )
}
