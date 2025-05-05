"use client"

import { useRouter, useSearchParams } from 'next/navigation'
import { useState, useEffect } from 'react'
import { MagnifyingGlassIcon, ChevronRightIcon, FunnelIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

const industries = [
  'Technology',
  'Healthcare',
  'Finance',
  'Manufacturing',
  'Retail',
  'Education',
  'Other',
]

const companySizes = [
  '1-10',
  '11-50',
  '51-200',
  '201-500',
  '501-1000',
  '1000+',
]

interface SearchFiltersProps {
  onSearch?: (params: Record<string, string>) => void;
}

export default function SearchFilters({ onSearch }: SearchFiltersProps) {
  const router = useRouter()
  const searchParams = useSearchParams()
  
  const [searchQuery, setSearchQuery] = useState(searchParams.get('q') || '')
  const [selectedIndustry, setSelectedIndustry] = useState(searchParams.get('industry') || '')
  const [selectedSize, setSelectedSize] = useState(searchParams.get('size') || '')
  const [selectedCountry, setSelectedCountry] = useState(searchParams.get('country') || '')
  const [showFilters, setShowFilters] = useState(false)
  const [validationError, setValidationError] = useState('')

  // Sync state with URL params if they change externally
  useEffect(() => {
    setSearchQuery(searchParams.get('q') || '')
    setSelectedIndustry(searchParams.get('industry') || '')
    setSelectedSize(searchParams.get('size') || '')
    setSelectedCountry(searchParams.get('country') || '')
  }, [searchParams])

  const validateSearch = () => {
    // If all fields are empty, show error
    if (!searchQuery && (!showFilters || (!selectedIndustry && !selectedSize && !selectedCountry))) {
      setValidationError('Please enter a search query or select at least one filter')
      return false
    }

    // If filter panel is open but no filters selected, show error
    if (showFilters && !selectedIndustry && !selectedSize && !selectedCountry) {
      setValidationError('Please select at least one filter when filter panel is open')
      return false
    }

    setValidationError('')
    return true
  }

  const isSearchEnabled = () => {
    return searchQuery.trim() !== '' || (showFilters && (selectedIndustry || selectedSize || selectedCountry))
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!validateSearch()) {
      return
    }
    
    // Create new URLSearchParams object
    const params: Record<string, string> = {}
    
    // Add query parameter if not empty
    if (searchQuery) params.q = searchQuery
    
    // Only include filter parameters if the filters panel is open
    if (showFilters) {
      if (selectedIndustry) params.industry = selectedIndustry
      if (selectedSize) params.size = selectedSize
      if (selectedCountry) params.country = selectedCountry
    }
    
    if (onSearch) {
      // Use the callback for homepage search
      onSearch(params)
    } else {
      // Navigate to the search page with the parameters (for other pages)
      const urlParams = new URLSearchParams()
      Object.entries(params).forEach(([key, value]) => {
        urlParams.set(key, value)
      })
      router.push(`/search?${urlParams.toString()}`)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.key === 'Enter' || e.key === 'Return') && isSearchEnabled()) {
      handleSearch(e)
    }
  }

  return (
    <div className="flex flex-col items-center gap-6 w-full">
      <form onSubmit={handleSearch} className="w-full flex justify-center">
        <div className="relative w-full max-w-xl">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
          </div>
          <input
            type="text"
            name="search"
            id="search"
            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 pr-12 py-3 sm:text-base border border-gray-300 bg-white rounded-lg shadow-sm placeholder-gray-300 text-black"
            placeholder="Search for companies (e.g., 'tech companies in Europe')"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            type="submit"
            className={`absolute inset-y-0 right-0 flex items-center px-3 ${
              isSearchEnabled()
                ? 'text-indigo-600 hover:text-indigo-800 cursor-pointer'
                : 'text-gray-300 cursor-not-allowed'
            } focus:outline-none`}
            aria-label="Search"
            disabled={!isSearchEnabled()}
          >
            <ChevronRightIcon className="h-6 w-6" />
          </button>
        </div>
      </form>

      {validationError && (
        <div className="w-full max-w-xl px-4 py-3 bg-red-50 text-red-700 border border-red-200 rounded-md flex items-center">
          <ExclamationTriangleIcon className="h-5 w-5 flex-shrink-0 mr-2" />
          <span>{validationError}</span>
        </div>
      )}

      <button
        type="button"
        className="flex items-center gap-2 text-sm font-medium text-indigo-600 hover:text-indigo-800 focus:outline-none"
        onClick={() => setShowFilters((prev) => !prev)}
        aria-expanded={showFilters}
      >
        <FunnelIcon className="h-5 w-5" /> Filters
        <span className={`transition-transform ${showFilters ? 'rotate-90' : ''}`}>▶</span>
      </button>

      {showFilters && (
        <div className="w-full flex flex-col sm:flex-row gap-4 justify-center bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
          <div className="flex-1 min-w-[150px]">
            <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-1">
              Industry
            </label>
            <select
              id="industry"
              name="industry"
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md text-black"
              value={selectedIndustry}
              onChange={(e) => setSelectedIndustry(e.target.value)}
            >
              <option value="" className="text-gray-300">Select Industry</option>
              {industries.map((industry) => (
                <option key={industry} value={industry}>
                  {industry}
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1 min-w-[150px]">
            <label htmlFor="size" className="block text-sm font-medium text-gray-700 mb-1">
              Company Size
            </label>
            <select
              id="size"
              name="size"
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md text-black"
              value={selectedSize}
              onChange={(e) => setSelectedSize(e.target.value)}
            >
              <option value="" className="text-gray-300">Select Size</option>
              {companySizes.map((size) => (
                <option key={size} value={size}>
                  {size} employees
                </option>
              ))}
            </select>
          </div>
          <div className="flex-1 min-w-[150px]">
            <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-1">
              Country
            </label>
            <input
              type="text"
              name="country"
              id="country"
              className="block w-full py-2 px-3 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm placeholder-gray-300 text-black"
              placeholder="Enter country"
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
            />
          </div>
        </div>
      )}
      
      <div className="w-full max-w-xl text-xs text-gray-500 flex flex-col">
        <p>
          <span className="font-medium">Tip:</span> You can use natural language like "tech companies in Europe founded after 2010"
        </p>
      </div>
    </div>
  )
} 