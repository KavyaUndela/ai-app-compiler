"use client"
import React from 'react'

export default function RepairViewer({ before, after }: { before?: any; after?: any }) {
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h3 className="font-semibold mb-3">Repair Report</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <h4 className="font-medium">Before</h4>
          <pre className="text-xs p-2 bg-gray-50 dark:bg-gray-900 rounded max-h-64 overflow-auto">{JSON.stringify(before, null, 2)}</pre>
        </div>
        <div>
          <h4 className="font-medium">After</h4>
          <pre className="text-xs p-2 bg-gray-50 dark:bg-gray-900 rounded max-h-64 overflow-auto">{JSON.stringify(after, null, 2)}</pre>
        </div>
      </div>
    </div>
  )
}
