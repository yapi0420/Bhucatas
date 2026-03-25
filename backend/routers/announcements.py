from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import require_admin
import models, schemas

router = APIRouter(prefix="/api/announcements", tags=["校园公告"])


def _enrich(a: models.Announcement) -> schemas.AnnouncementOut:
    return schemas.AnnouncementOut(
        id=a.id, author_id=a.author_id,
        author_name=a.author.username if a.author else "",
        title=a.title, content=a.content,
        created_at=a.created_at
    )


@router.get("", response_model=List[schemas.AnnouncementOut])
def list_announcements(db: Session = Depends(get_db)):
    items = db.query(models.Announcement).options(
        joinedload(models.Announcement.author)
    ).order_by(models.Announcement.created_at.desc()).all()
    return [_enrich(a) for a in items]


@router.post("", response_model=schemas.AnnouncementOut)
def create_announcement(data: schemas.AnnouncementCreate,
                        admin: models.User = Depends(require_admin),
                        db: Session = Depends(get_db)):
    ann = models.Announcement(author_id=admin.id, **data.model_dump())
    db.add(ann)
    db.commit()
    db.refresh(ann)
    ann.author = admin
    return _enrich(ann)


@router.delete("/{ann_id}")
def delete_announcement(ann_id: int, admin: models.User = Depends(require_admin),
                        db: Session = Depends(get_db)):
    ann = db.query(models.Announcement).filter(models.Announcement.id == ann_id).first()
    if not ann:
        raise HTTPException(404, "公告不存在")
    db.delete(ann)
    db.commit()
    return {"msg": "已删除"}