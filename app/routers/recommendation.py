from fastapi import APIRouter, Depends, HTTPException
from app.models.recommendation import RecommendationResponse, ErrorResponse
from app.services.recommendation_service import RecommendationService
from app.middleware.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

# 의존성 주입을 위한 서비스 인스턴스
recommendation_service = RecommendationService()

@router.get(
    "/movies",
    response_model=RecommendationResponse,
    summary="사용자별 영화 추천 목록 조회",
    description="인증된 사용자의 개인화된 영화 추천 목록을 반환합니다."
)
async def get_user_movie_recommendations(
    current_user: dict = Depends(get_current_user)
) -> RecommendationResponse:
    """
    **사용자별 영화 추천 API**
    
    - **인증 필요**: Bearer JWT 토큰
    - **기능**: Redis에서 사용자별 추천 영화 목록 조회
    - **응답**: 추천 영화 ID 리스트와 메타데이터
    
    **사용 예시:**
    ```
    GET /api/recommendations/movies
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
    ```
    """
    try:
        user_id = current_user["user_id"]
        username = current_user["username"]
        
        logger.info(f"영화 추천 요청 - 사용자: {username} (ID: {user_id})")
        
        # 추천 서비스에서 데이터 조회
        recommendations = await recommendation_service.get_recommendations_for_user(user_id)
        
        if recommendations is None:
            raise HTTPException(
                status_code=500,
                detail="추천 데이터를 가져오는 중 오류가 발생했습니다."
            )
        
        logger.info(f"추천 응답 성공 - 사용자: {username}, 영화 수: {recommendations.total_count}")
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"추천 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.get(
    "/health",
    summary="서비스 상태 확인",
    description="추천 서비스와 Redis 연결 상태를 확인합니다."
)
async def health_check():
    """서비스 헬스 체크"""
    try:
        # Redis 연결 테스트
        redis_service = RecommendationService().redis_service
        redis_service.redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "movie-recommendation-service",
            "redis": "connected"
        }
    except Exception as e:
        logger.error(f"헬스 체크 실패: {e}")
        raise HTTPException(
            status_code=503,
            detail="서비스가 현재 사용할 수 없습니다."
        )