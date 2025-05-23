"""
Configuration management for the betting intelligence platform
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    database_url: str = "sqlite:///./bet_intel.db"
    
    # API Keys
    odds_api_key: Optional[str] = None
    pinnacle_api_key: Optional[str] = None
    prophetx_api_key: Optional[str] = None
    sporttrade_api_key: Optional[str] = None
    
    # The Odds API Configuration
    odds_api_base_url: str = "https://api.the-odds-api.com/v4"
    odds_polling_interval_minutes: int = 3
    default_sport: str = "basketball_nba"  # Start with NBA
    default_regions: str = "us"
    default_markets: str = "h2h,spreads,totals"
    odds_format: str = "american"
    
    # Sportsbook URLs
    draftkings_base_url: str = "https://sportsbook.draftkings.com"
    fanduel_base_url: str = "https://sportsbook.fanduel.com"
    caesars_base_url: str = "https://www.caesars.com/sportsbook"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # Security
    secret_key: str = "your_secret_key_here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Rate Limiting
    api_rate_limit_per_minute: int = 60
    
    # Logging
    log_level: str = "INFO"
    
    # Affiliate Settings
    affiliate_tracking_enabled: bool = True
    draftkings_affiliate_id: Optional[str] = None
    fanduel_affiliate_id: Optional[str] = None
    caesars_affiliate_id: Optional[str] = None
    
    # AI/ML Settings
    enable_premium_features: bool = False
    monte_carlo_iterations: int = 10000
    bayesian_confidence_threshold: float = 0.8

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the application settings"""
    return settings 