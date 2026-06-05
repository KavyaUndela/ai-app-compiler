import { ReactNode } from 'react'

interface JSONViewerProps {
  data: any
  title?: string
  expanded?: boolean
}

export default function JSONViewer({ data, title, expanded = false }: JSONViewerProps) {
  const [isExpanded, setIsExpanded] = React.useState(expanded)

  return (
    <div className="card">
      {title && (
        <div
          className="flex items-center justify-between cursor-pointer mb-3"
          onClick={() => setIsExpanded(!isExpanded)}
        >
          <h3 className="font-bold text-lg">{title}</h3>
          <span className="text-lg">{isExpanded ? '▼' : '▶'}</span>
        </div>
      )}
      {isExpanded && (
        <pre className="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-96 text-gray-800">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  )
}

import React from 'react'
