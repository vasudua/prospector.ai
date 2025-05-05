"use client"

import { useEffect, useState } from 'react'
import { TrashIcon } from '@heroicons/react/24/outline'
import { Company, SavedCompany, savedCompaniesApi } from '@/services/api'

export default function SavedCompanies() {
  const [savedCompanies, setSavedCompanies] = useState<SavedCompany[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState<string | null>(null)
  const [pagination, setPagination] = useState({
    currentPage: 1,
    totalPages: 1,
    totalItems: 0,
    perPage: 10
  })

  const fetchSavedCompanies = async (page = 1) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await savedCompaniesApi.getSavedCompanies({
        page,
        per_page: pagination.perPage
      })
      
      setSavedCompanies(response.items)
      setPagination({
        currentPage: response.current_page,
        totalPages: response.pages,
        totalItems: response.total,
        perPage: pagination.perPage
      })
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch saved companies';
      setError(errorMessage)
      console.error('Error fetching saved companies:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchSavedCompanies()
  }, [])

  const handleRemove = async (savedId: string) => {
    setDeleting(savedId)
    try {
      const success = await savedCompaniesApi.deleteSavedCompany(savedId)
      if (success) {
        setSavedCompanies(savedCompanies.filter(company => company.id !== savedId))
      }
    } catch (err) {
      console.error('Failed to remove company:', err)
      setError(err instanceof Error ? err.message : 'Failed to remove company')
    } finally {
      setDeleting(null)
    }
  }

  if (loading && savedCompanies.length === 0) {
    return (
      <div className="bg-white shadow-sm rounded-lg p-8 text-center">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-indigo-500 mx-auto"></div>
        <p className="mt-2 text-gray-600">Loading saved companies...</p>
      </div>
    )
  }

  if (error && savedCompanies.length === 0) {
    const isConnectionError = typeof error === 'string' && (
      error.includes('Cannot connect to the server') || 
      error.includes('Failed to fetch') ||
      error.includes('Network Error')
    );

    return (
      <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-lg">
        <p className="font-bold mb-2">Error:</p>
        <p className="mb-4">{error}</p>
        {isConnectionError && (
          <div className="mt-2 bg-yellow-50 p-3 border border-yellow-200 rounded">
            <p className="text-yellow-800 font-medium">Backend Connection Issues:</p>
            <ol className="list-decimal ml-5 mt-2 text-yellow-800">
              <li className="mb-2">Make sure the backend server is running</li>
              <li className="mb-2">Check if the backend API is correctly configured</li>
              <li>Check browser console for CORS-related errors</li>
            </ol>
          </div>
        )}
        <div className="mt-4 flex flex-col sm:flex-row gap-4">
          <button 
            onClick={() => fetchSavedCompanies()}
            className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (savedCompanies.length === 0) {
    return (
      <div className="bg-white shadow-sm rounded-lg p-8 text-center">
        <p className="text-gray-600">You haven't saved any companies yet.</p>
      </div>
    )
  }

  return (
    <div className="bg-white shadow-sm rounded-lg">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Company
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Description
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Saved Date
              </th>
              <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {savedCompanies.map((saved) => (
              <tr key={saved.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{saved.company.name}</div>
                      <div className="text-sm text-gray-500">{saved.company.website}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div className="text-sm text-gray-900 max-w-md">
                    {saved.company.ai_summary || saved.company.description || 'No description available'}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-900">
                    {new Date(saved.saved_at).toLocaleDateString()}
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    onClick={() => handleRemove(saved.id)}
                    disabled={deleting === saved.id}
                    className={`inline-flex items-center px-2.5 py-1.5 border border-transparent text-xs font-medium rounded ${
                      deleting === saved.id
                        ? 'bg-red-100 text-red-400 cursor-not-allowed'
                        : 'text-red-700 bg-red-100 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500'
                    }`}
                  >
                    {deleting === saved.id ? (
                      <span className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-red-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Removing...
                      </span>
                    ) : (
                      <>
                        <TrashIcon className="-ml-0.5 mr-2 h-4 w-4" aria-hidden="true" />
                        Remove
                      </>
                    )}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Pagination - only show if we have multiple pages */}
      {pagination.totalPages > 1 && (
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex-1 flex justify-between sm:hidden">
              <button
                onClick={() => fetchSavedCompanies(pagination.currentPage - 1)}
                disabled={pagination.currentPage === 1}
                className={`relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                  pagination.currentPage === 1
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Previous
              </button>
              <button
                onClick={() => fetchSavedCompanies(pagination.currentPage + 1)}
                disabled={pagination.currentPage === pagination.totalPages}
                className={`ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md ${
                  pagination.currentPage === pagination.totalPages
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                Next
              </button>
            </div>
            <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div>
                <p className="text-sm text-gray-700">
                  Showing <span className="font-medium">{(pagination.currentPage - 1) * pagination.perPage + 1}</span> to{' '}
                  <span className="font-medium">
                    {Math.min(pagination.currentPage * pagination.perPage, pagination.totalItems)}
                  </span>{' '}
                  of <span className="font-medium">{pagination.totalItems}</span> results
                </p>
              </div>
              <div>
                <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button
                    onClick={() => fetchSavedCompanies(pagination.currentPage - 1)}
                    disabled={pagination.currentPage === 1}
                    className={`relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium ${
                      pagination.currentPage === 1
                        ? 'text-gray-300 cursor-not-allowed'
                        : 'text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    <span className="sr-only">Previous</span>
                    <span aria-hidden="true">&laquo;</span>
                  </button>
                  
                  {/* Current page indicator instead of all page buttons */}
                  <span className="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700">
                    Page {pagination.currentPage} of {pagination.totalPages}
                  </span>
                  
                  <button
                    onClick={() => fetchSavedCompanies(pagination.currentPage + 1)}
                    disabled={pagination.currentPage === pagination.totalPages}
                    className={`relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium ${
                      pagination.currentPage === pagination.totalPages
                        ? 'text-gray-300 cursor-not-allowed'
                        : 'text-gray-500 hover:bg-gray-50'
                    }`}
                  >
                    <span className="sr-only">Next</span>
                    <span aria-hidden="true">&raquo;</span>
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 