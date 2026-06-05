'use client'

import React from 'react'
import Link from 'next/link'

const Nav: React.FC = () => {
  const items = [
    { href: '/', label: 'Prompt' },
    { href: '/pipeline', label: 'Pipeline' },
    { href: '/validation', label: 'Validation' },
    { href: '/repair', label: 'Repair' },
    { href: '/runtime', label: 'Runtime' },
    { href: '/metrics', label: 'Metrics' },
  ]

  return (
    <nav className="w-64 bg-white border-r">
      <div className="p-6 border-b">
        <h1 className="text-lg font-semibold">AI Compiler</h1>
        <p className="text-sm text-gray-500">Dashboard</p>
      </div>
      <ul className="p-4 space-y-2">
        {items.map((it) => (
          <li key={it.href}>
            <Link href={it.href} className="block px-3 py-2 rounded hover:bg-gray-100">
              {it.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  )
}

export default Nav
