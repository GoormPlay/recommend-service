from typing import Optional, List
from app.services.redis_service import RedisService
from app.models.recommendation import RecommendationResponse
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.redis_service = RedisService()
    
    async def get_recommendations_for_user(self, user_id: str) -> Optional[RecommendationResponse]:
        """
        사용자별 영화 추천 목록을 가져옵니다.
        
        Args:
            user_id: 사용자 ID (JWT에서 추출)
            
        Returns:
            추천 응답 객체 또는 None
        """
        try:
            # Redis에서 추천 데이터 조회
            movies = await self.redis_service.get_user_recommendations(user_id)
            
            if movies is None:
                # 추천 데이터가 없는 경우 기본 추천 또는 빈 리스트
                logger.info(f"사용자 {user_id}의 추천 데이터가 없어 기본 추천을 제공합니다.")
                movies = await self._get_default_recommendations()
            
            return RecommendationResponse(
                user_id=user_id,
                movies=movies,
                total_count=len(movies),
                message="추천 영화 목록을 성공적으로 가져왔습니다."
            )
            
        except Exception as e:
            logger.error(f"추천 서비스 오류 (user_id: {user_id}): {e}")
            return None
    
    async def _get_default_recommendations(self) -> List[str]:
        """
        기본 추천 영화 목록 (추천 데이터가 없는 경우)
        실제로는 인기 영화나 신작 등을 반환
        """
        return ["dQw4w9WgXcQ", "jNQXAC9IVRw", "9bZkp7q19f0"]