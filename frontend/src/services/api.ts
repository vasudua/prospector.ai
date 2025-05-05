// API Service for backend communication
// Provides methods for all backend API endpoints

import { API_CONFIG, replaceUrlParams } from '@/config';

// Types
export interface Company {
  id: string;
  name: string;
  website?: string;
  founded?: string;
  size?: string;
  locality?: string;
  region?: string;
  country?: string;
  industry?: string;
  linkedin_url?: string;
  description?: string;
  ai_summary?: string;
}

export interface SavedCompany {
  id: string;
  company_id: string;
  user_id: string;
  notes?: string;
  saved_at: string;
  company: Company;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  pages: number;
  current_page: number;
}

// API Error handling
class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

// Default fetch options with CORS support
const defaultFetchOptions: RequestInit = {
  mode: 'cors',
  credentials: 'same-origin',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
};

// Helper function to handle API responses
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    const errorMessage = errorData.error || `API request failed with status ${response.status}`;
    throw new ApiError(errorMessage, response.status);
  }
  
  const jsonResponse = await response.json();
  
  // Handle the nested data structure from the API
  if (jsonResponse.status === 'success' && jsonResponse.data !== undefined) {
    return jsonResponse.data as T;
  }
  
  return jsonResponse as T;
}

// Safe fetch wrapper with better error handling
async function safeFetch(url: string, options?: RequestInit): Promise<Response> {
  try {
    const mergedOptions = {
      ...defaultFetchOptions,
      ...options,
      headers: {
        ...defaultFetchOptions.headers,
        ...(options?.headers || {})
      }
    };
    
    return await fetch(url, mergedOptions);
  } catch (error) {
    console.error(`Network request failed to ${url}:`, error);
    if (error instanceof TypeError && error.message === 'Failed to fetch') {
      throw new ApiError(
        `Cannot connect to the server at ${API_CONFIG.BASE_URL}. Please check if the backend is running.`, 
        0
      );
    }
    throw error;
  }
}

// Companies API
export const companiesApi = {
  /**
   * Search companies with filters
   */
  async searchCompanies(params: {
    q?: string;
    page?: number;
    per_page?: number;
    industry?: string;
    country?: string;
    region?: string;
    size?: string;
    founded_from?: number;
    founded_to?: number;
  }): Promise<PaginatedResponse<Company> & { sql_query?: string }> {
    const queryParams = new URLSearchParams();
    
    // Add all valid params to query string
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        queryParams.append(key, value.toString());
      }
    });
    
    console.log(`API_CONFIG.BASE_URL: ${API_CONFIG.BASE_URL}`);
    console.log(`Making API request to: ${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.COMPANY_SEARCH}?${queryParams.toString()}`);
    
    const response = await safeFetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.COMPANY_SEARCH}?${queryParams.toString()}`);
    const data = await handleResponse<{
      companies: Company[], 
      total: number, 
      pages: number, 
      current_page: number,
      sql_query?: string
    }>(response);
    
    return {
      items: data.companies,
      total: data.total,
      pages: data.pages,
      current_page: data.current_page,
      sql_query: data.sql_query
    };
  },
  
  /**
   * Get a single company by ID
   */
  async getCompany(id: string): Promise<Company> {
    const url = replaceUrlParams(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.COMPANY_DETAIL}`, { id });
    const response = await safeFetch(url);
    return handleResponse<Company>(response);
  }
};

// Saved Companies API
export const savedCompaniesApi = {
  /**
   * Get saved companies for a user
   */
  async getSavedCompanies(params: { user_id?: string, page?: number, per_page?: number } = {}): Promise<PaginatedResponse<SavedCompany>> {
    const queryParams = new URLSearchParams();
    
    // Add all valid params to query string
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, value.toString());
      }
    });
    
    const response = await safeFetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SAVED_COMPANIES}?${queryParams.toString()}`);
    const data = await handleResponse<{
      saved_companies: SavedCompany[], 
      total: number, 
      pages: number, 
      current_page: number
    }>(response);
    
    return {
      items: data.saved_companies,
      total: data.total,
      pages: data.pages,
      current_page: data.current_page
    };
  },
  
  /**
   * Save a company
   */
  async saveCompany(params: { company_id: string, user_id?: string, notes?: string }): Promise<SavedCompany> {
    const response = await safeFetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SAVED_COMPANIES}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    });
    
    const data = await handleResponse<{ success: boolean, saved_company: SavedCompany }>(response);
    return data.saved_company;
  },
  
  /**
   * Delete a saved company
   */
  async deleteSavedCompany(id: string): Promise<boolean> {
    const url = replaceUrlParams(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SAVED_COMPANY_DETAIL}`, { id });
    const response = await safeFetch(url, {
      method: 'DELETE'
    });
    
    const data = await handleResponse<{ success: boolean }>(response);
    return data.success;
  },
  
  /**
   * Update a saved company's notes
   */
  async updateSavedCompany(id: string, params: { notes?: string }): Promise<SavedCompany> {
    const url = replaceUrlParams(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.SAVED_COMPANY_DETAIL}`, { id });
    const response = await safeFetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    });
    
    const data = await handleResponse<{ success: boolean, saved_company: SavedCompany }>(response);
    return data.saved_company;
  }
};

// Enrichment API
export const enrichmentApi = {
  /**
   * Enrich a company with AI
   */
  async enrichCompany(companyId: string): Promise<Company> {
    const url = replaceUrlParams(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.ENRICH_COMPANY}`, { id: companyId });
    const response = await safeFetch(url, {
      method: 'POST'
    });
    
    const data = await handleResponse<{ success: boolean, company: Company }>(response);
    return data.company;
  },
  
  /**
   * Batch enrich multiple companies
   */
  async batchEnrichCompanies(companyIds: string[]): Promise<Company[]> {
    const response = await safeFetch(`${API_CONFIG.BASE_URL}${API_CONFIG.ENDPOINTS.BATCH_ENRICH}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ company_ids: companyIds })
    });
    
    const data = await handleResponse<{ success: boolean, enriched_companies: Company[] }>(response);
    return data.enriched_companies;
  }
}; 