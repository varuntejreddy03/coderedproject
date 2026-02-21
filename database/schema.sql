-- Supabase Database Schema for PumpWatch

-- Table 1: Rumor Sources (Telegram, Reddit, YouTube)
CREATE TABLE rumor_sources (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    channel TEXT,
    subreddit TEXT,
    title TEXT,
    text TEXT,
    tickers TEXT[],
    fraud_score INTEGER DEFAULT 0,
    hype_score INTEGER DEFAULT 0,
    upvotes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    url TEXT,
    timestamp TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_rumor_tickers ON rumor_sources USING GIN (tickers);
CREATE INDEX idx_rumor_source ON rumor_sources (source);

-- Table 2: Risk Analysis Results
CREATE TABLE risk_analysis (
    id BIGSERIAL PRIMARY KEY,
    ticker TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level TEXT,
    color TEXT,
    price DECIMAL(10, 2),
    volume BIGINT,
    z_score DECIMAL(10, 2),
    telegram_mentions INTEGER DEFAULT 0,
    reddit_mentions INTEGER DEFAULT 0,
    youtube_mentions INTEGER DEFAULT 0,
    social_hype_score INTEGER DEFAULT 0,
    volume_anomaly INTEGER DEFAULT 0,
    bot_coordination INTEGER DEFAULT 0,
    sentiment_spike INTEGER DEFAULT 0,
    lack_of_filings INTEGER DEFAULT 0,
    legitimacy_verdict TEXT,
    legitimacy_score INTEGER DEFAULT 0,
    ai_analysis TEXT,
    analyzed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_risk_ticker ON risk_analysis (ticker);
CREATE INDEX idx_risk_score ON risk_analysis (risk_score DESC);
