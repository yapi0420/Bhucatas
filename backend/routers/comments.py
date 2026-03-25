from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from database import get_db
from deps import get_current_user, get_optional_user, require_admin
import models, schemas

router = APIRouter(prefix="/api/comments", tags=["评论"])


def _enrich(comment: models.Comment) -> schemas.CommentOut:
    """把 ORM 对象转成带 username/cat_name 的响应"""
    return schemas.CommentOut(
        id=comment.id,
        user_id=comment.user_id,
        username=comment.user.username if comment.user else "",
        cat_id=comment.cat_id,
        cat_name=comment.cat.name if comment.cat else "",
        content=comment.content,
        likes=comment.likes,
        created_at=comment.created_at,
        replies=[
            schemas.CommentReplyOut(
                id=r.id, comment_id=r.comment_id, user_id=r.user_id,
                username=r.user.username if r.user else "",
                content=r.content, created_at=r.created_at
            ) for r in comment.replies
        ]
    )


@router.get("", response_model=List[schemas.CommentOut])
def list_comments(
    cat_id: Optional[int] = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    q = db.query(models.Comment).options(
        joinedload(models.Comment.user),
        joinedload(models.Comment.cat),
        joinedload(models.Comment.replies).joinedload(models.CommentReply.user),
    )
    if cat_id:
        q = q.filter(models.Comment.cat_id == cat_id)
    comments = q.order_by(models.Comment.created_at.desc()).limit(limit).all()
    return [_enrich(c) for c in comments]


@router.post("", response_model=schemas.CommentOut)
def create_comment(data: schemas.CommentCreate,
                   user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    comment = models.Comment(user_id=user.id, cat_id=data.cat_id, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    # reload relationships
    comment = db.query(models.Comment).options(
        joinedload(models.Comment.user),
        joinedload(models.Comment.cat),
    ).filter(models.Comment.id == comment.id).first()
    return _enrich(comment)


@router.post("/{comment_id}/like")
def like_comment(comment_id: int, user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "评论不存在")
    comment.likes += 1
    db.commit()
    return {"likes": comment.likes}


@router.post("/{comment_id}/reply", response_model=schemas.CommentReplyOut)
def reply_comment(comment_id: int, data: schemas.CommentReplyCreate,
                  user: models.User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "评论不存在")
    reply = models.CommentReply(comment_id=comment_id, user_id=user.id, content=data.content)
    db.add(reply)
    db.commit()
    db.refresh(reply)
    return schemas.CommentReplyOut(
        id=reply.id, comment_id=reply.comment_id, user_id=reply.user_id,
        username=user.username, content=reply.content, created_at=reply.created_at
    )


@router.delete("/{comment_id}")
def delete_comment(comment_id: int,
                   user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "评论不存在")
    if comment.user_id != user.id and user.role != "admin":
        raise HTTPException(403, "无权删除")
    db.delete(comment)
    db.commit()
    return {"msg": "已删除"}