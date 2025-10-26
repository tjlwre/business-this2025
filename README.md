# BusinessThis - Personal Financial Planning Platform

A comprehensive financial planning application that helps users calculate safe spending amounts, track savings goals, and improve their financial health.

> **🚀 Production Ready**: This project is now configured for production deployment with Next.js frontend and Supabase backend. See [README-NEXTJS.md](README-NEXTJS.md) for the modern Next.js implementation.

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
   
   Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   Install Node.js dependencies:
   ```bash
   npm install
   ```
   
   Or install specific components:
   ```bash
   # Backend only
   pip install -r requirements/backend.txt
   
   # Frontend only
   pip install -r requirements/frontend.txt
   
   # With integrations
   pip install -r requirements/integrations.txt
   ```

3. **Set up environment variables**
   ```bash
   cp config/env.example .env
   ```
   
   Edit `.env` with your credentials:
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_ANON_KEY=your_supabase_anon_key
   SUPABASE_SERVICE_KEY=your_supabase_service_key
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
   OPENAI_API_KEY=sk-your_openai_api_key
   SECRET_KEY=your_secret_key_for_sessions
   ```

4. **Set up the database**
   - Create a new Supabase project
   - Run the SQL schema from `database/schema.sql` in your Supabase SQL editor

5. **Run the application**

   **Terminal 1 - Backend:**
   ```bash
   python run_backend.py
   ```

   **Terminal 2 - Frontend (Node.js):**
   ```bash
   node server.js
   ```

   **Terminal 3 - Streamlit (Optional):**
   ```bash
   streamlit run frontend/streamlit/app.py
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000
   - Streamlit App: http://localhost:8501 (if running)
   - Admin Dashboard: `python admin/dashboard.py`

## Utility Scripts

The project includes several utility scripts for setup and management:

### Database Setup
```bash
python scripts/setup_database.py
```

### Create Admin User
```bash
python scripts/create_admin.py
```

### Seed Test Data
```bash
python scripts/seed_data.py
```

### Admin Dashboard
```bash
python admin/dashboard.py
```

## Project Structure

