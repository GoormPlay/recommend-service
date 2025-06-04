import redis
import json
import logging
from typing import Optional, List
from app.config import settings

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        """Redis 클라이언트 초기화"""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password if settings.redis_password else None,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # 연결 테스트
            self.redis_client.ping()
            logger.info("Redis 연결 성공")
        except Exception as e:
            logger.error(f"Redis 연결 실패: {e}")
            raise

    def get_user_recommendations(self, user_id: str) -> Optional[List[str]]:
        """
        사용자별 추천 영화 목록을 Redis에서 가져옵니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            추천 영화 ID 리스트 또는 None
        """
        try:
            key = f"user_recommendations:{user_id}"
            data = self.redis_client.get(key)
            
            if not data:
                logger.info(f"사용자 {user_id}의 추천 데이터가 없습니다.")
                return None
            
            recommendation_data = json.loads(data)
            
            if isinstance(recommendation_data, dict) and "recommend_movie" in recommendation_data:
                movies = recommendation_data["recommend_movie"]
                logger.info(f"사용자 {user_id}의 추천 영화 {len(movies)}개 조회 성공")
                return movies
            elif isinstance(recommendation_data, list):
                logger.info(f"사용자 {user_id}의 추천 영화 {len(recommendation_data)}개 조회 성공")
                return recommendation_data
            else:
                logger.warning(f"사용자 {user_id}의 추천 데이터 형식이 올바르지 않습니다")
                return None
                
        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류 (user_id: {user_id}): {e}")
            return None
        except Exception as e:
            logger.error(f"Redis 조회 오류 (user_id: {user_id}): {e}")
            return None

    def set_user_recommendations(self, user_id: str, movies: List[str], expire_seconds: int = 3600) -> bool:
        """
        사용자별 추천 영화 목록을 Redis에 저장합니다.
        
        Args:
            user_id: 사용자 ID
            movies: 추천 영화 ID 리스트
            expire_seconds: 만료 시간 (초)
            
        Returns:
            저장 성공 여부
        """
        try:
            key = f"user_recommendations:{user_id}"
            data = {
                "user_id": user_id,
                "recommend_movie": movies
            }
            
            result = self.redis_client.setex(
                key, 
                expire_seconds, 
                json.dumps(data, ensure_ascii=False)
            )
            
            logger.info(f"사용자 {user_id}의 추천 데이터 저장 완료 (TTL: {expire_seconds}초)")
            return result
            
        except Exception as e:
            logger.error(f"Redis 저장 오류 (user_id: {user_id}): {e}")
            return False

    def delete_user_recommendations(self, user_id: str) -> bool:
        """
        사용자의 추천 데이터를 삭제합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            삭제 성공 여부
        """
        try:
            key = f"user_recommendations:{user_id}"
            result = self.redis_client.delete(key)
            
            if result:
                logger.info(f"사용자 {user_id}의 추천 데이터 삭제 완료")
                return True
            else:
                logger.info(f"사용자 {user_id}의 추천 데이터가 존재하지 않습니다")
                return False
                
        except Exception as e:
            logger.error(f"Redis 삭제 오류 (user_id: {user_id}): {e}")
            return False
