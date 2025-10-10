-- BusinessThis Database Schema
-- Supabase PostgreSQL Database

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (extends Supabase auth.users)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    subscription_tier VARCHAR(20) DEFAULT 'free' CHECK (subscription_tier IN ('free', 'premium', 'pro')),
    subscription_status VARCHAR(20) DEFAULT 'active' CHECK (subscription_status IN ('active', 'cancelled', 'past_due')),
    subscription_expires_at TIMESTAMP WITH TIME ZONE,
    ai_usage_count INTEGER DEFAULT 0,
    ai_usage_limit INTEGER DEFAULT 0,
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE
);

-- Financial profiles table
CREATE TABLE public.financial_profiles (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    monthly_income DECIMAL(12,2) DEFAULT 0,
    fixed_expenses DECIMAL(12,2) DEFAULT 0,
    variable_expenses DECIMAL(12,2) DEFAULT 0,
    emergency_fund_target DECIMAL(12,2) DEFAULT 0,
    emergency_fund_current DECIMAL(12,2) DEFAULT 0,
    total_debt DECIMAL(12,2) DEFAULT 0,
    credit_score INTEGER,
    risk_tolerance VARCHAR(20) DEFAULT 'moderate' CHECK (risk_tolerance IN ('conservative', 'moderate', 'aggressive')),
    age INTEGER,
    retirement_age INTEGER DEFAULT 65,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Savings goals table
CREATE TABLE public.savings_goals (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    current_amount DECIMAL(12,2) DEFAULT 0,
    target_date DATE,
    monthly_contribution DECIMAL(12,2),
    priority INTEGER DEFAULT 1,
    is_achieved BOOLEAN DEFAULT FALSE,
    achieved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transactions table
CREATE TABLE public.transactions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    amount DECIMAL(12,2) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('income', 'expense', 'transfer')),
    date DATE NOT NULL,
    account_name VARCHAR(255),
    is_recurring BOOLEAN DEFAULT FALSE,
    recurring_frequency VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscriptions table
CREATE TABLE public.subscriptions (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    stripe_subscription_id VARCHAR(255),
    paypal_subscription_id VARCHAR(255),
    plan_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    current_period_start TIMESTAMP WITH TIME ZONE,
    current_period_end TIMESTAMP WITH TIME ZONE,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI usage tracking
CREATE TABLE public.ai_usage (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    request_type VARCHAR(50) NOT NULL,
    tokens_used INTEGER,
    cost DECIMAL(8,4),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Investment portfolios
CREATE TABLE public.investment_portfolios (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    total_value DECIMAL(12,2) DEFAULT 0,
    cash_balance DECIMAL(12,2) DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Investment holdings
CREATE TABLE public.investment_holdings (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    portfolio_id UUID REFERENCES public.investment_portfolios(id) ON DELETE CASCADE,
    symbol VARCHAR(20) NOT NULL,
    asset_type VARCHAR(20) CHECK (asset_type IN ('stock', 'bond', 'crypto', 'etf', 'mutual_fund')),
    quantity DECIMAL(12,6) NOT NULL,
    purchase_price DECIMAL(12,4),
    current_price DECIMAL(12,4),
    purchase_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Financial health scores
CREATE TABLE public.financial_health_scores (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    overall_score INTEGER NOT NULL CHECK (overall_score >= 0 AND overall_score <= 100),
    savings_rate_score INTEGER,
    debt_ratio_score INTEGER,
    emergency_fund_score INTEGER,
    investment_score INTEGER,
    calculated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Email campaigns
CREATE TABLE public.email_campaigns (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    template_type VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Email subscribers
CREATE TABLE public.email_subscribers (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    is_subscribed BOOLEAN DEFAULT TRUE,
    subscription_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    unsubscribed_at TIMESTAMP WITH TIME ZONE
);

-- Support tickets
CREATE TABLE public.support_tickets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    subject VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')),
    priority VARCHAR(10) DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_financial_profiles_user_id ON public.financial_profiles(user_id);
CREATE INDEX idx_savings_goals_user_id ON public.savings_goals(user_id);
CREATE INDEX idx_transactions_user_id ON public.transactions(user_id);
CREATE INDEX idx_transactions_date ON public.transactions(date);
CREATE INDEX idx_subscriptions_user_id ON public.subscriptions(user_id);
CREATE INDEX idx_ai_usage_user_id ON public.ai_usage(user_id);
CREATE INDEX idx_investment_portfolios_user_id ON public.investment_portfolios(user_id);
CREATE INDEX idx_financial_health_scores_user_id ON public.financial_health_scores(user_id);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Add updated_at triggers to all tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_financial_profiles_updated_at BEFORE UPDATE ON public.financial_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_savings_goals_updated_at BEFORE UPDATE ON public.savings_goals FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON public.transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON public.subscriptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_investment_portfolios_updated_at BEFORE UPDATE ON public.investment_portfolios FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_investment_holdings_updated_at BEFORE UPDATE ON public.investment_holdings FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_support_tickets_updated_at BEFORE UPDATE ON public.support_tickets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.financial_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.savings_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.transactions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_usage ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.investment_portfolios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.investment_holdings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.financial_health_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.email_subscribers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.support_tickets ENABLE ROW LEVEL SECURITY;

-- RLS Policies - Users can only access their own data
CREATE POLICY "Users can view own data" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own data" ON public.users FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own financial profiles" ON public.financial_profiles FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own savings goals" ON public.savings_goals FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own transactions" ON public.transactions FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own subscriptions" ON public.subscriptions FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own AI usage" ON public.ai_usage FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own investment portfolios" ON public.investment_portfolios FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own investment holdings" ON public.investment_holdings FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own financial health scores" ON public.financial_health_scores FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own email subscriptions" ON public.email_subscribers FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can view own support tickets" ON public.support_tickets FOR ALL USING (auth.uid() = user_id);
