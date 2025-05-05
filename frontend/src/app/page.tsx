"use client"

import { useState } from 'react'
import CompanyResults from '@/components/search/CompanyResults'
import SearchFilters from '@/components/search/SearchFilters'

export default function Home() {
  const [searchInitiated, setSearchInitiated] = useState(false)
  const [searchParams, setSearchParams] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = (params: Record<string, string>) => {
    setIsLoading(true)
    setSearchParams(params)
    setSearchInitiated(true)
    // The loading state will be handled by CompanyResults
  }

  return (
    <div className="space-y-8">
      <div className={`flex flex-col items-center justify-center ${!searchInitiated ? 'min-h-[60vh]' : ''} text-center`}>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">🚀 prospector.ai 🚀</h1>
        <p className="text-gray-600 mb-8 max-w-lg">
          Search for companies by name, industry, location, and more. Use the filters to narrow down your results.
        </p>
        <div className="w-full max-w-2xl">
          <SearchFilters onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>
      
      {searchInitiated && (
        <div>
          <CompanyResults 
            searchParams={searchParams} 
            onLoadingChange={(loading) => setIsLoading(loading)}
          />
        </div>
      )}
    </div>
  )
}

