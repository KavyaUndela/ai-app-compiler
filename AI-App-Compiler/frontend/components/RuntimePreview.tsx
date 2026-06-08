"use client"
import React from 'react'

export default function RuntimePreview({ schema }: { schema?: any }) {
  // Very small renderer for forms/tables based on schema shape
  return (
    <div className="p-4 bg-white dark:bg-gray-800 rounded shadow">
      <h3 className="font-semibold mb-3">Runtime Preview</h3>
      <div>
        <pre className="text-xs p-2 bg-gray-50 dark:bg-gray-900 rounded max-h-96 overflow-auto">{JSON.stringify(schema, null, 2)}</pre>
      </div>
    </div>
  )
}
