'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-12 text-center">
        <h1 className="text-5xl font-bold text-gray-800 mb-4">
          AI Application Compiler
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Convert natural language requirements into executable application configurations
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-12">
          <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-600">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">Intent Extraction</h3>
            <p className="text-gray-600">Understand your requirements at a deep level</p>
          </div>
          <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-600">
            <h3 className="text-lg font-semibold text-green-800 mb-2">System Design</h3>
            <p className="text-gray-600">Generate optimal architecture patterns</p>
          </div>
          <div className="bg-purple-50 p-6 rounded-lg border-l-4 border-purple-600">
            <h3 className="text-lg font-semibold text-purple-800 mb-2">Validation</h3>
            <p className="text-gray-600">Validate and repair configurations</p>
          </div>
        </div>

        <div className="flex gap-4 justify-center">
          <Link
            href="/compiler"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
          >
            Start Compiling
          </Link>
          <Link
            href="/dashboard"
            className="px-8 py-3 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 font-semibold"
          >
            View Dashboard
          </Link>
        </div>
      </div>

      <div className="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">🚀 Quick Start</h3>
          <p className="text-gray-600 mb-2">1. Enter your application requirements</p>
          <p className="text-gray-600 mb-2">2. Describe desired features and constraints</p>
          <p className="text-gray-600 mb-2">3. Get instant system design and schema</p>
          <p className="text-gray-600">4. Review and refine the output</p>
        </div>
        <div className="bg-white p-6 rounded-lg shadow">
          <h3 className="text-xl font-semibold text-gray-800 mb-4">✨ Features</h3>
          <p className="text-gray-600 mb-2">✓ Multi-stage compilation pipeline</p>
          <p className="text-gray-600 mb-2">✓ Real-time validation</p>
          <p className="text-gray-600 mb-2">✓ Automatic repair suggestions</p>
          <p className="text-gray-600">✓ Performance simulation</p>
        </div>
      </div>
    </div>
  );
}
