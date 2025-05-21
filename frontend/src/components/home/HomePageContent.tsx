"use client"

import { useState } from 'react'
import CompanyResults from '@/components/search/CompanyResults'
import SearchFilters from '@/components/search/SearchFilters'

export default function HomePageContent() {
  const [searchInitiated, setSearchInitiated] = useState(false)
  const [searchParams, setSearchParams] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)

  const handleSearch = (params: Record<string, string>) => {
    setIsLoading(true)
    // Create a fresh object to avoid reference issues
    const newParams = {...params}
    setSearchParams(newParams)
    setSearchInitiated(true)
  }

  return (
    <>
      <div className={`flex flex-col items-center justify-center ${!searchInitiated ? 'min-h-[60vh]' : ''} text-center`}>
        <div className="w-full max-w-2xl">
          <SearchFilters onSearch={handleSearch} isLoading={isLoading} />
        </div>
      </div>
      
      {searchInitiated && (
        <div className="mt-8"> {/* Added margin-top for spacing when results appear */}
          <CompanyResults 
            searchParams={searchParams} 
            onLoadingChange={(loading) => setIsLoading(loading)}
          />
        </div>
      )}
    </>
  )
} 