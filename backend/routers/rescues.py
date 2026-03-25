from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import get_current_user, require_admin
import models, schemas

router = APIRouter(prefix="/api/rescues", tags=["救助求助"])


def _enrich(r: models.Rescue) -> schemas.RescueOut:
    return schemas.RescueOut(
        id=r.id, user_id=r.user_id,
        username=r.user.username if r.user else "",
        location=r.location, description=r.description,
        status=r.status, note=r.note or "",
        created_at=r.created_at
    )


@router.get("", response_model=List[schemas.RescueOut])
def list_rescues(db: Session = Depends(get_db)):
    items = db.query(models.Rescue).options(
        joinedload(models.Rescue.user)
    ).order_by(models.Rescue.created_at.desc()).all()
    return [_enrich(r) for r in items]


@router.post("", response_model=schemas.RescueOut)
def create_rescue(data: schemas.RescueCreate,
                  user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    rescue = models.Rescue(user_id=user.id, **data.model_dump())
    db.add(rescue)
    db.commit()
    db.refresh(rescue)
    rescue.user = user
    return _enrich(rescue)


@router.put("/{rescue_id}/resolve", response_model=schemas.RescueOut)
def resolve_rescue(rescue_id: int, data: schemas.RescueResolve,
                   admin: models.User = Depends(require_admin),
                   db: Session = Depends(get_db)):
    rescue = db.query(models.Rescue).options(
        joinedload(models.Rescue.user)
    ).filter(models.Rescue.id == rescue_id).first()
    if not rescue:
        raise HTTPException(404, "求助不存在")
    rescue.status = "已处理"
    rescue.note = data.note
    db.commit()
    db.refresh(rescue)
    return _enrich(rescue)