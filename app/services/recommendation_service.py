from typing import Optional, List
from app.services.redis_service import RedisService
from app.models.recommendation import RecommendationResponse
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.redis_service = RedisService()
    
    def get_recommendations_for_user(self, user_id: str) -> Optional[RecommendationResponse]:
        """
        사용자별 영화 추천 목록을 가져옵니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            추천 응답 객체 또는 None
        """
        try:
            movies = self.redis_service.get_user_recommendations(user_id)
            
            if movies is None:
                logger.info(f"사용자 {user_id}의 추천 데이터가 없어 기본 추천을 제공합니다.")
                movies = self._get_default_recommendations()
            
            return RecommendationResponse(
                user_id=user_id,
                movies=movies,
                total_count=len(movies),
                message="추천 영화 목록을 성공적으로 가져왔습니다."
            )
            
        except Exception as e:
            logger.error(f"추천 서비스 오류 (user_id: {user_id}): {e}")
            return None
    
    def set_recommendations_for_user(self, user_id: str, movies: List[str], expire_seconds: int = 3600) -> bool:
        """
        사용자별 영화 추천 목록을 저장합니다.
        
        Args:
            user_id: 사용자 ID
            movies: 추천 영화 ID 리스트
            expire_seconds: 만료 시간 (초)
            
        Returns:
            저장 성공 여부
        """
        try:
            return self.redis_service.set_user_recommendations(user_id, movies, expire_seconds)
        except Exception as e:
            logger.error(f"추천 데이터 저장 오류 (user_id: {user_id}): {e}")
            return False
    
    def delete_recommendations_for_user(self, user_id: str) -> bool:
        """
        사용자의 추천 데이터를 삭제합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        try:
            return self.redis_service.delete_user_recommendations(user_id)
        except Exception as e:
            logger.error(f"추천 데이터 삭제 오류 (user_id: {user_id}): {e}")
            return False
    
    def get_all_users_with_recommendations(self) -> List[str]:
        """
        추천 데이터가 있는 모든 사용자를 조회합니다.
        
        Returns:
            사용자 ID 리스트
        """
        try:
            return self.redis_service.get_all_users_with_recommendations()
        except Exception as e:
            logger.error(f"사용자 목록 조회 오류: {e}")
            return []
    
    def _get_default_recommendations(self) -> List[str]:
        """
        기본 추천 영화 목록 (추천 데이터가 없는 경우)
        GoormPlay Content Service 호환 - 기본 10개 추천
        """
        return [
            "6837be17aec8b2058fac893a",  # 인셉션
            "6837be17aec8b2058fac893b",  # 기생충
            "6837be17aec8b2058fac893c",  # 올드보이
            "6837be17aec8b2058fac893d", 
            "6837be17aec8b2058fac893e", 
            "6837be17aec8b2058fac893f", 
            "6837be17aec8b2058fac8940", 
            "6837be17aec8b2058fac8942", 
            "6837be17aec8b2058fac8943", 
            "6837be17aec8b2058fac8944"
        ]
