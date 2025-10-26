# BusinessThis - Next.js Frontend

A modern financial planning application built with Next.js, TypeScript, and Supabase.

## Features

### Core Features
- **Safe Spending Calculator**: Calculate daily, weekly, and monthly safe spending amounts
- **Financial Health Score**: Get a 0-100 score based on your financial situation
- **Savings Goals Tracking**: Set and monitor multiple savings goals
- **Financial Profile Management**: Comprehensive financial data management
- **Real-time Analytics**: Visual charts and insights

### Premium Features (Subscription-based)
- **Advanced Analytics**: Detailed financial reports and projections
- **AI Financial Coaching**: Personalized financial advice
- **Multiple Savings Goals**: Track unlimited goals (vs 1 for free users)
- **PDF/Excel Export**: Export your financial data
- **Email Notifications**: Automated financial tips and reminders

## Technology Stack

### Frontend
- **Next.js**: React framework with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Radix UI**: Accessible component library
- **Recharts**: Data visualization
- **NextAuth.js**: Authentication

### Backend & Database
- **Supabase**: PostgreSQL database + Auth + API
- **Stripe**: Payment processing
- **OpenAI**: AI-powered financial coaching
- **SendGrid**: Email notifications

### Deployment
- **Vercel**: Full-stack deployment platform
- **Environment**: Production-ready with automatic deployments

## Quick Start

### Prerequisites
- Node.js 18+
- Supabase account
- Stripe account (for payments)
- OpenAI API key (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BusinessThis
   ```

2. **Install dependencies**
   ```bash
   cd nextjs-app
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your Supabase and API keys
   ```

4. **Set up Supabase**
   - Create a new Supabase project
   - Run the database schema from `database/schema-fixed.sql`
   - Get your project URL and anon key

5. **Run the development server**
   ```bash
   npm run dev
   ```

### Access the application

- **Frontend**: http://localhost:3000
- **Production**: https://businessthis.com (after deployment)

## Project Structure

```
nextjs-app/
├── src/
│   ├── app/                 # Next.js app router
│   │   ├── auth/           # Authentication pages
│   │   ├── dashboard/      # Dashboard pages
│   │   └── api/            # API routes
│   ├── components/          # Reusable UI components
│   ├── lib/                # Utilities and configurations
│   │   ├── supabase.ts     # Supabase client
│   │   ├── api-client.ts   # API client
│   │   └── auth.ts         # NextAuth configuration
│   ├── store/              # State management
│   └── types/               # TypeScript types
├── public/                  # Static assets
├── package.json
├── next.config.js
├── tailwind.config.js
└── tsconfig.json
```

## Environment Variables

Create a `.env.local` file with the following variables:

```env
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_key

# Optional: Stripe for payments
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key

# Optional: OpenAI for AI features
OPENAI_API_KEY=sk-your_openai_api_key
```

## Deployment

### Deploy to Vercel

1. **Connect your repository to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Set the root directory to `nextjs-app`

2. **Configure environment variables**
   - Add all environment variables in Vercel dashboard
   - Set `NEXTAUTH_URL` to your production domain

3. **Deploy**
   - Vercel will automatically deploy on every push to main
   - Your app will be available at `https://your-app.vercel.app`

### Custom Domain

1. **Add custom domain in Vercel**
   - Go to your project settings
   - Add `businessthis.com` as custom domain
   - Configure DNS records as instructed

2. **Update environment variables**
   - Set `NEXTAUTH_URL=https://businessthis.com`
   - Update any other domain-specific configurations

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Structure

- **Pages**: Use Next.js app router in `src/app/`
- **Components**: Reusable UI components in `src/components/`
- **API**: Server-side logic in `src/app/api/`
- **Styling**: Tailwind CSS with custom components
- **State**: Zustand for client-side state management

## API Integration

The app uses Supabase for all backend functionality:

- **Authentication**: Supabase Auth with NextAuth.js
- **Database**: Direct Supabase client queries
- **Real-time**: Supabase real-time subscriptions
- **Storage**: Supabase storage for file uploads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
