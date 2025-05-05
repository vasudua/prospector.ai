"use client"

import { useState } from 'react'
import { MagnifyingGlassIcon, ChevronRightIcon, FunnelIcon } from '@heroicons/react/24/outline'

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

export default function SearchFilters() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedIndustry, setSelectedIndustry] = useState('')
  const [selectedSize, setSelectedSize] = useState('')
  const [selectedCountry, setSelectedCountry] = useState('')
  const [showFilters, setShowFilters] = useState(false)

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Trigger search logic
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
            className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-10 pr-12 py-3 sm:text-base border border-gray-300 rounded-lg shadow-sm bg-white placeholder-gray-300 text-black"
            placeholder="What can I help you with?"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <button
            type="submit"
            className="absolute inset-y-0 right-0 flex items-center px-3 text-indigo-600 hover:text-indigo-800 focus:outline-none"
            aria-label="Search"
          >
            <ChevronRightIcon className="h-6 w-6" />
          </button>
        </div>
      </form>

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
              <option value="" className="text-gray-300">All Industries</option>
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
              <option value="" className="text-gray-300">Any Size</option>
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
              placeholder="All Countries"
              value={selectedCountry}
              onChange={(e) => setSelectedCountry(e.target.value)}
            />
          </div>
        </div>
      )}
    </div>
  )
} 