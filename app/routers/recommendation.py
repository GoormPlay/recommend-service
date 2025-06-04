from fastapi import APIRouter, HTTPException
from app.models.recommendation import RecommendationResponse, SetRecommendationRequest
from app.services.recommendation_service import RecommendationService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contents", tags=["contents"])
recommendation_service = RecommendationService()

# 서비스 상태 확인
@router.get("/recommended/health")
async def health_check():
    """서비스 상태 확인"""
    logger.info("헬스 체크 요청")
    return {
        "status": "healthy",
        "service": "movie-recommendation-service",
        "message": "서비스가 정상적으로 작동 중입니다"
    }

# 사용자별 영화 추천 조회
@router.get("/recommended/{user_id}", response_model=RecommendationResponse)
async def get_user_movie_recommendations(user_id: str):
    """
    사용자별 영화 추천 목록을 조회합니다.
    
    Args:
        user_id: 사용자 ID
        
    Returns:
        사용자별 추천 영화 목록
    """
    logger.info(f"영화 추천 요청 - 사용자 ID: {user_id}")
    
    try:
        recommendations = recommendation_service.get_recommendations_for_user(user_id)
        return recommendations
    except Exception as e:
        logger.error(f"추천 조회 오류 (user_id: {user_id}): {e}")
        raise HTTPException(status_code=500, detail="추천 데이터 조회 중 오류가 발생했습니다")

# 사용자별 영화 추천 저장
@router.post("/recommended")
async def set_user_movie_recommendations(request: SetRecommendationRequest):
    """
    사용자별 영화 추천 목록을 저장합니다.
    
    Args:
        request: 추천 저장 요청 (user_id, movies, expire_seconds)
        
    Returns:
        저장 결과
    """
    logger.info(f"영화 추천 저장 요청 - 사용자 ID: {request.user_id}, 영화 수: {len(request.movies)}")
    
    try:
        success = recommendation_service.set_recommendations_for_user(
            request.user_id, 
            request.movies, 
            request.expire_seconds
        )
        
        if success:
            return {
                "status": "success",
                "message": f"사용자 {request.user_id}의 추천 데이터가 저장되었습니다",
                "user_id": request.user_id,
                "movie_count": len(request.movies),
                "expire_seconds": request.expire_seconds
            }
        else:
            raise HTTPException(status_code=500, detail="추천 데이터 저장에 실패했습니다")
            
    except Exception as e:
        logger.error(f"추천 저장 오류 (user_id: {request.user_id}): {e}")
        raise HTTPException(status_code=500, detail="추천 데이터 저장 중 오류가 발생했습니다")

# 사용자별 영화 추천 삭제
@router.delete("/recommended/{user_id}")
async def delete_user_movie_recommendations(user_id: str):
    """
    사용자별 영화 추천 목록을 삭제합니다.
    
    Args:
        user_id: 사용자 ID
        
    Returns:
        삭제 결과
    """
    logger.info(f"영화 추천 삭제 요청 - 사용자 ID: {user_id}")
    
    try:
        success = recommendation_service.delete_recommendations_for_user(user_id)
        
        if success:
            return {
                "status": "success",
                "message": f"사용자 {user_id}의 추천 데이터가 삭제되었습니다",
                "user_id": user_id
            }
        else:
            return {
                "status": "not_found",
                "message": f"사용자 {user_id}의 추천 데이터가 존재하지 않습니다",
                "user_id": user_id
            }
            
    except Exception as e:
        logger.error(f"추천 삭제 오류 (user_id: {user_id}): {e}")
        raise HTTPException(status_code=500, detail="추천 데이터 삭제 중 오류가 발생했습니다")
