import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import HomePageContent from './HomePageContent';
import { companiesApi } from '@/services/api'; // To mock

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    refresh: jest.fn(),
  }),
  useSearchParams: () => ({
    get: jest.fn(),
  }),
  usePathname: jest.fn(),
}));

// Mock the companiesApi.searchCompanies function
jest.mock('@/services/api', () => ({
  ...jest.requireActual('@/services/api'), // Import and retain default exports
  companiesApi: {
    searchCompanies: jest.fn(),
  },
  // Mock other api services if they are called and need mocking
  enrichmentApi: {
    enrichCompany: jest.fn(),
  },
  savedCompaniesApi: {
    getSavedCompanies: jest.fn(),
    saveCompany: jest.fn(),
    deleteSavedCompany: jest.fn(),
  },
}));

describe('HomePageContent', () => {
  beforeEach(() => {
    // Reset mocks before each test
    (companiesApi.searchCompanies as jest.Mock).mockReset();
  });

  test('renders initial layout correctly and old elements are not present', () => {
    render(<HomePageContent />);

    // Assert search input is visible (from SearchFilters)
    expect(screen.getByPlaceholderText(/Search for companies/i)).toBeInTheDocument();

    // Assert old title is NOT present
    expect(screen.queryByRole('heading', { name: /🚀 prospector.ai 🚀/i })).not.toBeInTheDocument();

    // Assert old introductory paragraph is NOT present
    expect(screen.queryByText(/Search for companies by name, industry, location, and more./i)).not.toBeInTheDocument();
  });

  test('initiates search and displays results', async () => {
    // Mock the API response for this test
    (companiesApi.searchCompanies as jest.Mock).mockResolvedValue({
      items: [{ id: '1', name: 'Test Company Inc.', industry: 'Tech', /* other fields */ }],
      total: 1,
      pages: 1,
      current_page: 1,
    });

    render(<HomePageContent />);

    // Simulate typing into the search input
    const searchInput = screen.getByPlaceholderText(/Search for companies/i);
    fireEvent.input(searchInput, { target: { value: 'test query' } });

    const searchButton = screen.getByRole('button', { name: /Search/i }); 
    
    // Wait for the button to be enabled (react-hook-form state update)
    await waitFor(() => {
      expect(searchButton).not.toBeDisabled();
    });
    fireEvent.click(searchButton);

    // Assert that CompanyResults displays the "X Companies Found" heading
    // It might take a moment for the results to appear due to async operations
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /1 Companies Found/i })).toBeInTheDocument();
    });

    // Optionally, assert that specific company data is displayed
    expect(screen.getByText('Test Company Inc.')).toBeInTheDocument();
  });

  test('displays no results message when API returns empty items', async () => {
    (companiesApi.searchCompanies as jest.Mock).mockResolvedValue({
      items: [],
      total: 0,
      pages: 1,
      current_page: 1,
    });
  
    render(<HomePageContent />);
  
    const searchInput = screen.getByPlaceholderText(/Search for companies/i);
    fireEvent.input(searchInput, { target: { value: 'empty search' } });
  
    const searchButton = screen.getByRole('button', { name: /Search/i });

    // Wait for the button to be enabled
    await waitFor(() => {
      expect(searchButton).not.toBeDisabled();
    });
    fireEvent.click(searchButton);
  
    await waitFor(() => {
      expect(screen.getByText(/No companies found. Try adjusting your search criteria./i)).toBeInTheDocument();
    });
  });

  test('handles API error during search', async () => {
    (companiesApi.searchCompanies as jest.Mock).mockRejectedValue(new Error('API Error'));

    render(<HomePageContent />);

    const searchInput = screen.getByPlaceholderText(/Search for companies/i);
    fireEvent.input(searchInput, { target: { value: 'error search' } });

    const searchButton = screen.getByRole('button', { name: /Search/i });

    // Wait for the button to be enabled
    await waitFor(() => {
      expect(searchButton).not.toBeDisabled();
    });
    fireEvent.click(searchButton);

    await waitFor(() => {
      // Assuming the error is displayed to the user. 
      // The actual text depends on error handling in CompanyResults.tsx
      expect(screen.getByText(/Failed to fetch companies/i)).toBeInTheDocument();
    });
  });

});
