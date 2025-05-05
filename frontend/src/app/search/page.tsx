"use client"

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import CompanyResults from '@/components/search/CompanyResults'
import SearchFilters from '@/components/search/SearchFilters'

export default function SearchPage() {
  const searchParams = useSearchParams()
  const [normalizedParams, setNormalizedParams] = useState<Record<string, string>>({})
  const [searchInitiated, setSearchInitiated] = useState(false)
  
  // Convert searchParams to a regular object on initial load
  useEffect(() => {
    const params: Record<string, string> = {}
    searchParams.forEach((value, key) => {
      params[key] = value
    })
    
    const hasValidParams = Object.keys(params).length > 0 && 
                            Object.values(params).some(value => value)
    
    setNormalizedParams(params)
    setSearchInitiated(hasValidParams)
  }, [searchParams])

  const handleSearch = (params: Record<string, string>) => {
    setNormalizedParams(params)
    setSearchInitiated(true)
  }

  return (
    <div className="space-y-8">
      <div className={`flex justify-center ${!searchInitiated ? 'min-h-[60vh] items-center flex-col' : ''}`}>
        {!searchInitiated && (
          <h1 className="text-3xl font-bold text-gray-900 mb-8">🚀 prospector.ai 🚀</h1>
        )}
        <div className="w-full max-w-2xl">
          <SearchFilters onSearch={handleSearch} />
        </div>
      </div>
      
      {searchInitiated && (
        <div>
          <CompanyResults searchParams={normalizedParams} />
        </div>
      )}
    </div>
  )
} 