import React from 'react'
import RuntimePreview from '../../components/RuntimePreview'

export default function RuntimePreviewPage() {
  const schema = { form: [{ name: 'title', type: 'text' }], table: [{ name: 'id' }, { name: 'title' }] }
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Runtime Preview</h2>
      <RuntimePreview schema={schema} />
    </div>
  )
}
