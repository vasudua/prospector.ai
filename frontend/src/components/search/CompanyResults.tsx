"use client"

import React, { useEffect, useState } from 'react'
import { BookmarkIcon, SparklesIcon, XMarkIcon } from '@heroicons/react/24/outline'
import { Company, companiesApi, enrichmentApi, savedCompaniesApi } from '@/services/api'
import SearchFilters from './SearchFilters';

export default function CompanyResults({ searchParams = {} }: { searchParams?: Record<string, any> }) {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    perPage: 36
  })
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null)
  const [isEnriching, setIsEnriching] = useState(false)
  const [enrichingId, setEnrichingId] = useState<string | null>(null)
  const [saving, setSaving] = useState<string | null>(null)
  const [showModal, setShowModal] = useState(false)

  const fetchCompanies = async (page = 1) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await companiesApi.searchCompanies({
        ...searchParams,
        page,
        per_page: pagination.perPage
      })
      
      setCompanies(response.items)
      setPagination({
        currentPage: response.current_page,
        totalPages: response.pages,
        totalItems: response.total,
        perPage: pagination.perPage
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch companies';
      setError(errorMessage)
      console.error('Error fetching companies:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (params: Record<string, string>) => {
    // Update search params and fetch
    const newParams = {...searchParams, ...params, page: 1}
    // Need to update the searchParams reference to avoid rendering duplicate search bars
    Object.assign(searchParams, newParams)
    fetchCompanies(1)
  }
  
  useEffect(() => {
    fetchCompanies(parseInt(searchParams.page as string) || 1)
  }, [searchParams])

  const enrichCompany = async (companyId: string) => {
    if (isEnriching) return
    
    setIsEnriching(true)
    setEnrichingId(companyId)
    
    try {
      const enrichedCompany = await enrichmentApi.enrichCompany(companyId)
      
      // Update company in the list
      setCompanies(companies.map(company => 
        company.id === companyId ? enrichedCompany : company
      ))
      
      // Update selected company if this is the one in the modal
      if (selectedCompany && selectedCompany.id === companyId) {
        setSelectedCompany(enrichedCompany)
      }
    } catch (err) {
      console.error('Error enriching company:', err)
    } finally {
      setIsEnriching(false)
      setEnrichingId(null)
    }
  }

  const saveCompany = async (companyId: string) => {
    if (saving) return
    
    setSaving(companyId)
    
    try {
      // Placeholder for user ID - in a real app this would come from auth
      const userId = '1' 
      
      await savedCompaniesApi.saveCompany({
        company_id: companyId,
        user_id: userId
      })
      
      // Show success message or update UI
    } catch (err) {
      console.error('Error saving company:', err)
    } finally {
      setSaving(null)
    }
  }

  const handlePageChange = (newPage: number) => {
    if (newPage === pagination.currentPage) return
    fetchCompanies(newPage)
  }

  const viewCompanyDetails = (company: Company) => {
    setSelectedCompany(company)
    setShowModal(true)
  }

  const closeCompanyDetails = () => {
    setShowModal(false)
    setSelectedCompany(null)
  }

  return (
    <div className="py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Only render SearchFilters if there are no companies loaded and we're not loading */}
        {companies.length === 0 && !loading && (
          <div className="mb-6">
            <SearchFilters onSearch={handleSearch} />
          </div>
        )}
        
        {/* Results Header */}
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {loading ? 'Loading...' : `${pagination.totalItems} Companies Found`}
          </h2>
          {error && (
            <p className="mt-2 text-red-600">{error}</p>
          )}
        </div>
        
        {/* Company List */}
        {companies.length > 0 ? (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {companies.map(company => (
              <div 
                key={company.id} 
                className="bg-white overflow-hidden shadow rounded-lg divide-y divide-gray-200"
              >
                <div className="px-4 py-5 sm:px-6">
                  <div className="flex justify-between">
                    <h3 className="text-lg font-medium text-gray-900 truncate">{company.name}</h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => saveCompany(company.id)}
                        className={`${saving === company.id ? 'animate-pulse' : ''} inline-flex items-center p-1 border border-transparent rounded-full text-gray-500 hover:bg-gray-100 focus:outline-none`}
                      >
                        <BookmarkIcon className="h-6 w-6" />
                      </button>
                    </div>
                  </div>
                  <p className="mt-1 text-sm text-gray-500 truncate">
                    {company.industry || 'Industry not specified'}
                  </p>
                  <p className="mt-1 text-sm text-gray-500">
                    {[company.locality, company.region, company.country]
                      .filter(Boolean)
                      .join(', ') || 'Location not specified'}
                  </p>
                </div>
                <div className="px-4 py-4 sm:px-6">
                  <div className="text-sm">
                    {company.ai_summary ? (
                      <p className="text-gray-700">{company.ai_summary}</p>
                    ) : (
                      <div className="flex justify-between items-center">
                        <span className="text-gray-500 italic">No summary available</span>
                        <button
                          onClick={() => enrichCompany(company.id)}
                          disabled={isEnriching && enrichingId === company.id}
                          className={`inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none ${isEnriching && enrichingId === company.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                          <SparklesIcon className={`-ml-1 mr-2 h-4 w-4 ${isEnriching && enrichingId === company.id ? 'animate-spin' : ''}`} />
                          Enrich
                        </button>
                      </div>
                    )}
                  </div>
                  <div className="mt-2 flex justify-between items-center">
                    <div className="text-xs text-gray-500">
                      {company.founded ? `Founded: ${company.founded}` : ''}
                      {company.size ? (company.founded ? ' · ' : '') + `Size: ${company.size}` : ''}
                    </div>
                    <button
                      onClick={() => viewCompanyDetails(company)}
                      className="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-xs font-medium rounded text-gray-700 bg-white hover:bg-gray-50 focus:outline-none"
                    >
                      Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          !loading && (
            <div className="text-center py-10">
              <p className="text-gray-500">No companies found. Try adjusting your search criteria.</p>
            </div>
          )
        )}
        
        {/* Pagination */}
        {pagination.totalPages > 1 && (
          <div className="mt-6 flex justify-center">
            <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
              <button
                onClick={() => handlePageChange(pagination.currentPage - 1)}
                disabled={pagination.currentPage === 1}
                className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                  pagination.currentPage === 1
                    ? 'text-gray-300 cursor-not-allowed'
                    : 'text-gray-500 hover:bg-gray-50'
                }`}
              >
                <span className="sr-only">Previous</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </button>
              
              {/* Page Numbers */}
              {[...Array(pagination.totalPages)].map((_, i) => {
                const pageNum = i + 1
                const showEllipsisBefore = pageNum === 2 && pagination.currentPage > 4
                const showEllipsisAfter = pageNum === pagination.totalPages - 1 && pagination.currentPage < pagination.totalPages - 3
                
                // Only show certain page numbers to avoid cluttering
                const shouldShowPage = 
                  pageNum === 1 || 
                  pageNum === pagination.totalPages ||
                  (pageNum >= pagination.currentPage - 1 && pageNum <= pagination.currentPage + 1) ||
                  pagination.totalPages <= 7 ||
                  (pagination.currentPage <= 4 && pageNum <= 5) ||
                  (pagination.currentPage >= pagination.totalPages - 3 && pageNum >= pagination.totalPages - 4)
                
                if (!shouldShowPage) return null
                
                return (
                  <React.Fragment key={pageNum}>
                    {showEllipsisBefore && (
                      <span key={`ellipsis-before-${pageNum}`} className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                        ...
                      </span>
                    )}
                    <button
                      onClick={() => handlePageChange(pageNum)}
                      aria-current={pagination.currentPage === pageNum ? 'page' : undefined}
                      className={`relative inline-flex items-center px-4 py-2 border text-sm font-medium ${
                        pagination.currentPage === pageNum
                          ? 'z-10 bg-indigo-50 border-indigo-500 text-indigo-600'
                          : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50'
                      }`}
                    >
                      {pageNum}
                    </button>
                    {showEllipsisAfter && (
                      <span key={`ellipsis-after-${pageNum}`} className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                        ...
                      </span>
                    )}
                  </React.Fragment>
                )
              })}
              
              <button
                onClick={() => handlePageChange(pagination.currentPage + 1)}
                disabled={pagination.currentPage === pagination.totalPages}
                className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                  pagination.currentPage === pagination.totalPages
                    ? 'text-gray-300 cursor-not-allowed'
                    : 'text-gray-500 hover:bg-gray-50'
                }`}
              >
                <span className="sr-only">Next</span>
                <svg className="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                  <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                </svg>
              </button>
            </nav>
          </div>
        )}
      
      {/* Company Details Modal */}
      {showModal && selectedCompany && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-auto">
            <div className="flex justify-between items-center border-b border-gray-200 px-6 py-4">
              <h2 className="text-xl font-semibold text-gray-900">{selectedCompany.name}</h2>
              <button
                onClick={closeCompanyDetails}
                className="text-gray-400 hover:text-gray-500 focus:outline-none"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            
            <div className="px-6 py-4 grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Company Website */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">Website</h3>
                <p className="mt-1">
                  {selectedCompany.website ? (
                    <a 
                      href={selectedCompany.website.startsWith('http') ? selectedCompany.website : `https://${selectedCompany.website}`} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-indigo-600 hover:text-indigo-800"
                    >
                      {selectedCompany.website}
                    </a>
                  ) : (
                    <span className="text-gray-400">Not available</span>
                  )}
                </p>
              </div>
              
              {/* Company Founded */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">Founded</h3>
                <p className="mt-1 text-gray-900">
                  {selectedCompany.founded || <span className="text-gray-400">Not available</span>}
                </p>
              </div>
              
              {/* Company Size */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">Size</h3>
                <p className="mt-1 text-gray-900">
                  {selectedCompany.size || <span className="text-gray-400">Not available</span>}
                </p>
              </div>
              
              {/* Company Industry */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">Industry</h3>
                <p className="mt-1 text-gray-900">
                  {selectedCompany.industry || <span className="text-gray-400">Not available</span>}
                </p>
              </div>
              
              {/* Company Location */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">Location</h3>
                <p className="mt-1 text-gray-900">
                  {[selectedCompany.locality, selectedCompany.region, selectedCompany.country]
                    .filter(Boolean)
                    .join(', ') || <span className="text-gray-400">Not available</span>}
                </p>
              </div>
              
              {/* LinkedIn */}
              <div>
                <h3 className="text-sm font-medium text-gray-500">LinkedIn</h3>
                <p className="mt-1">
                  {selectedCompany.linkedin_url ? (
                    <a 
                      href={selectedCompany.linkedin_url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-indigo-600 hover:text-indigo-800"
                    >
                      View LinkedIn Profile
                    </a>
                  ) : (
                    <span className="text-gray-400">Not available</span>
                  )}
                </p>
              </div>
              
              {/* AI Summary - Spans full width */}
              <div className="col-span-1 md:col-span-2 border-t border-gray-200 pt-4 mt-2">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="text-sm font-medium text-gray-500">AI-Generated Summary</h3>
                  {!selectedCompany.ai_summary && (
                    <button
                      onClick={() => enrichCompany(selectedCompany.id)}
                      disabled={isEnriching && enrichingId === selectedCompany.id}
                      className={`inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none ${isEnriching && enrichingId === selectedCompany.id ? 'opacity-50 cursor-not-allowed' : ''}`}
                    >
                      <SparklesIcon className={`-ml-1 mr-2 h-4 w-4 ${isEnriching && enrichingId === selectedCompany.id ? 'animate-spin' : ''}`} />
                      Generate Summary
                    </button>
                  )}
                </div>
                {selectedCompany.ai_summary ? (
                  <p className="text-gray-700">{selectedCompany.ai_summary}</p>
                ) : (
                  <p className="text-gray-400 italic">No AI summary available. Generate one to learn more about this company.</p>
                )}
              </div>
            </div>
            
            <div className="border-t border-gray-200 px-6 py-4 flex justify-end">
              <button
                type="button"
                onClick={() => saveCompany(selectedCompany.id)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none"
              >
                <BookmarkIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                Save Company
              </button>
            </div>
          </div>
        </div>
      )}
      </div>
    </div>
  )
} 