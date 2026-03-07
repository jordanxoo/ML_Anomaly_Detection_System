from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "NADS – Network Anomaly Detection System"
    DEBUG: bool = True

    SECRET_KEY: str = "changeme_in_production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8  

 
    DATABASE_URL: str = "postgresql+asyncpg://nads:nadspassword@localhost:5432/nads_db"

 
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CHANNEL: str = "network_flows"

 
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "9_tGiR4ITDXv4Z7Dg5d71gXiazYtNToo-52_FDdRmqixaZoT_sGW7esKbDoF4_31ljnVUkOSeauOekLlItP-VQ=="
    INFLUXDB_ORG: str = "nads"
    INFLUXDB_BUCKET: str = "network_traffic"

  
    BINARY_MODEL_PATH: str = "models/model_binary.pkl"
    MULTICLASS_MODEL_PATH: str = "models/model_multiclass.pkl"
    LABEL_ENCODER_PATH: str = "models/label_encoder.pkl"

    FEATURE_COLUMNS_PATH: str = "models/feature_columns.pkl"

    ANOMALY_THRESHOLD: float = 0.35


settings = Settings()