```
BusinessThis/
├── frontend/               # Frontend applications
│   ├── static/             # Static HTML pages
│   │   ├── index.html      # Landing page
│   │   ├── app.html        # Main app
│   │   ├── pricing.html    # Pricing page
│   │   └── ...             # Other pages
│   └── streamlit/          # Streamlit app (optional)
│       ├── app.py          # Main Streamlit application
│       ├── components/     # Reusable components
│       └── pages/          # Page components
├── backend/                # Flask backend
│   ├── app.py              # Main Flask application
│   └── routes/             # API route modules
│       ├── auth.py         # Authentication routes
│       ├── profile.py      # Financial profile routes
│       ├── goals.py        # Savings goals routes
│       ├── calculator.py   # Calculator routes
│       ├── subscription.py # Subscription routes
│       ├── investment.py   # Investment routes
│       ├── ai.py           # AI routes
│       ├── reports.py      # Reports routes
│       ├── admin.py        # Admin routes
│       ├── email.py        # Email routes
│       ├── affiliate.py    # Affiliate routes
│       ├── courses.py      # Course routes
│       ├── accounts.py     # Multi-user account routes
│       └── advisor.py      # Advisor routes
├── services/               # Business services
│   ├── auth_service.py     # Authentication service
│   ├── financial_service.py # Financial calculations
│   ├── subscription_service.py # Subscription management
│   ├── calculation_service.py # Financial calculations
│   └── ...                 # Other services
├── models/                 # Data models
│   ├── user.py             # User model
│   ├── financial_profile.py # Financial profile model
│   ├── savings_goal.py     # Savings goal model
│   └── transaction.py     # Transaction model
├── core/                   # Core utilities
│   └── utils/              # Utility functions
│       ├── validators.py   # Input validation
│       ├── decorators.py   # Route decorators
│       ├── security.py     # Security utilities
│       └── error_handler.py # Error handling
├── config/                 # Configuration
│   ├── settings.py         # Centralized settings
│   ├── supabase_config.py  # Database configuration
│   └── env.example         # Environment template
├── database/               # Database schema
│   └── schema.sql          # Database schema
├── integrations/          # External service integrations
│   ├── stripe_integration.py
│   ├── paypal_integration.py
│   ├── openai_integration.py
│   ├── plaid_integration.py
│   └── sendgrid_integration.py
├── admin/                  # Admin dashboard
│   └── dashboard.py        # Admin interface
├── scripts/                # Utility scripts
│   ├── setup_database.py   # Database setup
│   ├── create_admin.py     # Admin user creation
│   └── seed_data.py        # Test data seeding
├── requirements/           # Modular dependencies
│   ├── base.txt            # Core dependencies
│   ├── backend.txt         # Backend dependencies
│   ├── frontend.txt        # Frontend dependencies
│   ├── integrations.txt    # Integration dependencies
│   ├── dev.txt             # Development dependencies
│   └── prod.txt            # Production dependencies
├── nextjs-app/             # Next.js app (archived)
├── server.js               # Node.js frontend server
├── package.json            # Node.js dependencies
├── requirements.txt        # Main Python dependencies
├── vercel.json             # Vercel deployment config
├── run_backend.py          # Backend startup script
└── README.md               # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user

### Financial Profile
- `GET /api/financial-profile` - Get financial profile
- `POST /api/financial-profile` - Create/update financial profile

### Savings Goals
- `GET /api/savings-goals` - Get savings goals
- `POST /api/savings-goals` - Create savings goal
- `PUT /api/savings-goals/{id}` - Update savings goal
- `DELETE /api/savings-goals/{id}` - Delete savings goal

### Calculator
- `POST /api/calculator/safe-spend` - Calculate safe spending
- `GET /api/calculator/financial-health` - Get financial health score

### Subscriptions
- `GET /api/subscription/status` - Get subscription status
- `POST /api/subscription/upgrade` - Upgrade subscription

## Subscription Tiers

### Free Tier
- Basic calculator
- 1 savings goal
- Financial health score
- Basic reports

### Premium ($9.99/month)
- Everything in Free
- 5 savings goals
- Advanced analytics
- PDF exports
- Email notifications
- 50 AI interactions/month

### Pro ($19.99/month)
- Everything in Premium
- Unlimited savings goals
- AI financial coaching
- Investment tracking
- API access
- White-label options
- Unlimited AI interactions

## Development

### Running in Development Mode
```bash
# Backend with auto-reload
python run_backend.py

# Frontend with auto-reload
streamlit run frontend/app.py --server.port 8501
```

### Testing
```bash
# Test the calculator
python -c "from calculations import get_all_safe_spends; print(get_all_safe_spends(5000, 2000, 1000, 10000, 12))"
```

## Deployment

### Backend Deployment
1. Deploy to Railway, Render, or Heroku
2. Set environment variables
3. Configure domain and SSL

### Frontend Deployment
1. Deploy to Streamlit Cloud, Vercel, or Netlify
2. Update API_BASE_URL in frontend/app.py
3. Configure CORS in backend

### Database
- Supabase handles database hosting
- Automatic backups and scaling
- Row Level Security (RLS) enabled

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@businessthis.com or create an issue in the repository.

## Roadmap

### Phase 1 (Current)
- ✅ User authentication
- ✅ Financial profile management
- ✅ Safe spending calculator
- ✅ Savings goals tracking
- ✅ Basic subscription system

### Phase 2 (Next)
- 🔄 AI financial coaching
- 🔄 Advanced analytics
- 🔄 PDF/Excel export
- 🔄 Email notifications

### Phase 3 (Future)
- 📋 Investment tracking
- 📋 Bank account integration
- 📋 Mobile app
- 📋 Enterprise features
