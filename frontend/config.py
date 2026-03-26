"""全局配置常量"""

# 后端 API 地址
API_BASE_URL = "http://localhost:8000"

# 页面路由名称
PAGE_HOME = "🏠 首页"
PAGE_CATALOG = "🐱 猫猫图鉴"
PAGE_DETAIL = "📖 猫猫详情"
PAGE_FEEDING = "🍚 喂猫打卡"
PAGE_LOST = "🔍 寻猫启事"
PAGE_ADOPTION = "🏠 领养中心"
PAGE_RESCUE = "🆘 救助求助"
PAGE_COMMENTS = "💬 评论广场"
PAGE_ANNOUNCE = "📢 校园公告"
PAGE_PROFILE = "👤 个人中心"
PAGE_ADMIN = "⚙️ 管理后台"

# 导航菜单（按顺序）
NAV_PAGES = [
    PAGE_HOME,
    PAGE_CATALOG,
    PAGE_FEEDING,
    PAGE_LOST,
    PAGE_ADOPTION,
    PAGE_RESCUE,
    PAGE_COMMENTS,
    PAGE_ANNOUNCE,
    PAGE_PROFILE,
]

# 猫猫状态选项
CAT_STATUS_OPTIONS = ["在校", "走失", "待收养", "已收养", "回喵星"]

# 角色映射
ROLE_LABELS = {
    "admin": "🔑 管理员",
    "certified": "⭐ 认证喂猫人",
    "user": "👤 普通用户",
}
ROLE_LABELS_SHORT = {
    "admin": "管理员",
    "certified": "认证喂猫人",
    "user": "普通用户",
}

# 头像选项
AVATAR_OPTIONS = ["👤", "😺", "😸", "😻", "🧑‍🎓", "👩‍💻", "🐱", "🐾"]

# 猫猫随机 Emoji / 颜色
CAT_EMOJIS = ["😺", "😸", "😻", "😽", "😼", "🐱", "🐈", "🐈‍⬛"]
CAT_COLORS = [
    "#FF8C00", "#E91E63", "#424242", "#90CAF9", "#AB47BC",
    "#607D8B", "#FFB74D", "#FF7043", "#78909C", "#8D6E63",
]

# 事件类型
EVENT_TYPES = ["🔍 发现", "✂️ 绝育", "💉 疫苗", "🏥 受伤", "🏠 收养", "🌈 离世", "🌟 事件"]