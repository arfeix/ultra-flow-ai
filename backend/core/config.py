"""
Configuration module for Ultra Flow AI backend.

This module handles all environment-based configuration for:
- Exchange settings (API keys, endpoints)
- Risk management parameters
- Database connections
- Redis cache settings
- Security and authentication
"""

import os
from typing import Optional
from pydantic import BaseSettings, validator, Field


class ExchangeConfig(BaseSettings):
    """Exchange API configuration."""
    
    # Primary exchange settings
    exchange_name: str = Field(default="binance", env="EXCHANGE_NAME")
    api_key: str = Field(default="", env="EXCHANGE_API_KEY")
    api_secret: str = Field(default="", env="EXCHANGE_API_SECRET")
    api_passphrase: Optional[str] = Field(default=None, env="EXCHANGE_API_PASSPHRASE")
    
    # Exchange endpoints
    rest_endpoint: str = Field(
        default="https://api.binance.com",
        env="EXCHANGE_REST_ENDPOINT"
    )
    ws_endpoint: str = Field(
        default="wss://stream.binance.com:9443/ws",
        env="EXCHANGE_WS_ENDPOINT"
    )
    testnet_enabled: bool = Field(default=False, env="EXCHANGE_TESTNET_ENABLED")
    testnet_endpoint: Optional[str] = Field(
        default=None,
        env="EXCHANGE_TESTNET_ENDPOINT"
    )
    
    # Exchange parameters
    request_timeout: int = Field(default=30, env="EXCHANGE_REQUEST_TIMEOUT")
    max_retries: int = Field(default=3, env="EXCHANGE_MAX_RETRIES")
    retry_delay: float = Field(default=1.0, env="EXCHANGE_RETRY_DELAY")
    
    class Config:
        env_prefix = "EXCHANGE_"
        case_sensitive = False


class RiskManagementConfig(BaseSettings):
    """Risk management configuration."""
    
    # Position sizing
    max_position_size: float = Field(default=0.1, env="RISK_MAX_POSITION_SIZE")
    max_leverage: float = Field(default=5.0, env="RISK_MAX_LEVERAGE")
    min_leverage: float = Field(default=1.0, env="RISK_MIN_LEVERAGE")
    
    # Risk limits
    max_daily_loss_percent: float = Field(default=5.0, env="RISK_MAX_DAILY_LOSS_PERCENT")
    max_drawdown_percent: float = Field(default=10.0, env="RISK_MAX_DRAWDOWN_PERCENT")
    max_open_positions: int = Field(default=10, env="RISK_MAX_OPEN_POSITIONS")
    
    # Stop loss and take profit
    default_stop_loss_percent: float = Field(default=2.0, env="RISK_DEFAULT_STOP_LOSS_PERCENT")
    default_take_profit_percent: float = Field(default=5.0, env="RISK_DEFAULT_TAKE_PROFIT_PERCENT")
    trailing_stop_enabled: bool = Field(default=True, env="RISK_TRAILING_STOP_ENABLED")
    trailing_stop_percent: float = Field(default=1.0, env="RISK_TRAILING_STOP_PERCENT")
    
    # Risk metrics
    max_correlation: float = Field(default=0.8, env="RISK_MAX_CORRELATION")
    min_volatility_threshold: float = Field(default=0.01, env="RISK_MIN_VOLATILITY_THRESHOLD")
    max_volatility_threshold: float = Field(default=0.1, env="RISK_MAX_VOLATILITY_THRESHOLD")
    
    # Circuit breaker
    circuit_breaker_enabled: bool = Field(default=True, env="RISK_CIRCUIT_BREAKER_ENABLED")
    circuit_breaker_threshold: float = Field(default=0.15, env="RISK_CIRCUIT_BREAKER_THRESHOLD")
    
    @validator("max_leverage")
    def validate_leverage(cls, v, values):
        if v < values.get("min_leverage", 1.0):
            raise ValueError("max_leverage must be >= min_leverage")
        return v
    
    class Config:
        env_prefix = "RISK_"
        case_sensitive = False


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    
    # Connection settings
    driver: str = Field(default="postgresql", env="DATABASE_DRIVER")
    host: str = Field(default="localhost", env="DATABASE_HOST")
    port: int = Field(default=5432, env="DATABASE_PORT")
    username: str = Field(default="postgres", env="DATABASE_USERNAME")
    password: str = Field(default="", env="DATABASE_PASSWORD")
    database: str = Field(default="ultra_flow_ai", env="DATABASE_NAME")
    
    # Pool configuration
    pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    pool_timeout: int = Field(default=30, env="DATABASE_POOL_TIMEOUT")
    pool_recycle: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    # SSL configuration
    ssl_enabled: bool = Field(default=False, env="DATABASE_SSL_ENABLED")
    ssl_cert_path: Optional[str] = Field(default=None, env="DATABASE_SSL_CERT_PATH")
    
    # Query settings
    echo: bool = Field(default=False, env="DATABASE_ECHO")
    echo_pool: bool = Field(default=False, env="DATABASE_ECHO_POOL")
    
    @property
    def url(self) -> str:
        """Generate database connection URL."""
        if self.password:
            return (
                f"{self.driver}://{self.username}:{self.password}@"
                f"{self.host}:{self.port}/{self.database}"
            )
        return f"{self.driver}://{self.username}@{self.host}:{self.port}/{self.database}"
    
    class Config:
        env_prefix = "DATABASE_"
        case_sensitive = False


