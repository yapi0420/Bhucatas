from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from deps import get_current_user
import models, schemas

router = APIRouter(prefix="/api/favorites", tags=["收藏"])


@router.get("", response_model=List[schemas.CatBrief])
def my_favorites(user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    favs = db.query(models.Favorite).options(
        joinedload(models.Favorite.cat)
    ).filter(models.Favorite.user_id == user.id).all()
    return [f.cat for f in favs if f.cat]


@router.post("/{cat_id}")
def add_favorite(cat_id: int, user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    exists = db.query(models.Favorite).filter(
        models.Favorite.user_id == user.id,
        models.Favorite.cat_id == cat_id
    ).first()
    if exists:
        raise HTTPException(400, "已收藏")
    fav = models.Favorite(user_id=user.id, cat_id=cat_id)
    db.add(fav)
    db.commit()
    return {"msg": "收藏成功"}


@router.delete("/{cat_id}")
def remove_favorite(cat_id: int, user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == user.id,
        models.Favorite.cat_id == cat_id
    ).first()
    if fav:
        db.delete(fav)
        db.commit()
    return {"msg": "已取消收藏"}


@router.get("/check/{cat_id}")
def check_favorite(cat_id: int, user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    exists = db.query(models.Favorite).filter(
        models.Favorite.user_id == user.id,
        models.Favorite.cat_id == cat_id
    ).first()
    return {"favorited": exists is not None}