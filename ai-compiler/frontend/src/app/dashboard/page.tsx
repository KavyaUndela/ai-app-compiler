'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const [dashboard, setDashboard] = useState<any>(null);
  const [performance, setPerformance] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  const loadMetrics = async () => {
    try {
      const [dash, perf, h] = await Promise.all([
        api.getDashboard(),
        api.getPerformance(),
        api.healthCheck()
      ]);

      setDashboard(dash.data);
      setPerformance(perf.data);
      setHealth(h.data);
    } catch (err) {
      console.error('Failed to load metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading metrics...</div>;
  }

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Metrics Dashboard</h1>

      {/* Health Status */}
      {health && (
        <div className="mb-8 bg-green-50 border-l-4 border-green-600 p-6 rounded">
          <h2 className="text-xl font-semibold text-green-800">✅ System Healthy</h2>
          <p className="text-gray-600 text-sm">API running normally</p>
        </div>
      )}

      {/* Compilation Stats */}
      {dashboard && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold">Total Compilations</h3>
            <p className="text-3xl font-bold text-blue-600">{dashboard.compilation_stats.total_compilations}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold">Successful</h3>
            <p className="text-3xl font-bold text-green-600">{dashboard.compilation_stats.successful}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold">Failed</h3>
            <p className="text-3xl font-bold text-red-600">{dashboard.compilation_stats.failed}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold">Success Rate</h3>
            <p className="text-3xl font-bold text-purple-600">{dashboard.compilation_stats.success_rate}%</p>
          </div>
        </div>
      )}

      {/* Performance Metrics */}
      {performance && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">API Performance</h3>
            <div className="space-y-3">
              <div>
                <p className="text-gray-600">Avg Response Time</p>
                <p className="text-2xl font-bold text-blue-600">
                  {performance.api_metrics.avg_response_time_ms}ms
                </p>
              </div>
              <div>
                <p className="text-gray-600">P95 Response Time</p>
                <p className="text-2xl font-bold text-blue-600">
                  {performance.api_metrics.p95_response_time_ms}ms
                </p>
              </div>
              <div>
                <p className="text-gray-600">Requests/Second</p>
                <p className="text-2xl font-bold text-blue-600">
                  {performance.api_metrics.requests_per_second} RPS
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Database Performance</h3>
            <div className="space-y-3">
              <div>
                <p className="text-gray-600">Avg Query Time</p>
                <p className="text-2xl font-bold text-green-600">
                  {performance.database_metrics.avg_query_time_ms}ms
                </p>
              </div>
              <div>
                <p className="text-gray-600">Total Queries</p>
                <p className="text-2xl font-bold text-green-600">
                  {performance.database_metrics.total_queries}
                </p>
              </div>
              <div>
                <p className="text-gray-600">Slow Queries</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {performance.database_metrics.slow_queries}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Recent Compilations */}
      {dashboard && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Compilations</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-gray-200">
                <tr>
                  <th className="text-left py-3 px-4 text-gray-600">ID</th>
                  <th className="text-left py-3 px-4 text-gray-600">Title</th>
                  <th className="text-left py-3 px-4 text-gray-600">Status</th>
                  <th className="text-left py-3 px-4 text-gray-600">Duration</th>
                </tr>
              </thead>
              <tbody>
                {dashboard.recent_compilations.map((c: any) => (
                  <tr key={c.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4 font-mono text-sm text-gray-600">{c.id}</td>
                    <td className="py-3 px-4">{c.title}</td>
                    <td className="py-3 px-4">
                      <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-sm">
                        {c.status}
                      </span>
                    </td>
                    <td className="py-3 px-4">{c.duration_ms}ms</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