class RedisConfig(BaseSettings):
    """Redis cache configuration."""
    
    # Connection settings
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")
    password: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    db: int = Field(default=0, env="REDIS_DB")
    
    # Pool configuration
    pool_size: int = Field(default=10, env="REDIS_POOL_SIZE")
    pool_timeout: int = Field(default=30, env="REDIS_POOL_TIMEOUT")
    socket_timeout: int = Field(default=5, env="REDIS_SOCKET_TIMEOUT")
    socket_connect_timeout: int = Field(default=5, env="REDIS_SOCKET_CONNECT_TIMEOUT")
    
    # SSL configuration
    ssl_enabled: bool = Field(default=False, env="REDIS_SSL_ENABLED")
    ssl_cert_reqs: Optional[str] = Field(default=None, env="REDIS_SSL_CERT_REQS")
    ssl_ca_certs: Optional[str] = Field(default=None, env="REDIS_SSL_CA_CERTS")
    
    # TTL settings
    default_ttl: int = Field(default=3600, env="REDIS_DEFAULT_TTL")  # 1 hour
    cache_ttl: int = Field(default=1800, env="REDIS_CACHE_TTL")  # 30 minutes
    session_ttl: int = Field(default=86400, env="REDIS_SESSION_TTL")  # 24 hours
    
    # Feature flags
    enable_cache: bool = Field(default=True, env="REDIS_ENABLE_CACHE")
    enable_session: bool = Field(default=True, env="REDIS_ENABLE_SESSION")
    
    @property
    def url(self) -> str:
        """Generate Redis connection URL."""
        if self.ssl_enabled:
            scheme = "rediss"
        else:
            scheme = "redis"
        
        if self.password:
            return f"{scheme}://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"{scheme}://{self.host}:{self.port}/{self.db}"
    
    class Config:
        env_prefix = "REDIS_"
        case_sensitive = False


