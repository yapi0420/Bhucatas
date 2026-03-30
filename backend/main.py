from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
# import os
from database import engine, Base
from init_data import init

# 创建所有表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🐱 北华大学猫猫校园 API",
    description="Campus Cat Backend API",
    version="1.0.0",
)
# ── CORS 跨域（允许 Streamlit 前端访问）──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 静态文件服务（猫猫照片）──
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")



# ── 注册所有路由 ──
from routers import auth, cats, comments, feedings, lost, adoptions
from routers import rescues, announcements, favorites, followups, admin

app.include_router(auth.router)
app.include_router(cats.router)
app.include_router(comments.router)
app.include_router(feedings.router)
app.include_router(lost.router)
app.include_router(adoptions.router)
app.include_router(rescues.router)
app.include_router(announcements.router)
app.include_router(favorites.router)
app.include_router(followups.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"msg": "🐱 北华大学猫猫校园 API 运行中", "docs": "/docs"}


@app.on_event("startup")
def startup():
    init()  # 首次启动时填充种子数据


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)