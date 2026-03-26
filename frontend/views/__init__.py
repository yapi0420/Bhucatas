"""
页面注册表 —— 统一管理所有页面的导入
app.py 只需 from views import PAGE_REGISTRY
"""
# 包内模块：使用相对导入
from .home import page_home
from .catalog import page_catalog
from .detail import page_detail
from .feeding import page_feeding
from .lost import page_lost
from .adoption import page_adoption
from .rescue import page_rescue
from .comments import page_comments
from .announcements import page_announcements
from .profile import page_profile
from .admin import page_admin

# 外部模块：使用绝对导入
from config import (
    PAGE_HOME, PAGE_CATALOG, PAGE_DETAIL, PAGE_FEEDING,
    PAGE_LOST, PAGE_ADOPTION, PAGE_RESCUE, PAGE_COMMENTS,
    PAGE_ANNOUNCE, PAGE_PROFILE, PAGE_ADMIN,
)

# 路由名 → 渲染函数
PAGE_REGISTRY = {
    PAGE_HOME: page_home,
    PAGE_CATALOG: page_catalog,
    PAGE_DETAIL: page_detail,
    PAGE_FEEDING: page_feeding,
    PAGE_LOST: page_lost,
    PAGE_ADOPTION: page_adoption,
    PAGE_RESCUE: page_rescue,
    PAGE_COMMENTS: page_comments,
    PAGE_ANNOUNCE: page_announcements,
    PAGE_PROFILE: page_profile,
    PAGE_ADMIN: page_admin,
}