from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config import settings
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    JWT 토큰을 검증하고 사용자 정보를 반환합니다.
    GoormPlay의 Auth Service에서 발급한 토큰을 검증합니다.
    
    Args:
        credentials: HTTP Bearer 토큰
        
    Returns:
        JWT 페이로드 (사용자 정보 포함)
        
    Raises:
        HTTPException: 토큰이 유효하지 않은 경우
    """
    try:
        # JWT 토큰 디코딩 및 검증
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # 필수 클레임 확인
        user_id = payload.get("sub")  # subject = memberId
        username = payload.get("username")
        role = payload.get("role")
        
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="토큰에 사용자 ID가 없습니다."
            )
        
        logger.info(f"JWT 인증 성공 - 사용자: {username} (ID: {user_id})")
        
        return {
            "user_id": user_id,
            "username": username,
            "role": role
        }
        
    except JWTError as e:
        logger.error(f"JWT 검증 실패: {e}")
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 토큰입니다."
        )
    except Exception as e:
        logger.error(f"인증 처리 중 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail="인증 처리 중 오류가 발생했습니다."
        )

async def get_current_user(token_data: dict = Depends(verify_jwt_token)) -> dict:
    """
    현재 사용자 정보를 반환합니다.
    
    Args:
        token_data: JWT에서 추출한 사용자 정보
        
    Returns:
        사용자 정보 딕셔너리
    """
    return token_data