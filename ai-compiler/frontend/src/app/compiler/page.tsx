'use client';

import { useState } from 'react';
import { api } from '@/lib/api';
import { CompilationResponse } from '@/lib/types';

export default function CompilerPage() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [features, setFeatures] = useState('');
  const [constraints, setConstraints] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<CompilationResponse | null>(null);
  const [error, setError] = useState('');

  const handleCompile = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await api.compile({
        requirement: {
          title,
          description,
          features: features.split('\n').filter(f => f.trim()),
          constraints,
          tech_preferences: { frontend: 'Next.js', backend: 'FastAPI' }
        },
        include_simulation: true,
        include_repairs: true
      });

      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Compilation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-800 mb-8">Application Compiler</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">Your Requirements</h2>
          <form onSubmit={handleCompile}>
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">Project Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., E-commerce Platform"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">Description</label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe your application in detail..."
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">Features (one per line)</label>
              <textarea
                value={features}
                onChange={(e) => setFeatures(e.target.value)}
                placeholder="User authentication&#10;Product search&#10;Payment processing"
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            <div className="mb-6">
              <label className="block text-gray-700 font-semibold mb-2">Constraints</label>
              <input
                type="text"
                value={constraints}
                onChange={(e) => setConstraints(e.target.value)}
                placeholder="e.g., Must handle 10k concurrent users"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>

            {error && (
              <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-semibold transition"
            >
              {loading ? 'Compiling...' : 'Compile Application'}
            </button>
          </form>
        </div>

        {/* Results */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">Compilation Result</h2>

          {result ? (
            <div className="space-y-6">
              <div className="bg-green-50 p-4 rounded border-l-4 border-green-600">
                <h3 className="font-semibold text-green-800">Status: ✅ Compiled</h3>
                <p className="text-sm text-gray-600">Duration: {result.duration_ms.toFixed(2)}ms</p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Architecture</h3>
                <p className="text-gray-600">{result.design.architecture}</p>
              </div>

              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Components</h3>
                <ul className="list-disc list-inside text-gray-600">
                  {result.design.components.slice(0, 3).map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="font-semibold text-gray-800 mb-2">Validation Score</h3>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${result.validation.score * 100}%` }}
                  />
                </div>
                <p className="text-sm text-gray-600 mt-1">
                  {(result.validation.score * 100).toFixed(1)}%
                </p>
              </div>

              <button
                onClick={() => setResult(null)}
                className="w-full px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400 font-semibold"
              >
                New Compilation
              </button>
            </div>
          ) : (
            <div className="text-center text-gray-500 py-12">
              <p>Fill in your requirements and click "Compile Application"</p>
              <p className="text-sm mt-2">Results will appear here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
