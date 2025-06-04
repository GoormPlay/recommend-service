from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import recommendation
from app.config import settings
import logging
import uvicorn

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# FastAPI 앱 생성
app = FastAPI(
    title="GoormPlay 호환 영화 추천 서비스",
    description="GoormPlay Content Service와 호환되는 사용자별 개인화된 영화 추천 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"예상치 못한 오류: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "서버 내부 오류가 발생했습니다."}
    )

# 라우터 등록
app.include_router(recommendation.router)

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "service": "GoormPlay Compatible Movie Recommendation Service",
        "version": "1.0.0",
        "status": "running",
        "description": "GoormPlay Content Service와 호환되는 영화 추천 서비스",
        "api_base_path": "/api/contents/recommended",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/contents/recommended/health",
            "get_recommendations": "/api/contents/recommended/{user_id}",
            "bulk_ids": "/api/contents/recommended/bulk-ids",
            "set_recommendations": "/api/contents/recommended",
            "delete_recommendations": "/api/contents/recommended/{user_id}",
            "list_users": "/api/contents/recommended/users"
        },
        "goormplay_compatible": True
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.service_port,
        reload=True
    )
