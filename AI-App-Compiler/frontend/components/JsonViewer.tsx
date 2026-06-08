"use client"
import React from 'react'
import ReactJson from 'react-json-view'

export default function JsonViewer({ data }: { data: any }) {
  return (
    <div className="border rounded p-2 bg-gray-50 dark:bg-gray-900">
      <ReactJson src={data} name={false} collapsed={1} enableClipboard={true} displayDataTypes={false} />
    </div>
  )
}
