import React from 'react'
import MetricsDashboard from '../../components/MetricsDashboard'
import { getMetrics } from '../../services/api'

export default async function MetricsPage() {
  let metrics = null
  try {
    metrics = await getMetrics()
  } catch (e) {
    metrics = null
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Metrics</h2>
      <MetricsDashboard metrics={metrics} />
    </div>
  )
}
