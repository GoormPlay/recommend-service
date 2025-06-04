from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Redis 설정
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # 서비스 설정
    service_name: str = "movie-recommendation-service"
    service_port: int = 8001
    
    class Config:
        env_file = ".env"

settings = Settings()
