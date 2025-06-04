from typing import List
from app.services.redis_service import RedisService
from app.models.recommendation import RecommendationResponse
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.redis_service = RedisService()

    def get_recommendations_for_user(self, user_id: str) -> RecommendationResponse:
        """
        사용자별 추천 영화 목록을 조회합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            추천 영화 응답 객체
        """
        # Redis에서 사용자 추천 데이터 조회
        movies = self.redis_service.get_user_recommendations(user_id)
        
        # 데이터가 없으면 기본 추천 제공
        if movies is None:
            logger.info(f"사용자 {user_id}의 추천 데이터가 없어 기본 추천을 제공합니다.")
            movies = self._get_default_recommendations()
        
        return RecommendationResponse(
            user_id=user_id,
            movies=movies,
            total_count=len(movies),
            message="추천 영화 목록을 성공적으로 가져왔습니다."
        )

    def set_recommendations_for_user(self, user_id: str, movies: List[str], expire_seconds: int = 3600) -> bool:
        """
        사용자별 추천 영화 목록을 저장합니다.
        
        Args:
            user_id: 사용자 ID
            movies: 추천 영화 ID 리스트
            expire_seconds: 만료 시간 (초, 기본값: 1시간)
            
        Returns:
            저장 성공 여부
        """
        return self.redis_service.set_user_recommendations(user_id, movies, expire_seconds)

    def _get_default_recommendations(self) -> List[str]:
        """
        기본 추천 영화 목록을 반환합니다.
        
        Returns:
            기본 영화 ID 리스트
        """
        return [
            "6837be17aec8b2058fac893a",
            "6837be17aec8b2058fac893b", 
            "6837be17aec8b2058fac893c",
            "6837be17aec8b2058fac893d",
            "6837be17aec8b2058fac893e"
        ]

    def delete_recommendations_for_user(self, user_id: str) -> bool:
        """
        사용자별 추천 영화 목록을 삭제합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        return self.redis_service.delete_user_recommendations(user_id)
