from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import get_current_user, require_admin
import models, schemas

router = APIRouter(prefix="/api/adoptions", tags=["领养"])


def _enrich(a: models.AdoptionApplication) -> schemas.AdoptionOut:
    return schemas.AdoptionOut(
        id=a.id, user_id=a.user_id,
        username=a.user.username if a.user else "",
        cat_id=a.cat_id,
        cat_name=a.cat.name if a.cat else "",
        reason=a.reason, contact=a.contact,
        status=a.status, created_at=a.created_at
    )


@router.get("", response_model=List[schemas.AdoptionOut])
def list_adoptions(user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    q = db.query(models.AdoptionApplication).options(
        joinedload(models.AdoptionApplication.user),
        joinedload(models.AdoptionApplication.cat),
    )
    if user.role != "admin":
        q = q.filter(models.AdoptionApplication.user_id == user.id)
    items = q.order_by(models.AdoptionApplication.created_at.desc()).all()
    return [_enrich(a) for a in items]


@router.post("", response_model=schemas.AdoptionOut)
def create_adoption(data: schemas.AdoptionCreate,
                    user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    app = models.AdoptionApplication(user_id=user.id, **data.model_dump())
    db.add(app)
    db.commit()
    db.refresh(app)
    app = db.query(models.AdoptionApplication).options(
        joinedload(models.AdoptionApplication.user),
        joinedload(models.AdoptionApplication.cat),
    ).filter(models.AdoptionApplication.id == app.id).first()
    return _enrich(app)


@router.put("/{app_id}/review", response_model=schemas.AdoptionOut)
def review_adoption(app_id: int, data: schemas.AdoptionReview,
                    admin: models.User = Depends(require_admin),
                    db: Session = Depends(get_db)):
    app = db.query(models.AdoptionApplication).options(
        joinedload(models.AdoptionApplication.user),
        joinedload(models.AdoptionApplication.cat),
    ).filter(models.AdoptionApplication.id == app_id).first()
    if not app:
        raise HTTPException(404, "申请不存在")
    app.status = data.status
    # 通过后更新猫猫状态
    if data.status == "已通过" and app.cat:
        app.cat.status = "已收养"
    db.commit()
    db.refresh(app)
    return _enrich(app)