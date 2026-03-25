from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database import get_db
from deps import require_admin
import models, schemas

router = APIRouter(prefix="/api/admin", tags=["管理后台"])


@router.get("/stats", response_model=schemas.DashboardStats)
def dashboard_stats(admin: models.User = Depends(require_admin),
                    db: Session = Depends(get_db)):
    cats = db.query(models.Cat).all()
    return schemas.DashboardStats(
        total_cats=len(cats),
        on_campus=len([c for c in cats if c.status == "在校"]),
        adopted=len([c for c in cats if c.status == "已收养"]),
        rainbow=len([c for c in cats if c.status == "回喵星"]),
        waiting_adopt=len([c for c in cats if c.status == "待收养"]),
        lost=len([c for c in cats if c.status == "走失"]),
        total_users=db.query(func.count(models.User.id)).scalar(),
        total_feedings=db.query(func.count(models.Feeding.id)).scalar(),
        total_comments=db.query(func.count(models.Comment.id)).scalar(),
        pending_adoptions=db.query(func.count(models.AdoptionApplication.id)).filter(
            models.AdoptionApplication.status == "审核中"
        ).scalar(),
    )


@router.get("/users", response_model=List[schemas.UserOut])
def list_users(admin: models.User = Depends(require_admin),
               db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.id).all()


@router.put("/users/{user_id}/role", response_model=schemas.UserOut)
def update_user_role(user_id: int, data: schemas.RoleUpdate,
                     admin: models.User = Depends(require_admin),
                     db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(404, "用户不存在")
    if data.role not in ["user", "certified", "admin"]:
        raise HTTPException(400, "无效角色")
    user.role = data.role
    db.commit()
    db.refresh(user)
    return user


@router.get("/backup")
def backup_data(admin: models.User = Depends(require_admin),
                db: Session = Depends(get_db)):
    """导出全部数据为 JSON"""
    cats = db.query(models.Cat).all()
    users = db.query(models.User).all()
    return {
        "cats": [{"id":c.id,"name":c.name,"status":c.status,"gender":c.gender,
                  "age":c.age,"area":c.area,"neutered":c.neutered} for c in cats],
        "users": [{"id":u.id,"username":u.username,"nickname":u.nickname,
                   "role":u.role} for u in users],
        "total_feedings": db.query(func.count(models.Feeding.id)).scalar(),
        "total_comments": db.query(func.count(models.Comment.id)).scalar(),
    }