import Link from 'next/link'
import { BookmarkIcon } from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Saved Prospects', href: '/saved', icon: BookmarkIcon },
]

export default function Navbar() {
  return (
    <nav className="bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <Link 
              href="/"
              className="flex flex-shrink-0 items-center"
            >
              <span className="text-2xl" aria-label="Rocket">🚀</span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
                >
                  <item.icon className="mr-2 h-5 w-5" />
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
} 