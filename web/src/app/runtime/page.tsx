'use client'

import React from 'react'

export default function RuntimePage() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Runtime Preview</h2>
      <div className="bg-white border rounded p-4">
        <h3 className="font-medium">Simulation Runs</h3>
        <div className="mt-2 text-sm text-gray-600">No simulation runs available.</div>
      </div>
    </div>
  )
}
