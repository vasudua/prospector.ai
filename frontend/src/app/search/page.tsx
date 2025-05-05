"use client"

import { Suspense } from 'react'
import SearchPageContent from '@/components/search/SearchPageContent'

export default function SearchPage() {
  return (
    <div className="space-y-8">
      <Suspense fallback={<div className="flex justify-center min-h-[60vh] items-center flex-col">
        <div className="w-full max-w-2xl h-48 bg-gray-100 animate-pulse rounded-lg"></div>
      </div>}>
        <SearchPageContent />
      </Suspense>
    </div>
  )
} 