from pydantic import BaseModel
from typing import List

class RecommendationResponse(BaseModel):
    """추천 영화 응답 모델"""
    user_id: str
    movies: List[str]
    total_count: int
    message: str

class SetRecommendationRequest(BaseModel):
    """추천 영화 저장 요청 모델"""
    user_id: str
    movies: List[str]
    expire_seconds: int = 3600  # 기본값: 1시간
