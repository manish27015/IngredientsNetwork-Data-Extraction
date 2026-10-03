-- Supabase / PostgreSQL Table Schema for Scraped Suppliers Data
-- Relu Consultancy Hiring Challenge - Bonus Challenge

CREATE TABLE IF NOT EXISTS suppliers (
    id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL,
    company_description TEXT,
    sales_markets TEXT,
    primary_business_activity TEXT,
    categories TEXT,
    events TEXT,
    address TEXT,
    email TEXT,
    telephone TEXT,
    website TEXT,
    profile_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for search and filtering performance
CREATE INDEX IF NOT EXISTS idx_suppliers_company_name ON suppliers(company_name);
CREATE INDEX IF NOT EXISTS idx_suppliers_business_activity ON suppliers(primary_business_activity);
