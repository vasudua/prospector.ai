import SavedCompanies from '@/components/saved/SavedCompanies'

export default function SavedPage() {
  return (
    <div className="space-y-6">
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900">Saved Prospects</h1>
          <p className="mt-2 text-sm text-gray-700">
            View and manage your saved companies. These are the companies you&apos;ve marked for follow-up.
          </p>
        </div>
      </div>

      <SavedCompanies />
    </div>
  )
} 