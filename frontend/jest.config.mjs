/** @type {import('ts-jest').JestConfigWithTsJest} */
export default {
  testEnvironment: 'jest-environment-jsdom',
  preset: 'ts-jest/presets/default-esm', // or other ESM preset
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy', // Mock CSS imports
  },
  transform: {
    // '^.+\\.[tj]sx?$' to process js/ts/jsx/tsx files with `ts-jest`
    // '^.+\\.m?[tj]sx?$' to process js/ts/jsx/tsx/mjs/mts files with `ts-jest`
    '^.+\\.tsx?$': [
      'ts-jest',
      {
        useESM: true,
        tsconfig: 'tsconfig.jest.json', // Use a separate tsconfig for tests
      },
    ],
  },
  setupFilesAfterEnv: ['<rootDir>/jest.setup.ts'], // For @testing-library/jest-dom
  testPathIgnorePatterns: ['<rootDir>/.next/', '<rootDir>/node_modules/'],
  moduleFileExtensions: ['ts', 'tsx', 'js', 'mjs', 'jsx', 'json', 'node'],
  globals: {
    'ts-jest': {
      useESM: true,
    },
  },
};
