# BusinessThis Next.js Frontend

A modern, responsive Next.js application for BusinessThis financial planning platform.

## 🚀 Features

- **Modern UI/UX**: Built with Tailwind CSS and shadcn/ui components
- **TypeScript**: Full type safety throughout the application
- **Authentication**: Secure JWT-based authentication with NextAuth.js
- **State Management**: Zustand for global state management
- **Responsive Design**: Mobile-first approach with modern design system
- **API Integration**: Seamless integration with Flask backend

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: shadcn/ui + Radix UI
- **State Management**: Zustand
- **Authentication**: NextAuth.js
- **Charts**: Recharts
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── auth/            # Authentication pages
│   ├── dashboard/        # Dashboard pages
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Root layout
│   └── page.tsx         # Home page
├── components/          # Reusable components
│   └── ui/              # Base UI components
├── lib/                 # Utilities and configurations
│   ├── api-client.ts   # API client
│   ├── auth.ts         # Auth configuration
│   └── utils.ts        # Helper functions
├── store/              # Zustand stores
│   ├── auth-store.ts   # Authentication state
│   └── financial-store.ts # Financial data state
├── types/              # TypeScript type definitions
└── middleware.ts       # Next.js middleware
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Flask backend running on port 5000

### Installation

1. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env.local
   ```
   
   Update the environment variables in `.env.local`:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:5000
   NEXTAUTH_SECRET=your-secret-key
   NEXTAUTH_URL=http://localhost:3000
   ```

3. **Start the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

### Code Structure

#### Components
- **UI Components**: Reusable components in `src/components/ui/`
- **Page Components**: Page-specific components in `src/app/`
- **Layout Components**: Shared layouts and navigation

#### State Management
- **Auth Store**: User authentication and session management
- **Financial Store**: Financial data, goals, and calculations

#### API Integration
- **API Client**: Centralized HTTP client with interceptors
- **Type Safety**: Full TypeScript integration with backend API

### Styling

The application uses a comprehensive design system:

- **CSS Variables**: Consistent color palette and spacing
- **Tailwind CSS**: Utility-first CSS framework
- **Component Variants**: Reusable component styles
- **Dark Mode**: Built-in dark mode support
- **Responsive Design**: Mobile-first approach

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (`#3b82f6` to `#2563eb`)
- **Secondary**: Green gradient (`#22c55e` to `#16a34a`)
- **Neutral**: Gray scale for text and backgrounds
- **Status**: Success, warning, error colors

### Typography
- **Primary Font**: Inter (Google Fonts)
- **Monospace**: JetBrains Mono
- **Font Weights**: 300, 400, 500, 600, 700, 800

### Components
- **Cards**: Modern glassmorphism design
- **Buttons**: Gradient and outline variants
- **Forms**: Consistent input styling
- **Metrics**: Financial data display cards

## 🔐 Authentication

The application uses NextAuth.js for authentication:

- **JWT Tokens**: Secure token-based authentication
- **Session Management**: Automatic token refresh
- **Protected Routes**: Middleware-based route protection
- **User State**: Global user state management

### Auth Flow
1. User logs in with email/password
2. Backend validates credentials
3. JWT token returned and stored
4. Token used for API requests
5. Automatic logout on token expiry

## 📊 State Management

### Auth Store
```typescript
interface AuthState {
  user: User | null
  subscription: Subscription | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}
```

### Financial Store
```typescript
interface FinancialState {
  profile: FinancialProfile | null
  goals: SavingsGoal[]
  calculations: SafeSpendingCalculation | null
  isLoading: boolean
  error: string | null
}
```

## 🚀 Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Set environment variables
3. Deploy automatically on push to main branch

### Other Platforms
- **Netlify**: Static site deployment
- **Railway**: Full-stack deployment
- **Docker**: Containerized deployment

### Environment Variables
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=https://your-domain.com
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation

---

Built with ❤️ by the BusinessThis team
