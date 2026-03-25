from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ╔══════════════════════════════════════════╗
# ║       所有 Pydantic 请求/响应模型          ║
# ╚══════════════════════════════════════════╝


# ═══════════ Token ═══════════
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserOut"


# ═══════════ User ═══════════
class UserCreate(BaseModel):
    username: str
    password: str
    nickname: str = ""

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    nickname: str
    avatar: str
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None

class PasswordChange(BaseModel):
    old_password: str
    new_password: str

class RoleUpdate(BaseModel):
    role: str


# ═══════════ Cat ═══════════
class CatEventOut(BaseModel):
    id: int
    event_date: str
    event_type: str
    description: str
    class Config:
        from_attributes = True

class CatEventCreate(BaseModel):
    event_date: str
    event_type: str
    description: str

class CatRelationOut(BaseModel):
    id: int
    related_cat_id: int
    related_cat_name: str
    relation_type: str
    class Config:
        from_attributes = True

class CatRelationCreate(BaseModel):
    related_cat_id: int
    related_cat_name: str
    relation_type: str

class CatPhotoOut(BaseModel):
    id: int
    file_path: str
    caption: str
    created_at: datetime
    class Config:
        from_attributes = True

class CatCreate(BaseModel):
    name: str
    emoji: str = "🐱"
    color: str = "#FF8C00"
    gender: str = "♂ 公"
    age: str = "未知"
    breed: str = "中华田园猫"
    fur: str = ""
    neutered: bool = False
    status: str = "在校"
    area: str = ""
    personality: List[str] = []
    vaccine: bool = False
    deworm: bool = False
    description: str = ""

class CatUpdate(BaseModel):
    name: Optional[str] = None
    emoji: Optional[str] = None
    color: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    fur: Optional[str] = None
    neutered: Optional[bool] = None
    status: Optional[str] = None
    area: Optional[str] = None
    personality: Optional[List[str]] = None
    vaccine: Optional[bool] = None
    deworm: Optional[bool] = None
    description: Optional[str] = None

class CatBrief(BaseModel):
    """列表用简要信息"""
    id: int
    name: str
    emoji: str
    color: str
    gender: str
    age: str
    breed: str
    fur: str
    neutered: bool
    status: str
    area: str
    personality: List[str]
    vaccine: bool
    deworm: bool
    class Config:
        from_attributes = True

class CatDetail(BaseModel):
    """详情页完整信息"""
    id: int
    name: str
    emoji: str
    color: str
    gender: str
    age: str
    breed: str
    fur: str
    neutered: bool
    status: str
    area: str
    personality: List[str]
    vaccine: bool
    deworm: bool
    description: str
    events: List[CatEventOut]
    relations: List[CatRelationOut]
    photos: List[CatPhotoOut]
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Comment ═══════════
class CommentReplyCreate(BaseModel):
    content: str

class CommentReplyOut(BaseModel):
    id: int
    comment_id: int
    user_id: int
    username: str = ""
    content: str
    created_at: datetime
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    cat_id: int
    content: str

class CommentOut(BaseModel):
    id: int
    user_id: int
    username: str = ""
    cat_id: int
    cat_name: str = ""
    content: str
    likes: int
    replies: List[CommentReplyOut] = []
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Feeding ═══════════
class FeedingCreate(BaseModel):
    cat_id: int
    location: str
    food: str

class FeedingOut(BaseModel):
    id: int
    user_id: int
    username: str = ""
    cat_id: int
    cat_name: str = ""
    location: str
    food: str
    created_at: datetime
    class Config:
        from_attributes = True

class FeedingStats(BaseModel):
    cat_name: str
    count: int


# ═══════════ Lost Notice ═══════════
class LostCreate(BaseModel):
    cat_name: str
    description: str
    location: str

class LostMarkFound(BaseModel):
    found_note: str = ""

class LostOut(BaseModel):
    id: int
    user_id: int
    username: str = ""
    cat_name: str
    description: str
    location: str
    found: bool
    found_note: str
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Adoption ═══════════
class AdoptionCreate(BaseModel):
    cat_id: int
    reason: str
    contact: str

class AdoptionReview(BaseModel):
    status: str   # 已通过 / 已拒绝

class AdoptionOut(BaseModel):
    id: int
    user_id: int
    username: str = ""
    cat_id: int
    cat_name: str = ""
    reason: str
    contact: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Rescue ═══════════
class RescueCreate(BaseModel):
    location: str
    description: str

class RescueResolve(BaseModel):
    note: str = ""

class RescueOut(BaseModel):
    id: int
    user_id: int
    username: str = ""
    location: str
    description: str
    status: str
    note: str
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Announcement ═══════════
class AnnouncementCreate(BaseModel):
    title: str
    content: str

class AnnouncementOut(BaseModel):
    id: int
    author_id: int
    author_name: str = ""
    title: str
    content: str
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Followup ═══════════
class FollowupCreate(BaseModel):
    cat_id: int
    content: str
    status: str = "良好"

class FollowupOut(BaseModel):
    id: int
    cat_id: int
    cat_name: str = ""
    user_id: int
    username: str = ""
    content: str
    status: str
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Favorite ═══════════
class FavoriteOut(BaseModel):
    cat_id: int
    cat: CatBrief
    created_at: datetime
    class Config:
        from_attributes = True


# ═══════════ Admin Stats ═══════════
class DashboardStats(BaseModel):
    total_cats: int
    on_campus: int
    adopted: int
    rainbow: int
    waiting_adopt: int
    lost: int
    total_users: int
    total_feedings: int
    total_comments: int
    pending_adoptions: int


# 解决循环引用
Token.model_rebuild()