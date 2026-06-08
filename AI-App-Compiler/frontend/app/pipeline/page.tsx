import React from 'react'
import PipelineViewer from '../../components/PipelineViewer'

export default function PipelinePage() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div className="col-span-2">
        <h2 className="text-xl font-semibold mb-4">Pipeline Viewer</h2>
        <PipelineViewer />
      </div>
      <aside>
        <h3 className="font-semibold mb-2">Notes</h3>
        <p className="text-sm">Follow the pipeline stages to see how prompts are transformed.</p>
      </aside>
    </div>
  )
}
