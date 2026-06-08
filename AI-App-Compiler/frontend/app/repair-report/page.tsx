import React from 'react'
import RepairViewer from '../../components/RepairViewer'

export default function RepairReportPage() {
  const before = { issues: ['missing id', 'invalid type'] }
  const after = { issues: [] }
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Repair Report</h2>
      <RepairViewer before={before} after={after} />
    </div>
  )
}
