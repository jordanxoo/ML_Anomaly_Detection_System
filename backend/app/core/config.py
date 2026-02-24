from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # App
    APP_NAME: str = "NADS – Network Anomaly Detection System"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "changeme_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  # 8 hours

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://nads:nadspassword@localhost:5432/nads_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CHANNEL: str = "network_flows"

    # InfluxDB
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "mydevtoken"
    INFLUXDB_ORG: str = "nads"
    INFLUXDB_BUCKET: str = "network_traffic"

    # ML Model
    MODEL_PATH: str = "ml/models/anomaly_model.pkl"
    ANOMALY_THRESHOLD: float = 0.5  # decision threshold for Isolation Forest score


settings = Settings()
