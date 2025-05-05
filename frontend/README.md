# Frontend - Searcher

The frontend application for Searcher built with Next.js, React 19, and TailwindCSS.

## Technology Stack

- **Framework**: Next.js 15.3
- **UI Library**: React 19
- **Styling**: TailwindCSS 4
- **State Management**: React Query (TanStack Query)
- **Form Handling**: React Hook Form + Zod validation
- **UI Components**: Radix UI, Headless UI
- **HTTP Client**: Axios

## Development

### Prerequisites

- Node.js (latest LTS version)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server with Turbopack
npm run dev
```

### Build for Production

```bash
# Create production build
npm run build

# Start production server
npm start
```

## Folder Structure

- `src/`: Main source code
  - `app/`: Next.js app router
  - `components/`: Reusable UI components
  - `lib/`: Utility functions and shared code
  - `types/`: TypeScript type definitions
  - `hooks/`: Custom React hooks
  - `services/`: API service functions

## Linting

```bash
npm run lint
```

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following variables:

```
NEXT_PUBLIC_API_URL=http://localhost:5001
```

## Testing

[Add testing instructions when implemented] 