from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ═══════════════════════════════════════════
# 数据库配置 —— 按需切换
# ═══════════════════════════════════════════

# 方式一：SQLite（开发测试用，零配置）
DATABASE_URL = "sqlite:///./campus_cat.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 方式二：MySQL（生产环境）
# DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/campus_cat?charset=utf8mb4"
# engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10)

# 方式三：PostgreSQL
# DATABASE_URL = "postgresql://user:password@localhost:5432/campus_cat"
# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()