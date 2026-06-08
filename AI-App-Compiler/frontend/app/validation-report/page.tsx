import React from 'react'
import ValidationViewer from '../../components/ValidationViewer'

export default function ValidationReportPage() {
  const example = { failures: [{ message: 'Missing required field name' }], warnings: [{ message: 'Deprecated field used' }] }
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Validation Report</h2>
      <ValidationViewer report={example} />
    </div>
  )
}