class SecurityConfig(BaseSettings):
    """Security and authentication configuration."""
    
    # JWT settings
    jwt_secret_key: str = Field(default="change-me-in-production", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_hours: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    jwt_refresh_expiration_days: int = Field(default=7, env="JWT_REFRESH_EXPIRATION_DAYS")
    
    # Password settings
    password_min_length: int = Field(default=12, env="PASSWORD_MIN_LENGTH")
    password_require_uppercase: bool = Field(default=True, env="PASSWORD_REQUIRE_UPPERCASE")
    password_require_lowercase: bool = Field(default=True, env="PASSWORD_REQUIRE_LOWERCASE")
    password_require_digits: bool = Field(default=True, env="PASSWORD_REQUIRE_DIGITS")
    password_require_special: bool = Field(default=True, env="PASSWORD_REQUIRE_SPECIAL")
    
    # Encryption settings
    encryption_key: str = Field(default="", env="ENCRYPTION_KEY")
    enable_encryption: bool = Field(default=True, env="ENABLE_ENCRYPTION")
    
    # 2FA settings
    two_factor_auth_enabled: bool = Field(default=True, env="TWO_FACTOR_AUTH_ENABLED")
    totp_issuer: str = Field(default="Ultra Flow AI", env="TOTP_ISSUER")
    
    # API security
    api_rate_limit_enabled: bool = Field(default=True, env="API_RATE_LIMIT_ENABLED")
    api_rate_limit_requests: int = Field(default=100, env="API_RATE_LIMIT_REQUESTS")
    api_rate_limit_window_seconds: int = Field(default=60, env="API_RATE_LIMIT_WINDOW_SECONDS")
    
    # CORS settings
    cors_origins: list = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: list = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        env="CORS_ALLOW_METHODS"
    )
    cors_allow_headers: list = Field(
        default=["Content-Type", "Authorization"],
        env="CORS_ALLOW_HEADERS"
    )
    
    # Audit logging
    audit_logging_enabled: bool = Field(default=True, env="AUDIT_LOGGING_ENABLED")
    audit_log_retention_days: int = Field(default=90, env="AUDIT_LOG_RETENTION_DAYS")
    
    # API key management
    api_key_rotation_enabled: bool = Field(default=True, env="API_KEY_ROTATION_ENABLED")
    api_key_rotation_days: int = Field(default=90, env="API_KEY_ROTATION_DAYS")
    
    class Config:
        env_prefix = "SECURITY_"
        case_sensitive = False


class AppConfig(BaseSettings):
    """Application-wide configuration."""
    
    # App settings
    app_name: str = Field(default="Ultra Flow AI", env="APP_NAME")
    app_version: str = Field(default="1.0.0", env="APP_VERSION")
    environment: str = Field(default="development", env="ENVIRONMENT")
    debug: bool = Field(default=False, env="DEBUG")
    
    # API settings
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Trading settings
    trading_enabled: bool = Field(default=False, env="TRADING_ENABLED")
    paper_trading_enabled: bool = Field(default=True, env="PAPER_TRADING_ENABLED")
    
    # Feature flags
    enable_backtesting: bool = Field(default=True, env="ENABLE_BACKTESTING")
    enable_live_trading: bool = Field(default=False, env="ENABLE_LIVE_TRADING")
    enable_paper_trading: bool = Field(default=True, env="ENABLE_PAPER_TRADING")
    
    # Notifications
    notifications_enabled: bool = Field(default=True, env="NOTIFICATIONS_ENABLED")
    notification_channels: list = Field(
        default=["email", "in_app"],
        env="NOTIFICATION_CHANNELS"
    )
    
    @validator("environment")
    def validate_environment(cls, v):
        valid_environments = ["development", "staging", "production"]
        if v not in valid_environments:
            raise ValueError(f"environment must be one of {valid_environments}")
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"
    
    class Config:
        env_prefix = "APP_"
        case_sensitive = False


class Config(BaseSettings):
    """Main configuration class that aggregates all sub-configurations."""
    
    # Sub-configurations
    app: AppConfig = AppConfig()
    exchange: ExchangeConfig = ExchangeConfig()
    risk: RiskManagementConfig = RiskManagementConfig()
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    security: SecurityConfig = SecurityConfig()
    
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global config instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config() -> Config:
    """Reload configuration from environment variables and .env file."""
    global config
    config = Config()
    return config
