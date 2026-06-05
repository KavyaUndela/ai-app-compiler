import Navbar from './Navbar'
import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <>
      <Navbar />
      <main className="flex-1 pt-20 pb-8">
        <div className="container">
          {children}
        </div>
      </main>
    </>
  )
}
