from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import get_current_user
import models, schemas

router = APIRouter(prefix="/api/lost", tags=["寻猫启事"])


def _enrich(n: models.LostNotice) -> schemas.LostOut:
    return schemas.LostOut(
        id=n.id, user_id=n.user_id,
        username=n.user.username if n.user else "",
        cat_name=n.cat_name, description=n.description,
        location=n.location, found=n.found,
        found_note=n.found_note or "", created_at=n.created_at
    )


@router.get("", response_model=List[schemas.LostOut])
def list_lost(db: Session = Depends(get_db)):
    items = db.query(models.LostNotice).options(
        joinedload(models.LostNotice.user)
    ).order_by(models.LostNotice.created_at.desc()).all()
    return [_enrich(n) for n in items]


@router.post("", response_model=schemas.LostOut)
def create_lost(data: schemas.LostCreate,
                user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    notice = models.LostNotice(user_id=user.id, **data.model_dump())
    db.add(notice)
    db.commit()
    db.refresh(notice)
    notice.user = user
    return _enrich(notice)


@router.put("/{notice_id}/found", response_model=schemas.LostOut)
def mark_found(notice_id: int, data: schemas.LostMarkFound,
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    notice = db.query(models.LostNotice).options(
        joinedload(models.LostNotice.user)
    ).filter(models.LostNotice.id == notice_id).first()
    if not notice:
        raise HTTPException(404, "启事不存在")
    if notice.user_id != user.id and user.role != "admin":
        raise HTTPException(403, "无权操作")
    notice.found = True
    notice.found_note = data.found_note
    db.commit()
    db.refresh(notice)
    return _enrich(notice)