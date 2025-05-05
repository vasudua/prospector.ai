"use client"

import { Suspense } from 'react'
import HomePageContent from '@/components/home/HomePageContent'

export default function Home() {
  return (
    <div className="space-y-8">
      <Suspense fallback={<div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">🚀 prospector.ai 🚀</h1>
        <div className="w-full max-w-2xl h-12 bg-gray-100 animate-pulse rounded-lg"></div>
      </div>}>
        <HomePageContent />
      </Suspense>
    </div>
  )
}

