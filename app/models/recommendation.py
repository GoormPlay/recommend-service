from pydantic import BaseModel
from typing import List, Optional

class RecommendationResponse(BaseModel):
    user_id: str
    movies: List[str]
    total_count: int
    message: str = "추천 영화 목록을 성공적으로 가져왔습니다."

class RecommendationRequest(BaseModel):
    user_id: str

class SetRecommendationRequest(BaseModel):
    user_id: str
    movies: List[str]
    expire_seconds: int = 3600

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int
