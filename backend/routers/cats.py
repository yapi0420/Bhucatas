from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from database import get_db
from deps import get_current_user, require_admin
import models, schemas
import os, uuid

router = APIRouter(prefix="/api/cats", tags=["猫猫"])

UPLOAD_DIR = "uploads/cats"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("", response_model=List[schemas.CatBrief])
def list_cats(
    name: Optional[str] = None,
    gender: Optional[str] = None,
    status: Optional[str] = None,
    neutered: Optional[bool] = None,
    area: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """搜索筛选猫猫列表"""
    q = db.query(models.Cat)
    if name:
        q = q.filter(models.Cat.name.contains(name))
    if gender:
        q = q.filter(models.Cat.gender == gender)
    if status:
        q = q.filter(models.Cat.status == status)
    if neutered is not None:
        q = q.filter(models.Cat.neutered == neutered)
    if area:
        q = q.filter(models.Cat.area.contains(area))
    return q.order_by(models.Cat.id).all()


@router.get("/random", response_model=List[schemas.CatBrief])
def random_cats(count: int = Query(4, ge=1, le=10), db: Session = Depends(get_db)):
    """随机获取在校猫猫（首页推荐）"""
    from sqlalchemy.sql.expression import func
    return db.query(models.Cat).filter(
        models.Cat.status == "在校"
    ).order_by(func.random()).limit(count).all()


@router.get("/{cat_id}", response_model=schemas.CatDetail)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Cat).options(
        joinedload(models.Cat.events),
        joinedload(models.Cat.relations),
        joinedload(models.Cat.photos),
    ).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "猫猫不存在")
    return cat


@router.post("", response_model=schemas.CatDetail)
def create_cat(data: schemas.CatCreate, admin: models.User = Depends(require_admin),
               db: Session = Depends(get_db)):
    cat = models.Cat(**data.model_dump())
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/{cat_id}", response_model=schemas.CatDetail)
def update_cat(cat_id: int, data: schemas.CatUpdate,
               admin: models.User = Depends(require_admin),
               db: Session = Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "猫猫不存在")
    for key, val in data.model_dump(exclude_unset=True).items():
        setattr(cat, key, val)
    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{cat_id}")
def delete_cat(cat_id: int, admin: models.User = Depends(require_admin),
               db: Session = Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "猫猫不存在")
    db.delete(cat)
    db.commit()
    return {"msg": "已删除"}


# ────── 事件时间线 ──────
@router.post("/{cat_id}/events", response_model=schemas.CatEventOut)
def add_event(cat_id: int, data: schemas.CatEventCreate,
              admin: models.User = Depends(require_admin),
              db: Session = Depends(get_db)):
    cat = db.query(models.Cat).filter(models.Cat.id == cat_id).first()
    if not cat:
        raise HTTPException(404, "猫猫不存在")
    event = models.CatEvent(cat_id=cat_id, **data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


# ────── 关系图谱 ──────
@router.post("/{cat_id}/relations", response_model=schemas.CatRelationOut)
def add_relation(cat_id: int, data: schemas.CatRelationCreate,
                 admin: models.User = Depends(require_admin),
                 db: Session = Depends(get_db)):
    event = models.CatRelation(cat_id=cat_id, **data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


# ────── 照片上传 ──────
@router.post("/{cat_id}/photos", response_model=schemas.CatPhotoOut)
async def upload_photo(
    cat_id: int,
    file: UploadFile = File(...),
    caption: str = "",
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ext = os.path.splitext(file.filename)[1]
    filename = f"{cat_id}_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        content = await file.read()
        f.write(content)

    photo = models.CatPhoto(
        cat_id=cat_id, file_path=filepath,
        caption=caption, uploaded_by=user.id
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo