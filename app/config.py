from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Redis 설정
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""
    
    # JWT 설정 (GoormPlay의 Auth Service와 동일한 시크릿)
    jwt_secret_key: str = "pA1Qb6q8vXqWn4FQ8zQ2h6V7Q6k3y8fB3wZ2s9T1n4m5c6p7v8w9x0y1z2A3B4C5D6E7F8G9H0I1J2K3L4M5N6O7P8Q9R0S1T2U3V4W5X6Y7Z8"
    jwt_algorithm: str = "HS256"
    
    # 서비스 설정
    service_name: str = "movie-recommendation-service"
    service_port: int = 8001
    
    # API Gateway 설정
    api_gateway_url: str = "http://localhost:8080"
    
    class Config:
        env_file = ".env"

settings = Settings()