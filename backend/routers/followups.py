from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import get_current_user
import models, schemas

router = APIRouter(prefix="/api/followups", tags=["领养回访"])


def _enrich(f: models.Followup) -> schemas.FollowupOut:
    return schemas.FollowupOut(
        id=f.id, cat_id=f.cat_id,
        cat_name=f.cat.name if f.cat else "",
        user_id=f.user_id,
        username=f.user.username if f.user else "",
        content=f.content, status=f.status,
        created_at=f.created_at
    )


@router.get("", response_model=List[schemas.FollowupOut])
def list_followups(db: Session = Depends(get_db)):
    items = db.query(models.Followup).options(
        joinedload(models.Followup.cat),
        joinedload(models.Followup.user),
    ).order_by(models.Followup.created_at.desc()).all()
    return [_enrich(f) for f in items]


@router.post("", response_model=schemas.FollowupOut)
def create_followup(data: schemas.FollowupCreate,
                    user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    fu = models.Followup(user_id=user.id, **data.model_dump())
    db.add(fu)
    db.commit()
    db.refresh(fu)
    fu = db.query(models.Followup).options(
        joinedload(models.Followup.cat),
        joinedload(models.Followup.user),
    ).filter(models.Followup.id == fu.id).first()
    return _enrich(fu)