from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, Text,
    DateTime, ForeignKey, JSON, UniqueConstraint
)
from sqlalchemy.orm import relationship
from database import Base

# ╔══════════════════════════════════════════╗
# ║         所有 SQLAlchemy 数据模型          ║
# ╚══════════════════════════════════════════╝


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    nickname = Column(String(50), default="")
    avatar = Column(String(10), default="👤")
    role = Column(String(20), default="user")  # user / certified / admin
    created_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship("Comment", back_populates="user")
    feedings = relationship("Feeding", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")


class Cat(Base):
    __tablename__ = "cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    emoji = Column(String(10), default="🐱")
    color = Column(String(20), default="#FF8C00")
    gender = Column(String(10))           # ♂ 公 / ♀ 母
    age = Column(String(20))
    breed = Column(String(50), default="中华田园猫")
    fur = Column(String(50))              # 毛色特征
    neutered = Column(Boolean, default=False)
    status = Column(String(20), default="在校")  # 在校/走失/待收养/已收养/回喵星
    area = Column(String(100))            # 常出没区域
    personality = Column(JSON, default=list)
    vaccine = Column(Boolean, default=False)
    deworm = Column(Boolean, default=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("CatEvent", back_populates="cat", cascade="all,delete-orphan",
                          order_by="CatEvent.event_date")
    relations = relationship("CatRelation", back_populates="cat",
                             foreign_keys="CatRelation.cat_id", cascade="all,delete-orphan")
    photos = relationship("CatPhoto", back_populates="cat", cascade="all,delete-orphan")
    comments = relationship("Comment", back_populates="cat")
    feedings = relationship("Feeding", back_populates="cat")


class CatEvent(Base):
    """猫猫事件时间线"""
    __tablename__ = "cat_events"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)
    event_date = Column(String(20))
    event_type = Column(String(50))       # 🔍 发现 / ✂️ 绝育 / 💉 疫苗 ...
    description = Column(Text)

    cat = relationship("Cat", back_populates="events")


class CatRelation(Base):
    """猫猫社交关系"""
    __tablename__ = "cat_relations"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)
    related_cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    related_cat_name = Column(String(50))
    relation_type = Column(String(50))    # 父子 / 好朋友 / 冤家 ...

    cat = relationship("Cat", back_populates="relations", foreign_keys=[cat_id])
    related_cat = relationship("Cat", foreign_keys=[related_cat_id])


class CatPhoto(Base):
    """猫猫相册"""
    __tablename__ = "cat_photos"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255))
    caption = Column(String(200), default="")
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    cat = relationship("Cat", back_populates="photos")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    content = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    cat = relationship("Cat", back_populates="comments")
    replies = relationship("CommentReply", back_populates="comment", cascade="all,delete-orphan")


class CommentReply(Base):
    """楼中楼回复"""
    __tablename__ = "comment_replies"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    comment = relationship("Comment", back_populates="replies")
    user = relationship("User")


class Feeding(Base):
    """投喂打卡"""
    __tablename__ = "feedings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    location = Column(String(100))
    food = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedings")
    cat = relationship("Cat", back_populates="feedings")


class LostNotice(Base):
    """寻猫启事"""
    __tablename__ = "lost_notices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cat_name = Column(String(50))
    description = Column(Text)
    location = Column(String(100))
    found = Column(Boolean, default=False)
    found_note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class AdoptionApplication(Base):
    """领养申请"""
    __tablename__ = "adoption_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    reason = Column(Text)
    contact = Column(String(50))
    status = Column(String(20), default="审核中")  # 审核中 / 已通过 / 已拒绝
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    cat = relationship("Cat")


class Rescue(Base):
    """救助求助"""
    __tablename__ = "rescues"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location = Column(String(100))
    description = Column(Text)
    status = Column(String(20), default="求助中")  # 求助中 / 已处理
    note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class Announcement(Base):
    """校园公告"""
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User")


class Favorite(Base):
    """收藏猫猫"""
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "cat_id"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    cat = relationship("Cat")


class Followup(Base):
    """领养回访"""
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("cats.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    status = Column(String(20))  # 良好 / 一般 / 需关注
    created_at = Column(DateTime, default=datetime.utcnow)

    cat = relationship("Cat")
    user = relationship("User")