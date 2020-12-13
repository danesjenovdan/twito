CREATE TABLE IF NOT EXISTS daily_stats (
    id INTEGER PRIMARY KEY,
    metric_date DATE NOT NULL,
    original_tweets INTEGER DEFAULT 0 NOT NULL,
    retweets INTEGER DEFAULT 0 NOT NULL,
    quoted_tweets INTEGER DEFAULT 0 NOT NULL,
    estimated_seconds INTEGER DEFAULT 0 NOT NULL
)
