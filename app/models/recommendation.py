from pydantic import BaseModel
from typing import List, Optional

class MovieRecommendation(BaseModel):
    user_id: str
    recommend_movies: List[str]
    
class RecommendationResponse(BaseModel):
    user_id: str
    movies: List[str]
    total_count: int
    message: str = "추천 영화 목록을 성공적으로 가져왔습니다."

class ErrorResponse(BaseModel):
    error: str
    message: str
    status_code: int