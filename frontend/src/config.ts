const defaultApiUrl = process.env.NEXT_PUBLIC_API_URL || 
  (typeof window !== 'undefined' ? 
    '' : // Empty string to use relative URLs with the Next.js proxy
    'http://localhost:5001');

// API settings
export const API_CONFIG = {
  // Print info about API URL configuration
  get BASE_URL() {
    const url = defaultApiUrl;
    // Log in development only
    if (process.env.NODE_ENV !== 'production') {
      console.log(`[Config] Using API URL: ${url || 'using Next.js proxy'}`);
      if (!process.env.NEXT_PUBLIC_API_URL) {
        console.log(`[Config] Note: Using Next.js proxy to connect to the backend. Set NEXT_PUBLIC_API_URL to override.`);
      }
    }
    return url;
  },
  ENDPOINTS: {
    // Company endpoints
    COMPANY_SEARCH: '/api/companies/search',
    COMPANY_DETAIL: '/api/companies/:id',
    
    // Saved company endpoints
    SAVED_COMPANIES: '/api/saved-companies/',
    SAVED_COMPANY_DETAIL: '/api/saved-companies/:id',
    
    // Enrichment endpoints
    ENRICH_COMPANY: '/api/enrichment/company/:id',
    BATCH_ENRICH: '/api/enrichment/batch',
  }
};

// Replace URL parameters with values
export const replaceUrlParams = (url: string, params: Record<string, string>) => {
  let result = url;
  Object.entries(params).forEach(([key, value]) => {
    result = result.replace(`:${key}`, value);
  });
  return result;
}; 