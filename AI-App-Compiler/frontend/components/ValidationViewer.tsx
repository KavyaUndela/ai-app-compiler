"use client"
import React from 'react'

export default function ValidationViewer({ report }: { report?: any }) {
  const failures = report?.failures || []
  const warnings = report?.warnings || []
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h3 className="font-semibold mb-3">Validation Report</h3>
      <div className="mb-3">
        <div className="text-sm">Errors: <strong>{failures.length}</strong></div>
        <div className="text-sm">Warnings: <strong>{warnings.length}</strong></div>
      </div>

      <div className="space-y-2">
        {failures.map((f: any, idx: number) => (
          <div key={idx} className="p-2 border rounded bg-red-50 dark:bg-red-900/20">{f.message || JSON.stringify(f)}</div>
        ))}

        {warnings.map((w: any, idx: number) => (
          <div key={idx} className="p-2 border rounded bg-yellow-50 dark:bg-yellow-900/20">{w.message || JSON.stringify(w)}</div>
        ))}
      </div>
    </div>
  )
}
