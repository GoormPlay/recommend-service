from fastapi import FastAPI
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.routers import recommendation
import uvicorn

# FastAPI 앱 생성
app = FastAPI(
    title="영화 추천 서비스",
    description="사용자별 영화 추천 데이터를 관리하는 간단한 API 서비스",
    version="1.0.0"
)

# 라우터 등록
app.include_router(recommendation.router)

# 루트 엔드포인트
@app.get("/")
async def root():
    return {
        "service": "영화 추천 서비스",
        "version": "1.0.0",
        "status": "running",
        "description": "사용자별 영화 추천 데이터 관리 서비스",
        "endpoints": {
            "docs": "/docs",
            "health": "/api/contents/recommended/health",
            "get_recommendations": "/api/contents/recommended/{user_id}",
            "set_recommendations": "/api/contents/recommended",
            "delete_recommendations": "/api/contents/recommended/{user_id}"
        }
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
