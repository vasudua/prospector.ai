import SearchFilters from '@/components/search/SearchFilters'
import CompanyResults from '@/components/search/CompanyResults'

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="flex justify-center">
        <div className="w-full max-w-2xl">
          <SearchFilters />
        </div>
      </div>
      <div>
        <CompanyResults />
      </div>
    </div>
  )
}
