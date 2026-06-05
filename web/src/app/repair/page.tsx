'use client'

import React from 'react'

export default function RepairPage() {
  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Repair Viewer</h2>
      <div className="bg-white border rounded p-4">
        <h3 className="font-medium">Suggested Repairs</h3>
        <ul className="mt-2 list-disc pl-6 text-sm text-gray-600">
          <li>No suggested repairs yet.</li>
        </ul>
      </div>
    </div>
  )
}
