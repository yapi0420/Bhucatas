from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import Optional, List
from database import get_db
from deps import get_current_user
import models, schemas

router = APIRouter(prefix="/api/feedings", tags=["投喂打卡"])


def _enrich(f: models.Feeding) -> schemas.FeedingOut:
    return schemas.FeedingOut(
        id=f.id, user_id=f.user_id,
        username=f.user.username if f.user else "",
        cat_id=f.cat_id,
        cat_name=f.cat.name if f.cat else "",
        location=f.location, food=f.food, created_at=f.created_at
    )


@router.get("", response_model=List[schemas.FeedingOut])
def list_feedings(
    cat_id: Optional[int] = None,
    user_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    q = db.query(models.Feeding).options(
        joinedload(models.Feeding.user),
        joinedload(models.Feeding.cat),
    )
    if cat_id:
        q = q.filter(models.Feeding.cat_id == cat_id)
    if user_id:
        q = q.filter(models.Feeding.user_id == user_id)
    items = q.order_by(models.Feeding.created_at.desc()).limit(limit).all()
    return [_enrich(f) for f in items]


@router.post("", response_model=schemas.FeedingOut)
def create_feeding(data: schemas.FeedingCreate,
                   user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    feeding = models.Feeding(
        user_id=user.id, cat_id=data.cat_id,
        location=data.location, food=data.food
    )
    db.add(feeding)
    db.commit()
    db.refresh(feeding)
    feeding = db.query(models.Feeding).options(
        joinedload(models.Feeding.user),
        joinedload(models.Feeding.cat),
    ).filter(models.Feeding.id == feeding.id).first()
    return _enrich(feeding)


@router.get("/stats", response_model=List[schemas.FeedingStats])
def feeding_stats(db: Session = Depends(get_db)):
    """各猫猫投喂次数统计"""
    results = db.query(
        models.Cat.name,
        func.count(models.Feeding.id).label("count")
    ).join(models.Cat).group_by(models.Cat.name).order_by(
        func.count(models.Feeding.id).desc()
    ).all()
    return [schemas.FeedingStats(cat_name=r[0], count=r[1]) for r in results]