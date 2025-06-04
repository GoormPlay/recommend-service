from fastapi import APIRouter, HTTPException, Query
from app.models.recommendation import (
    RecommendationResponse, 
    RecommendationRequest,
    SetRecommendationRequest,
    ErrorResponse
)
from app.services.recommendation_service import RecommendationService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/contents", tags=["contents"])

# 서비스 인스턴스
recommendation_service = RecommendationService()

@router.get(
    "/recommended/{user_id}",
    response_model=RecommendationResponse,
    summary="사용자별 영화 추천 목록 조회",
    description="특정 사용자의 개인화된 영화 추천 목록을 반환합니다."
)
async def get_user_movie_recommendations(user_id: str) -> RecommendationResponse:
    """
    **사용자별 영화 추천 API**
    
    - **기능**: Redis에서 사용자별 추천 영화 목록 조회
    - **응답**: 추천 영화 ID 리스트와 메타데이터
    
    **사용 예시:**
    ```
    GET /api/contents/recommended/user123
    ```
    """
    try:
        logger.info(f"영화 추천 요청 - 사용자 ID: {user_id}")
        
        recommendations = recommendation_service.get_recommendations_for_user(user_id)
        
        if recommendations is None:
            raise HTTPException(
                status_code=500,
                detail="추천 데이터를 가져오는 중 오류가 발생했습니다."
            )
        
        logger.info(f"추천 응답 성공 - 사용자: {user_id}, 영화 수: {recommendations.total_count}")
        return recommendations
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"추천 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.post(
    "/recommended/bulk-ids",
    summary="추천 영화 ID 목록 조회 (GoormPlay 호환)",
    description="GoormPlay Content Service와 호환되는 bulk ID 요청 엔드포인트"
)
async def get_recommendations_by_bulk_ids(request: RecommendationRequest):
    """
    **GoormPlay Content Service 호환 API**
    
    Content Service의 getRecommendedContentsForUser()와 호환
    사용자 ID로 추천 영화 ID 목록을 반환
    
    **사용 예시:**
    ```json
    {
        "user_id": "user123"
    }
    ```
    
    **응답:**
    ```json
    {
        "contentIds": ["6837be17aec8b2058fac893a", "6837be17aec8b2058fac893b"]
    }
    ```
    """
    try:
        logger.info(f"GoormPlay 호환 Bulk IDs 요청 - 사용자 ID: {request.user_id}")
        
        recommendations = recommendation_service.get_recommendations_for_user(request.user_id)
        
        if recommendations is None:
            raise HTTPException(
                status_code=500,
                detail="추천 데이터를 가져오는 중 오류가 발생했습니다."
            )
        
        # GoormPlay Content Service 호환 형식으로 응답
        return {
            "contentIds": recommendations.movies
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Bulk IDs API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.post(
    "/recommended",
    summary="사용자별 영화 추천 저장",
    description="특정 사용자의 추천 영화 목록을 Redis에 저장합니다."
)
async def set_user_movie_recommendations(request: SetRecommendationRequest):
    """
    **사용자별 영화 추천 저장 API**
    
    - **기능**: Redis에 사용자별 추천 영화 목록 저장
    - **요청**: 사용자 ID, 영화 목록, 만료 시간
    
    **사용 예시:**
    ```json
    {
        "user_id": "user123",
        "movies": ["6837be17aec8b2058fac893a", "6837be17aec8b2058fac893b"],
        "expire_seconds": 3600
    }
    ```
    """
    try:
        logger.info(f"추천 데이터 저장 요청 - 사용자: {request.user_id}, 영화 수: {len(request.movies)}")
        
        success = recommendation_service.set_recommendations_for_user(
            request.user_id, 
            request.movies, 
            request.expire_seconds
        )
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="추천 데이터 저장 중 오류가 발생했습니다."
            )
        
        return {
            "message": f"사용자 {request.user_id}의 추천 데이터가 성공적으로 저장되었습니다.",
            "user_id": request.user_id,
            "movie_count": len(request.movies),
            "expire_seconds": request.expire_seconds
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"추천 저장 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.delete(
    "/recommended/{user_id}",
    summary="사용자별 영화 추천 삭제",
    description="특정 사용자의 추천 데이터를 삭제합니다."
)
async def delete_user_movie_recommendations(user_id: str):
    """
    **사용자별 영화 추천 삭제 API**
    
    - **기능**: Redis에서 사용자별 추천 영화 목록 삭제
    
    **사용 예시:**
    ```
    DELETE /api/contents/recommended/user123
    ```
    """
    try:
        logger.info(f"추천 데이터 삭제 요청 - 사용자 ID: {user_id}")
        
        success = recommendation_service.delete_recommendations_for_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail="삭제할 추천 데이터가 없거나 삭제 중 오류가 발생했습니다."
            )
        
        return {
            "message": f"사용자 {user_id}의 추천 데이터가 성공적으로 삭제되었습니다.",
            "user_id": user_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"추천 삭제 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.get(
    "/recommended/users",
    summary="추천 데이터가 있는 사용자 목록",
    description="현재 Redis에 추천 데이터가 저장된 모든 사용자의 목록을 반환합니다."
)
async def get_users_with_recommendations():
    """
    **추천 데이터 보유 사용자 목록 API**
    
    - **기능**: Redis에 추천 데이터가 있는 모든 사용자 조회
    
    **사용 예시:**
    ```
    GET /api/contents/recommended/users
    ```
    """
    try:
        logger.info("추천 데이터 보유 사용자 목록 요청")
        
        users = recommendation_service.get_all_users_with_recommendations()
        
        return {
            "message": "추천 데이터 보유 사용자 목록을 성공적으로 조회했습니다.",
            "users": users,
            "total_count": len(users)
        }
        
    except Exception as e:
        logger.error(f"사용자 목록 조회 API 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="서버 내부 오류가 발생했습니다."
        )

@router.get(
    "/recommended/health",
    summary="서비스 상태 확인",
    description="추천 서비스와 Redis 연결 상태를 확인합니다."
)
async def health_check():
    """서비스 헬스 체크"""
    try:
        # Redis 연결 테스트
        redis_service = recommendation_service.redis_service
        redis_service.redis_client.ping()
        
        return {
            "status": "healthy",
            "service": "movie-recommendation-service",
            "redis": "connected",
            "message": "모든 서비스가 정상 작동 중입니다.",
            "goormplay_compatible": True,
            "default_recommendation_count": 10,
            "api_path": "/api/contents/recommended"
        }
    except Exception as e:
        logger.error(f"헬스 체크 실패: {e}")
        raise HTTPException(
            status_code=503,
            detail="서비스가 현재 사용할 수 없습니다."
        )
