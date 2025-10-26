/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://businessthis.com/api',
  },
  images: {
    domains: ['localhost', 'businessthis.com'],
  },
  output: 'export',
  trailingSlash: true,
  distDir: 'out',
  // Note: Removed generic /api rewrites to avoid proxying NextAuth internal routes.
}

module.exports = nextConfig
