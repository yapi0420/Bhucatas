import streamlit as st
import hashlib
import random
from datetime import datetime, timedelta

from sqlalchemy.sql.functions import current_user

# ╔══════════════════════════════════════════╗
# ║    🐱 北华大学猫猫校园 Campus Cat Website   ║
# ╚══════════════════════════════════════════╝

st.set_page_config(
    page_title="🐱 北华大学猫猫校园",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 全局 CSS 样式 — 可爱粉色主题
# ============================================
st.markdown("""
<style>
/* ---------- 整体背景 ---------- */
.stApp {
    background: linear-gradient(160deg, #fff0f5 0%, #fce4ec 30%, #f3e5f5 60%, #e8eaf6 100%);
}

/* ---------- 侧边栏 ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce4ec 0%, #f8bbd0 100%);
    border-right: 3px solid #f48fb1;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c2185b;
}

/* ---------- 卡片容器 ---------- */
.cat-card {
    background: white;
    border-radius: 20px;
    padding: 24px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(233, 30, 99, 0.10);
    border: 2px solid #fce4ec;
    transition: all 0.3s ease;
    text-align: center;
}
.cat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 30px rgba(233, 30, 99, 0.18);
    border-color: #f48fb1;
}

/* ---------- 猫猫头像区域 ---------- */
.cat-avatar {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 60px;
    margin: 0 auto 12px auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 4px solid white;
}

/* ---------- 状态标签 ---------- */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.82em;
    font-weight: 700;
    margin: 3px;
    letter-spacing: 0.5px;
}
.badge-school   { background: #e8f5e9; color: #2e7d32; }
.badge-lost     { background: #fff3e0; color: #e65100; }
.badge-adopt    { background: #e3f2fd; color: #1565c0; }
.badge-adopted  { background: #f3e5f5; color: #7b1fa2; }
.badge-star     { background: #fce4ec; color: #c62828; }
.badge-male     { background: #e3f2fd; color: #1976d2; }
.badge-female   { background: #fce4ec; color: #d81b60; }
.badge-neutered { background: #e8f5e9; color: #388e3c; }
.badge-vaccine  { background: #e0f7fa; color: #00838f; }

/* ---------- 信息面板 ---------- */
.info-panel {
    background: linear-gradient(135deg, #ffffff, #fff5f7);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    border-left: 5px solid #f48fb1;
    box-shadow: 0 2px 12px rgba(233, 30, 99, 0.06);
}

/* ---------- 统计卡片 ---------- */
.stat-card {
    background: white;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 3px 15px rgba(0,0,0,0.06);
    border: 2px solid #fce4ec;
}
.stat-number {
    font-size: 2.4em;
    font-weight: 800;
    background: linear-gradient(135deg, #ec407a, #ab47bc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stat-label { color: #888; font-size: 0.95em; margin-top: 4px; }

/* ---------- 时间线 ---------- */
.timeline-item {
    background: white;
    border-radius: 12px;
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 4px solid #f48fb1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    display: flex;
    align-items: center;
    gap: 12px;
}
.timeline-date {
    color: #e91e63;
    font-weight: 700;
    font-size: 0.88em;
    white-space: nowrap;
}

/* ---------- 评论卡片 ---------- */
.comment-card {
    background: white;
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
    border: 1px solid #f8bbd0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* ---------- 公告卡片 ---------- */
.announce-card {
    background: linear-gradient(135deg, #fff8e1, #fff3e0);
    border-radius: 14px;
    padding: 18px;
    margin: 8px 0;
    border-left: 5px solid #ffb300;
    box-shadow: 0 2px 10px rgba(255,179,0,0.1);
}

/* ---------- 欢迎横幅 ---------- */
.welcome-banner {
    background: linear-gradient(135deg, #ec407a 0%, #ab47bc 50%, #7c4dff 100%);
    border-radius: 24px;
    padding: 40px;
    color: white;
    text-align: center;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(233, 30, 99, 0.25);
}
.welcome-banner h1 {
    font-size: 2.4em;
    margin: 0;
    text-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.welcome-banner p {
    font-size: 1.15em;
    opacity: 0.92;
    margin-top: 8px;
}

/* ---------- 按钮美化 ---------- */
.stButton > button {
    border-radius: 25px !important;
    padding: 0.4rem 1.6rem !important;
    font-weight: 600 !important;
    border: 2px solid #f48fb1 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: #fce4ec !important;
    border-color: #ec407a !important;
    transform: scale(1.03);
}

/* ---------- 选项卡 ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px 12px 0 0;
    padding: 8px 20px;
    font-weight: 600;
}

/* ---------- 隐藏默认的 Streamlit 元素 ---------- */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ---------- 关系图谱节点 ---------- */
.relation-node {
    display: inline-block;
    background: white;
    border: 3px solid #f48fb1;
    border-radius: 50%;
    width: 80px;
    height: 80px;
    line-height: 80px;
    text-align: center;
    font-size: 36px;
    margin: 5px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}
.relation-line {
    display: inline-block;
    color: #e91e63;
    font-size: 0.9em;
    vertical-align: middle;
    margin: 0 8px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ============================================
# 📦 数据初始化
# ============================================
def init_data():
    if 'init' in st.session_state:
        return
    st.session_state.init = True
    st.session_state.logged_in_user = None
    st.session_state.page = "🏠 首页"
    st.session_state.detail_cat = None

    # ---------- 用户数据 ----------
    st.session_state.users = {
        "admin": {"pwd": hashlib.sha256(b"admin123").hexdigest(), "role": "admin",
                  "nick": "超级管理员🐾", "favs": [], "avatar": "👩‍💻", "reg": "2024-01-01"},
        "catfan": {"pwd": hashlib.sha256(b"cat123").hexdigest(), "role": "certified",
                   "nick": "北华喂猫第一人", "favs": [1, 3, 5], "avatar": "😻", "reg": "2024-02-14"},
        "demo": {"pwd": hashlib.sha256(b"demo123").hexdigest(), "role": "user",
                 "nick": "路过的同学", "favs": [2], "avatar": "🧑‍🎓", "reg": "2024-09-01"},
    }

    # ---------- 猫猫数据 ----------
    st.session_state.cats = [
        {"id":1,"name":"橘座","emoji":"😺","color":"#FF8C00",
         "gender":"♂ 公","age":"3岁","breed":"中华田园猫","fur":"橘色虎斑",
         "neutered":True,"status":"在校","area":"一食堂门口",
         "personality":["友善亲人","贪吃","爱撒娇"],
         "vaccine":True,"deworm":True,
         "desc":"北华第一网红猫，十橘九胖的典范代表。每天准时蹲守食堂门口等投喂。",
         "events":[
             {"d":"2022-03-15","t":"🔍 发现","s":"在一食堂附近首次被发现"},
             {"d":"2022-04-20","t":"✂️ 绝育","s":"完成绝育手术，恢复良好"},
             {"d":"2022-05-10","t":"💉 疫苗","s":"完成三联疫苗接种"},
             {"d":"2023-09-01","t":"⭐ 封号","s":"荣获北华第一网红猫称号"},
         ],
         "rels":[{"cid":8,"cn":"小橘","r":"父子(疑似)"},{"cid":4,"cn":"大白","r":"好朋友"}]},

        {"id":2,"name":"花花","emoji":"😽","color":"#E91E63",
         "gender":"♀ 母","age":"2岁","breed":"中华田园猫","fur":"三花色",
         "neutered":True,"status":"在校","area":"图书馆花园",
         "personality":["害羞","安静","偶尔高冷"],
         "vaccine":True,"deworm":True,
         "desc":"图书馆旁的安静女孩，喜欢趴在花坛边晒太阳。不太亲人，但熟悉后会蹭腿。",
         "events":[
             {"d":"2023-01-10","t":"🔍 发现","s":"在图书馆花园被同学发现"},
             {"d":"2023-03-08","t":"✂️ 绝育","s":"完成绝育手术"},
             {"d":"2023-03-20","t":"💉 疫苗","s":"接种疫苗"},
         ],
         "rels":[{"cid":5,"cn":"三花姐","r":"好闺蜜"}]},

        {"id":3,"name":"小黑","emoji":"🐈‍⬛","color":"#424242",
         "gender":"♂ 公","age":"4岁","breed":"中华田园猫","fur":"纯黑色",
         "neutered":True,"status":"在校","area":"工学院楼下",
         "personality":["独立","高冷","夜行侠"],
         "vaccine":True,"deworm":True,
         "desc":"神出鬼没的校园保安猫，深夜巡逻主力。白天基本找不到踪影。",
         "events":[
             {"d":"2021-09-01","t":"🔍 发现","s":"开学季出现在工学院"},
             {"d":"2021-11-15","t":"✂️ 绝育","s":"志愿者诱捕后完成绝育"},
             {"d":"2021-12-01","t":"💉 疫苗","s":"接种疫苗及驱虫"},
         ],
         "rels":[{"cid":6,"cn":"奶牛","r":"冤家"}]},

        {"id":4,"name":"大白","emoji":"😸","color":"#90CAF9",
         "gender":"♂ 公","age":"1岁","breed":"中华田园猫","fur":"纯白色",
         "neutered":False,"status":"待收养","area":"南门小花园",
         "personality":["粘人","活泼","话唠"],
         "vaccine":True,"deworm":False,
         "desc":"超级粘人的小可爱，见人就翻肚皮求摸。正在等待一个温暖的家。",
         "events":[
             {"d":"2024-05-20","t":"🔍 发现","s":"在南门小花园发现，疑似被遗弃"},
             {"d":"2024-06-01","t":"💉 疫苗","s":"完成首次疫苗接种"},
             {"d":"2024-06-15","t":"📋 待收养","s":"身体健康，开放领养申请"},
         ],
         "rels":[{"cid":1,"cn":"橘座","r":"好朋友"},{"cid":7,"cn":"布丁","r":"玩伴"}]},

        {"id":5,"name":"三花姐","emoji":"😻","color":"#AB47BC",
         "gender":"♀ 母","age":"5岁","breed":"中华田园猫","fur":"三花色",
         "neutered":True,"status":"在校","area":"二食堂后门",
         "personality":["温柔","大姐大","母性强"],
         "vaccine":True,"deworm":True,
         "desc":"校园猫中的大姐大，其他猫咪都让她三分。经常护着新来的小猫。",
         "events":[
             {"d":"2020-09-01","t":"🔍 发现","s":"入学时就已经在学校了"},
             {"d":"2020-10-15","t":"✂️ 绝育","s":"完成绝育"},
             {"d":"2021-04-01","t":"🍼 哺育","s":"收养照顾了一窝被遗弃的小奶猫"},
         ],
         "rels":[{"cid":2,"cn":"花花","r":"好闺蜜"},{"cid":9,"cn":"灰灰","r":"老伙计"}]},

        {"id":6,"name":"奶牛","emoji":"🐱","color":"#607D8B",
         "gender":"♂ 公","age":"2岁","breed":"中华田园猫","fur":"黑白奶牛色",
         "neutered":True,"status":"在校","area":"操场看台",
         "personality":["调皮","爱打架","运动健将"],
         "vaccine":True,"deworm":True,
         "desc":"操场上的运动健将，最爱追蝴蝶和树叶。和小黑是欢喜冤家。",
         "events":[
             {"d":"2023-04-01","t":"🔍 发现","s":"操场看台下发现"},
             {"d":"2023-05-20","t":"✂️ 绝育","s":"完成绝育"},
             {"d":"2023-06-01","t":"💉 疫苗","s":"接种疫苗"},
             {"d":"2024-01-15","t":"🏥 受伤","s":"和流浪狗冲突受伤，已救治康复"},
         ],
         "rels":[{"cid":3,"cn":"小黑","r":"冤家"},{"cid":8,"cn":"小橘","r":"玩伴"}]},

        {"id":7,"name":"布丁","emoji":"😺","color":"#FFB74D",
         "gender":"♀ 母","age":"1岁","breed":"中华田园猫","fur":"奶油色",
         "neutered":False,"status":"在校","area":"宿舍区花坛",
         "personality":["好奇","胆小","吃货"],
         "vaccine":True,"deworm":True,
         "desc":"奶油色的小甜心，对什么都充满好奇但又胆小。听到响声就跑。",
         "events":[
             {"d":"2024-03-01","t":"🔍 发现","s":"宿舍区花坛附近出现"},
             {"d":"2024-04-15","t":"💉 疫苗","s":"完成疫苗接种"},
         ],
         "rels":[{"cid":4,"cn":"大白","r":"玩伴"}]},

        {"id":8,"name":"小橘","emoji":"😸","color":"#FF7043",
         "gender":"♂ 公","age":"6个月","breed":"中华田园猫","fur":"浅橘色",
         "neutered":False,"status":"在校","area":"一食堂门口",
         "personality":["活泼","疯跑","精力旺盛"],
         "vaccine":True,"deworm":True,
         "desc":"疑似橘座的崽子，继承了老爸的饭量但还没继承体重。整天疯跑。",
         "events":[
             {"d":"2024-06-01","t":"🔍 发现","s":"在一食堂附近被发现，疑似橘座后代"},
             {"d":"2024-07-15","t":"💉 疫苗","s":"完成首次疫苗"},
         ],
         "rels":[{"cid":1,"cn":"橘座","r":"父子(疑似)"},{"cid":6,"cn":"奶牛","r":"玩伴"}]},

        {"id":9,"name":"灰灰","emoji":"😿","color":"#78909C",
         "gender":"♀ 母","age":"6岁","breed":"中华田园猫","fur":"蓝灰色",
         "neutered":True,"status":"已收养","area":"原: 行政楼前",
         "personality":["沉稳","温顺","佛系"],
         "vaccine":True,"deworm":True,
         "desc":"校园最年长的喵之一，已被教职工家属收养。偶尔回学校探亲。",
         "events":[
             {"d":"2019-09-01","t":"🔍 发现","s":"入校新生时就已在校"},
             {"d":"2019-12-01","t":"✂️ 绝育","s":"完成绝育"},
             {"d":"2024-09-01","t":"🏠 收养","s":"被李老师家属正式收养"},
         ],
         "rels":[{"cid":5,"cn":"三花姐","r":"老伙计"}]},

        {"id":10,"name":"虎斑","emoji":"😼","color":"#8D6E63",
         "gender":"♂ 公","age":"3岁","breed":"中华田园猫","fur":"棕色虎斑",
         "neutered":True,"status":"回喵星","area":"原: 体育馆",
         "personality":["勇敢","亲人","领地意识强"],
         "vaccine":True,"deworm":True,
         "desc":"曾经的体育馆霸主，2024年初因病离世。永远怀念。🌈",
         "events":[
             {"d":"2022-03-01","t":"🔍 发现","s":"体育馆旁被发现"},
             {"d":"2022-04-15","t":"✂️ 绝育","s":"完成绝育"},
             {"d":"2024-02-20","t":"🏥 生病","s":"确诊猫传腹"},
             {"d":"2024-03-10","t":"🌈 离世","s":"治疗无效，回了喵星"},
         ],
         "rels":[]},
    ]

    # ---------- 评论 ----------
    st.session_state.comments = [
        {"id":1,"user":"catfan","cat_id":1,"text":"橘座今天又胖了！太可爱啦～","time":"2024-12-01 10:30","likes":12,"replies":[
            {"user":"demo","text":"哈哈是的！我刚喂了它小鱼干","time":"2024-12-01 11:00"}
        ]},
        {"id":2,"user":"demo","cat_id":2,"text":"花花今天终于让我摸了一下！幸福😭","time":"2024-12-02 14:20","likes":8,"replies":[]},
        {"id":3,"user":"catfan","cat_id":4,"text":"大白太可爱了，好想带回家…","time":"2024-12-03 09:15","likes":15,"replies":[
            {"user":"admin","text":"可以在领养中心提交申请哦～","time":"2024-12-03 10:00"}
        ]},
        {"id":4,"user":"catfan","cat_id":1,"text":"今天橘座在食堂门口翻肚皮晒太阳🌞","time":"2024-12-05 15:00","likes":20,"replies":[]},
    ]

    # ---------- 投喂记录 ----------
    st.session_state.feedings = [
        {"user":"catfan","cat_id":1,"cat_name":"橘座","time":"2024-12-05 07:30","loc":"一食堂门口","food":"猫粮+小鱼干"},
        {"user":"catfan","cat_id":2,"cat_name":"花花","time":"2024-12-05 07:45","loc":"图书馆花园","food":"猫粮"},
        {"user":"demo","cat_id":1,"cat_name":"橘座","time":"2024-12-04 17:00","loc":"一食堂门口","food":"猫罐头"},
        {"user":"catfan","cat_id":4,"cat_name":"大白","time":"2024-12-04 12:30","loc":"南门小花园","food":"猫粮+鸡胸肉"},
        {"user":"catfan","cat_id":6,"cat_name":"奶牛","time":"2024-12-03 08:00","loc":"操场看台","food":"猫粮"},
    ]

    # ---------- 寻猫启事 ----------
    st.session_state.lost = [
        {"id":1,"cat_name":"橘座（误报）","desc":"两天没在食堂看到橘座了！求信息！",
         "user":"demo","time":"2024-11-20","loc":"一食堂","found":True,
         "found_note":"橘座只是换了个地方睡觉…在二食堂后面找到了😅"},
    ]

    # ---------- 领养申请 ----------
    st.session_state.adoptions = [
        {"id":1,"user":"demo","cat_id":4,"cat_name":"大白","time":"2024-12-01",
         "reason":"家里有养猫经验，已准备好猫砂猫粮等用品。住在校外，有稳定住所。",
         "status":"审核中","contact":"138****1234"},
    ]

    # ---------- 救助求助 ----------
    st.session_state.rescues = [
        {"id":1,"user":"catfan","time":"2024-11-15","loc":"东门外马路边",
         "desc":"发现一只受伤的流浪猫，右前腿疑似骨折，需要紧急救助！",
         "status":"已处理","note":"已送往宠物医院治疗，费用由爱心基金承担"},
    ]

    # ---------- 校园公告 ----------
    st.session_state.announcements = [
        {"id":1,"title":"🎄 冬季投喂指南","content":"冬季来临，请大家在投喂点增加温水供应，猫粮建议选择高热量款。投喂时间建议在早7点和晚5点。",
         "time":"2024-12-01","author":"admin"},
        {"id":2,"title":"📢 第三届校园猫猫摄影大赛","content":"用镜头记录北华喵星人的可爱瞬间！投稿截止12月31日，优秀作品将在图书馆展出！奖品丰厚～",
         "time":"2024-11-25","author":"admin"},
        {"id":3,"title":"💉 秋季疫苗驱虫通知","content":"本学期秋季集中疫苗驱虫工作已完成，共为8只在校猫咪完成疫苗接种和体内外驱虫。",
         "time":"2024-10-15","author":"admin"},
    ]

    # ---------- 领养回访 ----------
    st.session_state.followups = [
        {"cat_id":9,"cat_name":"灰灰","user":"李老师家属","time":"2024-11-01",
         "content":"灰灰在家适应得很好，每天吃得饱饱的，已经长胖了一斤！特别喜欢趴在窗台晒太阳。",
         "status":"良好"},
    ]


# ============================================
# 🔧 工具函数
# ============================================
def get_user():
    return st.session_state.get("logged_in_user")

def get_user_info():
    u = get_user()
    if u and u in st.session_state.users:
        return st.session_state.users[u]
    return None

def is_admin()->bool:
    # u=current_user()
    # return u and u.get("role") =="admin"
    info = get_user_info()
    return info and info["role"] == "admin"

def get_cat(cid):
    for c in st.session_state.cats:
        if c["id"] == cid:
            return c
    return None

def status_badge(s):
    m = {"在校":"school","走失":"lost","待收养":"adopt","已收养":"adopted","回喵星":"star"}
    cls = m.get(s, "school")
    return f'<span class="badge badge-{cls}">{s}</span>'

def render_cat_card(cat, show_button=True):
    """渲染猫猫卡片 HTML"""
    badges = status_badge(cat["status"])
    if cat["neutered"]:
        badges += ' <span class="badge badge-neutered">✅ 已绝育</span>'
    gender_cls = "male" if "公" in cat["gender"] else "female"
    badges = f'<span class="badge badge-{gender_cls}">{cat["gender"]}</span> ' + badges

    html = f"""
    <div class="cat-card">
        <div class="cat-avatar" style="background: linear-gradient(135deg, {cat['color']}33, {cat['color']}66);">
            {cat['emoji']}
        </div>
        <h3 style="margin:8px 0 4px;color:#333;">{cat['name']}</h3>
        <p style="color:#999;font-size:0.9em;margin:2px 0;">{cat['breed']} · {cat['age']}</p>
        <div style="margin:8px 0;">{badges}</div>
        <p style="color:#666;font-size:0.88em;">📍 {cat['area']}</p>
        <p style="color:#888;font-size:0.85em;margin-top:6px;">{'、'.join(cat['personality'])}</p>
    </div>
    """
    return html


# ============================================
# 📄 页面：首页
# ============================================
def page_home():
    st.markdown("""
    <div class="welcome-banner">
        <h1>🐾 欢迎来到北华大学猫猫校园 🐾</h1>
        <p>记录每一只校园喵星人的故事 · 用爱守护流浪的它们</p>
        <p style="font-size:0.9em;opacity:0.8;margin-top:12px;">
            🐱 喵星人档案 · 🍚 喂猫打卡 · 🔍 寻猫启事 · 🏠 领养中心 · 🆘 救助求助
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 统计数据
    cats = st.session_state.cats
    on_campus = len([c for c in cats if c["status"]=="在校"])
    adopted = len([c for c in cats if c["status"]=="已收养"])
    total_feed = len(st.session_state.feedings)
    total_users = len(st.session_state.users)

    cols = st.columns(4)
    stats = [
        ("🐱",str(len(cats)),"猫猫总数"),
        ("🏫",str(on_campus),"在校猫咪"),
        ("🍚",str(total_feed),"投喂总次数"),
        ("👥",str(total_users),"注册用户"),
    ]
    for col, (icon,num,label) in zip(cols, stats):
        col.markdown(f"""
        <div class="stat-card">
            <div style="font-size:2em;">{icon}</div>
            <div class="stat-number">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 随机推荐在校猫猫
    st.markdown("### ✨ 今日推荐猫猫")
    campus_cats = [c for c in cats if c["status"]=="在校"]
    if campus_cats:
        show_cats = random.sample(campus_cats, min(4, len(campus_cats)))
        cols = st.columns(len(show_cats))
        for col, cat in zip(cols, show_cats):
            with col:
                st.markdown(render_cat_card(cat), unsafe_allow_html=True)
                if st.button(f"查看 {cat['name']} 详情", key=f"home_{cat['id']}", use_container_width=True):
                    st.session_state.detail_cat = cat["id"]
                    st.session_state.page = "📖 猫猫详情"
                    st.rerun()

    st.markdown("---")

    # 最新公告
    st.markdown("### 📢 最新公告")
    for a in st.session_state.announcements[:2]:
        st.markdown(f"""
        <div class="announce-card">
            <h4 style="margin:0 0 6px;">{a['title']}</h4>
            <p style="color:#666;margin:0;font-size:0.92em;">{a['content'][:100]}...</p>
            <p style="color:#bbb;font-size:0.82em;margin-top:6px;">📅 {a['time']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 最新投喂
    st.markdown("### 🍚 最近投喂动态")
    for f in st.session_state.feedings[:3]:
        st.markdown(f"""
        <div class="timeline-item">
            <span class="timeline-date">🕐 {f['time']}</span>
            <span>👤 {f['user']} 在 📍{f['loc']} 投喂了 🐱<b>{f['cat_name']}</b> ({f['food']})</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 📄 页面：猫猫图鉴
# ============================================
def page_catalog():
    st.markdown("## 🐱 猫猫图鉴")
    st.markdown("> 北华大学全部喵星人档案，点击查看详细信息")

    cats = st.session_state.cats

    # 搜索筛选
    with st.expander("🔍 搜索与筛选", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        search_name = c1.text_input("🔎 搜索名字", "")
        filter_gender = c2.selectbox("性别", ["全部","♂ 公","♀ 母"])
        filter_status = c3.selectbox("状态", ["全部","在校","走失","待收养","已收养","回喵星"])
        filter_neutered = c4.selectbox("绝育状态", ["全部","已绝育","未绝育"])

    filtered = cats.copy()
    if search_name:
        filtered = [c for c in filtered if search_name.lower() in c["name"].lower()]
    if filter_gender != "全部":
        filtered = [c for c in filtered if c["gender"] == filter_gender]
    if filter_status != "全部":
        filtered = [c for c in filtered if c["status"] == filter_status]
    if filter_neutered != "全部":
        n = filter_neutered == "已绝育"
        filtered = [c for c in filtered if c["neutered"] == n]

    st.markdown(f"共找到 **{len(filtered)}** 只猫猫 🐾")

    # 显示网格
    if filtered:
        rows = [filtered[i:i+4] for i in range(0, len(filtered), 4)]
        for row in rows:
            cols = st.columns(4)
            for i, cat in enumerate(row):
                with cols[i]:
                    st.markdown(render_cat_card(cat), unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("📖 详情", key=f"cat_{cat['id']}", use_container_width=True):
                            st.session_state.detail_cat = cat["id"]
                            st.session_state.page = "📖 猫猫详情"
                            st.rerun()
                    with c2:
                        user = get_user()
                        if user:
                            favs = st.session_state.users[user]["favs"]
                            if cat["id"] in favs:
                                if st.button("💔 取消", key=f"unfav_{cat['id']}", use_container_width=True):
                                    favs.remove(cat["id"])
                                    st.rerun()
                            else:
                                if st.button("❤️ 收藏", key=f"fav_{cat['id']}", use_container_width=True):
                                    favs.append(cat["id"])
                                    st.toast(f"已收藏 {cat['name']} ❤️")
                                    st.rerun()
                        else:
                            st.button("❤️ 收藏", key=f"fav_no_{cat['id']}", disabled=True, use_container_width=True, help="请先登录")
    else:
        st.info("没有找到匹配的猫猫 😿")


# ============================================
# 📄 页面：猫猫详情
# ============================================
def page_detail():
    cid = st.session_state.get("detail_cat")
    if not cid:
        st.warning("请从猫猫图鉴选择一只猫猫查看")
        if st.button("← 返回图鉴"):
            st.session_state.page = "🐱 猫猫图鉴"
            st.rerun()
        return

    cat = get_cat(cid)
    if not cat:
        st.error("猫猫不存在")
        return

    if st.button("← 返回图鉴"):
        st.session_state.page = "🐱 猫猫图鉴"
        st.rerun()

    # 头部信息
    h1, h2 = st.columns([1, 2])
    with h1:
        st.markdown(f"""
        <div style="text-align:center; padding:20px;">
            <div class="cat-avatar" style="background:linear-gradient(135deg,{cat['color']}33,{cat['color']}66);width:160px;height:160px;font-size:80px;line-height:160px;">
                {cat['emoji']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        badges = status_badge(cat["status"])
        g_cls = "male" if "公" in cat["gender"] else "female"
        st.markdown(f"""
        <div style="padding:10px 0;">
            <h1 style="margin:0;color:#333;">{cat['name']} {cat['emoji']}</h1>
            <div style="margin:10px 0;">
                <span class="badge badge-{g_cls}">{cat['gender']}</span>
                {badges}
                {'<span class="badge badge-neutered">✅ 已绝育</span>' if cat['neutered'] else '<span class="badge" style="background:#fff3e0;color:#e65100;">❌ 未绝育</span>'}
                {'<span class="badge badge-vaccine">💉 已免疫</span>' if cat['vaccine'] else ''}
            </div>
            <p style="color:#666;font-size:1.05em;margin-top:12px;">{cat['desc']}</p>
        </div>
        """, unsafe_allow_html=True)

    # 选项卡
    tabs = st.tabs(["📋 基本信息", "📸 相册", "⏳ 事件时间线", "🔗 关系图谱", "💬 评论", "🍚 投喂记录"])

    # TAB: 基本信息
    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        info_items = [
            ("🎂 年龄", cat["age"]),
            ("🐾 品种", cat["breed"]),
            ("🎨 毛色", cat["fur"]),
            ("📍 常出没", cat["area"]),
            ("✂️ 绝育", "是" if cat["neutered"] else "否"),
            ("💉 疫苗", "已接种" if cat["vaccine"] else "未接种"),
            ("🐛 驱虫", "已驱虫" if cat["deworm"] else "未驱虫"),
            ("💕 性格", "、".join(cat["personality"])),
        ]
        for i, (label, val) in enumerate(info_items):
            col = [c1,c2,c3][i%3]
            col.markdown(f"""
            <div class="info-panel">
                <b style="color:#e91e63;">{label}</b><br/>
                <span style="font-size:1.1em;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    # TAB: 相册
    with tabs[1]:
        st.markdown("#### 📸 猫猫相册")
        st.info("🖼️ 这里将展示猫猫的生活照和成长照片")
        # 模拟相册展示
        pcols = st.columns(4)
        moments = ["😺 晒太阳","😸 吃饭中","😻 被摸头","😽 打哈欠","🙀 被惊吓","😹 玩耍中"]
        for i, m in enumerate(moments[:4]):
            pcols[i].markdown(f"""
            <div style="background:linear-gradient(135deg,{cat['color']}22,{cat['color']}44);
                        border-radius:16px;padding:40px 10px;text-align:center;
                        border:2px dashed {cat['color']}66;margin:5px 0;">
                <span style="font-size:48px;">{cat['emoji']}</span>
                <p style="color:#888;margin-top:8px;">{m}</p>
            </div>
            """, unsafe_allow_html=True)

        user = get_user()
        if user:
            st.markdown("---")
            uploaded = st.file_uploader("📤 上传猫猫照片", type=["jpg","png","jpeg"], accept_multiple_files=True, key=f"upload_{cid}")
            if uploaded:
                st.success(f"已上传 {len(uploaded)} 张照片！")
                for f in uploaded:
                    st.image(f, width=200)

    # TAB: 时间线
    with tabs[2]:
        st.markdown("#### ⏳ 事件时间线")
        if cat["events"]:
            for ev in cat["events"]:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">{ev['d']}</span>
                    <b>{ev['t']}</b>&nbsp;&nbsp;{ev['s']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无记录")

        if is_admin():
            st.markdown("---")
            st.markdown("**➕ 添加新事件**")
            ec1, ec2 = st.columns(2)
            ev_date = ec1.date_input("日期", key=f"ev_d_{cid}")
            ev_type = ec2.selectbox("类型", ["🔍 发现","✂️ 绝育","💉 疫苗","🏥 受伤","🏠 收养","🌈 离世","🌟 事件"], key=f"ev_t_{cid}")
            ev_desc = st.text_input("描述", key=f"ev_s_{cid}")
            if st.button("添加事件", key=f"ev_add_{cid}"):
                if ev_desc:
                    cat["events"].append({"d":str(ev_date),"t":ev_type,"s":ev_desc})
                    st.success("事件已添加！")
                    st.rerun()

    # TAB: 关系图谱
    with tabs[3]:
        st.markdown("#### 🔗 社交关系图谱")
        if cat["rels"]:
            for rel in cat["rels"]:
                rc = get_cat(rel["cid"])
                r_emoji = rc["emoji"] if rc else "🐱"
                st.markdown(f"""
                <div style="text-align:center;margin:15px 0;">
                    <span class="relation-node" style="border-color:{cat['color']}">{cat['emoji']}</span>
                    <span class="relation-line">—— {rel['r']} ——</span>
                    <span class="relation-node">{r_emoji}</span>
                    <br/>
                    <span style="color:#888;font-size:0.9em;">{cat['name']}  ↔  {rel['cn']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("该猫猫暂无已知社交关系记录")

    # TAB: 评论
    with tabs[4]:
        st.markdown("#### 💬 大家的评论")
        cat_comments = [c for c in st.session_state.comments if c["cat_id"]==cid]
        if cat_comments:
            for cmt in cat_comments:
                st.markdown(f"""
                <div class="comment-card">
                    <b>👤 {cmt['user']}</b> <span style="color:#bbb;font-size:0.82em;">· {cmt['time']}</span>
                    <p style="margin:8px 0;">{cmt['text']}</p>
                    <span style="color:#e91e63;cursor:pointer;">❤️ {cmt['likes']}</span>
                </div>
                """, unsafe_allow_html=True)
                # 楼中楼回复
                for rep in cmt.get("replies",[]):
                    st.markdown(f"""
                    <div style="margin-left:30px;background:#fef9ff;border-radius:10px;padding:10px 14px;border-left:3px solid #f48fb1;margin-bottom:5px;">
                        <b>👤 {rep['user']}</b> <span style="color:#bbb;font-size:0.82em;">· {rep['time']}</span>
                        <p style="margin:4px 0;">{rep['text']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # 回复按钮
                user = get_user()
                if user:
                    with st.expander(f"💬 回复此评论", expanded=False):
                        reply_text = st.text_input("回复内容", key=f"reply_{cmt['id']}")
                        if st.button("发送回复", key=f"reply_btn_{cmt['id']}"):
                            if reply_text:
                                cmt["replies"].append({
                                    "user": user,
                                    "text": reply_text,
                                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                                })
                                st.success("回复成功！")
                                st.rerun()
                st.markdown("")
        else:
            st.info("还没有评论，快来抢沙发吧！🐾")

        # 发表评论
        user = get_user()
        if user:
            st.markdown("---")
            st.markdown("**✍️ 发表评论**")
            new_cmt = st.text_area("说点什么吧～", key=f"new_cmt_{cid}", placeholder="这只猫猫也太可爱了吧！")
            if st.button("发布评论 🐾", key=f"post_cmt_{cid}"):
                if new_cmt.strip():
                    st.session_state.comments.append({
                        "id": len(st.session_state.comments)+1,
                        "user": user,
                        "cat_id": cid,
                        "text": new_cmt.strip(),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "likes": 0,
                        "replies": []
                    })
                    st.success("评论发布成功！🎉")
                    st.rerun()
                else:
                    st.warning("评论不能为空哦～")
        else:
            st.info("登录后即可发表评论 💬")

    # TAB: 投喂记录
    with tabs[5]:
        st.markdown("#### 🍚 投喂记录")
        cat_feeds = [f for f in st.session_state.feedings if f["cat_id"]==cid]
        if cat_feeds:
            for fd in cat_feeds:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">🕐 {fd['time']}</span>
                    👤 {fd['user']} · 📍 {fd['loc']} · 🍽️ {fd['food']}
                </div>
                """, unsafe_allow_html=True)
            st.markdown(f"\n📊 累计被投喂 **{len(cat_feeds)}** 次")
        else:
            st.info("暂无投喂记录")


# ============================================
# 📄 页面：喂猫打卡
# ============================================
def page_feeding():
    st.markdown("## 🍚 喂猫打卡")
    st.markdown("> 记录你的每一次投喂，让爱心看得见 💕")

    user = get_user()
    if not user:
        st.warning("请登录后使用打卡功能 🔑")
        return

    tab1, tab2 = st.tabs(["📝 打卡投喂", "📊 投喂统计"])

    with tab1:
        st.markdown("### 🐾 新建投喂打卡")
        c1, c2 = st.columns(2)
        campus_cats = [c for c in st.session_state.cats if c["status"]=="在校"]
        cat_options = {c["name"]: c for c in campus_cats}
        sel_name = c1.selectbox("选择投喂的猫猫 🐱", list(cat_options.keys()))
        loc = c2.text_input("投喂地点 📍", value=cat_options[sel_name]["area"] if sel_name else "")
        food = st.text_input("投喂内容 🍽️", placeholder="如: 猫粮+猫罐头")

        if st.button("✅ 提交打卡", use_container_width=True):
            if sel_name and food:
                sel_cat = cat_options[sel_name]
                st.session_state.feedings.insert(0, {
                    "user": user,
                    "cat_id": sel_cat["id"],
                    "cat_name": sel_cat["name"],
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "loc": loc,
                    "food": food
                })
                st.success(f"打卡成功！感谢你投喂了 {sel_name} 🎉")
                st.balloons()
                st.rerun()
            else:
                st.warning("请填写完整信息")

        st.markdown("---")
        st.markdown("### 📋 最近投喂记录")
        for fd in st.session_state.feedings[:10]:
            st.markdown(f"""
            <div class="timeline-item">
                <span class="timeline-date">🕐 {fd['time']}</span>
                👤 {fd['user']} 在 📍{fd['loc']} 投喂了 🐱<b>{fd['cat_name']}</b> · 🍽️ {fd['food']}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📊 投喂统计")
        # 统计各猫猫投喂次数
        feed_count = {}
        for fd in st.session_state.feedings:
            name = fd["cat_name"]
            feed_count[name] = feed_count.get(name, 0) + 1

        if feed_count:
            import pandas as pd
            df = pd.DataFrame(list(feed_count.items()), columns=["猫猫","投喂次数"])
            df = df.sort_values("投喂次数", ascending=False)
            st.bar_chart(df.set_index("猫猫"))

            st.markdown("**🏆 投喂排行榜**")
            for i, (_, row) in enumerate(df.iterrows()):
                medal = ["🥇","🥈","🥉"][i] if i<3 else f"  {i+1}."
                st.markdown(f"{medal} **{row['猫猫']}** — 被投喂 {row['投喂次数']} 次")

        # 我的投喂统计
        my_feeds = [f for f in st.session_state.feedings if f["user"]==user]
        st.markdown(f"\n---\n### 🙋 我的投喂\n\n你已累计投喂 **{len(my_feeds)}** 次 🎉")


# ============================================
# 📄 页面：寻猫启事
# ============================================
def page_lost():
    st.markdown("## 🔍 寻猫启事")
    st.markdown("> 找不到猫猫？发布寻猫启事，大家一起帮忙找！")

    user = get_user()

    # 发布寻猫
    if user:
        with st.expander("📝 发布寻猫启事", expanded=False):
            l_name = st.text_input("走失猫猫名称/特征", key="lost_name")
            l_loc = st.text_input("最后出现地点", key="lost_loc")
            l_desc = st.text_area("详细描述", key="lost_desc", placeholder="毛色、体型、最后见到的时间...")
            if st.button("发布启事", key="lost_submit"):
                if l_name and l_desc:
                    st.session_state.lost.insert(0, {
                        "id": len(st.session_state.lost)+1,
                        "cat_name": l_name,
                        "desc": l_desc,
                        "user": user,
                        "time": datetime.now().strftime("%Y-%m-%d"),
                        "loc": l_loc,
                        "found": False,
                        "found_note": ""
                    })
                    st.success("寻猫启事发布成功！🐾")
                    st.rerun()

    # 展示列表
    for notice in st.session_state.lost:
        status_text = "✅ 已找回" if notice["found"] else "🔍 寻找中"
        bg = "#e8f5e9" if notice["found"] else "#fff3e0"
        st.markdown(f"""
        <div class="info-panel" style="border-left-color: {'#4caf50' if notice['found'] else '#ff9800'}; background:{bg}22;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <h4 style="margin:0;">🐱 {notice['cat_name']}</h4>
                <span class="badge" style="background:{bg};color:{'#2e7d32' if notice['found'] else '#e65100'};">{status_text}</span>
            </div>
            <p style="margin:8px 0;color:#555;">{notice['desc']}</p>
            <p style="color:#999;font-size:0.85em;">📍 {notice['loc']} · 👤 {notice['user']} · 📅 {notice['time']}</p>
            {'<p style="color:#2e7d32;margin-top:6px;">📌 '+notice["found_note"]+'</p>' if notice['found'] and notice['found_note'] else ''}
        </div>
        """, unsafe_allow_html=True)

        # 标记找回
        if user and not notice["found"] and (user == notice["user"] or is_admin()):
            c1, c2 = st.columns([3,1])
            fn = c1.text_input("找回备注", key=f"fn_{notice['id']}")
            if c2.button("标记已找回", key=f"found_{notice['id']}"):
                notice["found"] = True
                notice["found_note"] = fn
                st.success("已标记为找回！🎉")
                st.rerun()


# ============================================
# 📄 页面：领养中心
# ============================================
def page_adoption():
    st.markdown("## 🏠 领养中心")
    st.markdown("> 给流浪的它们一个温暖的家 💕")

    user = get_user()
    tab1, tab2, tab3 = st.tabs(["🐱 待收养猫咪", "📋 领养申请", "📝 领养回访"])

    # TAB1: 待收养
    with tab1:
        adopt_cats = [c for c in st.session_state.cats if c["status"]=="待收养"]
        if adopt_cats:
            for cat in adopt_cats:
                st.markdown(f"""
                <div class="cat-card" style="text-align:left;">
                    <div style="display:flex;align-items:center;gap:20px;">
                        <div class="cat-avatar" style="background:linear-gradient(135deg,{cat['color']}33,{cat['color']}66);width:100px;height:100px;font-size:50px;line-height:100px;flex-shrink:0;">
                            {cat['emoji']}
                        </div>
                        <div>
                            <h3 style="margin:0;">{cat['name']} <span class="badge badge-adopt">待收养</span></h3>
                            <p style="color:#666;margin:6px 0;">{cat['gender']} · {cat['age']} · {cat['fur']}</p>
                            <p style="color:#888;margin:4px 0;">性格: {'、'.join(cat['personality'])}</p>
                            <p style="color:#555;margin:4px 0;">{cat['desc']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if user:
                    with st.expander(f"📝 申请领养 {cat['name']}"):
                        reason = st.text_area("领养理由", key=f"adopt_r_{cat['id']}",
                                             placeholder="请描述你的养猫经验、居住条件等...")
                        contact = st.text_input("联系方式", key=f"adopt_c_{cat['id']}")
                        if st.button("提交申请", key=f"adopt_s_{cat['id']}"):
                            if reason and contact:
                                st.session_state.adoptions.append({
                                    "id": len(st.session_state.adoptions)+1,
                                    "user": user,
                                    "cat_id": cat["id"],
                                    "cat_name": cat["name"],
                                    "time": datetime.now().strftime("%Y-%m-%d"),
                                    "reason": reason,
                                    "status": "审核中",
                                    "contact": contact
                                })
                                st.success("领养申请已提交，请等待管理员审核 🎉")
                                st.rerun()
                            else:
                                st.warning("请填写完整信息")
        else:
            st.info("目前没有待收养的猫猫 😸 所有猫猫都有归宿啦！")

    # TAB2: 申请记录
    with tab2:
        st.markdown("### 📋 领养申请记录")
        apps = st.session_state.adoptions
        if user:
            my_apps = [a for a in apps if a["user"]==user]
            if my_apps:
                for a in my_apps:
                    s_color = {"审核中":"#ff9800","已通过":"#4caf50","已拒绝":"#f44336"}.get(a["status"],"#999")
                    st.markdown(f"""
                    <div class="info-panel">
                        <h4 style="margin:0;">🐱 {a['cat_name']} <span style="color:{s_color};font-weight:700;">【{a['status']}】</span></h4>
                        <p style="color:#666;">{a['reason'][:80]}...</p>
                        <p style="color:#999;font-size:0.85em;">📅 {a['time']} · 📞 {a['contact']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("你还没有提交过领养申请")

        if is_admin():
            st.markdown("---")
            st.markdown("### 🔑 管理员审核")
            pending = [a for a in apps if a["status"]=="审核中"]
            for a in pending:
                st.markdown(f"""
                <div class="info-panel" style="border-left-color:#ff9800;">
                    <h4>🐱 {a['cat_name']} — 申请人: {a['user']}</h4>
                    <p>{a['reason']}</p>
                    <p style="font-size:0.85em;color:#999;">📞 {a['contact']} · 📅 {a['time']}</p>
                </div>
                """, unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                if bc1.button("✅ 通过", key=f"ap_{a['id']}"):
                    a["status"] = "已通过"
                    # 更新猫猫状态
                    cat = get_cat(a["cat_id"])
                    if cat:
                        cat["status"] = "已收养"
                    st.success("已通过！")
                    st.rerun()
                if bc2.button("❌ 拒绝", key=f"ar_{a['id']}"):
                    a["status"] = "已拒绝"
                    st.rerun()

    # TAB3: 回访
    with tab3:
        st.markdown("### 📝 领养回访记录")
        for fu in st.session_state.followups:
            st.markdown(f"""
            <div class="info-panel" style="border-left-color:#4caf50;">
                <h4 style="margin:0;">🐱 {fu['cat_name']} <span class="badge badge-neutered">{fu['status']}</span></h4>
                <p style="color:#555;">{fu['content']}</p>
                <p style="color:#999;font-size:0.85em;">👤 {fu['user']} · 📅 {fu['time']}</p>
            </div>
            """, unsafe_allow_html=True)

        if user:
            with st.expander("📤 提交回访记录"):
                adopted_cats = [c for c in st.session_state.cats if c["status"]=="已收养"]
                if adopted_cats:
                    fu_cat = st.selectbox("回访猫猫", [c["name"] for c in adopted_cats], key="fu_cat")
                    fu_content = st.text_area("近况反馈", key="fu_content", placeholder="猫猫最近怎么样？")
                    fu_status = st.selectbox("状态", ["良好","一般","需关注"], key="fu_status")
                    if st.button("提交回访", key="fu_submit"):
                        if fu_content:
                            st.session_state.followups.append({
                                "cat_id": next(c["id"] for c in adopted_cats if c["name"]==fu_cat),
                                "cat_name": fu_cat,
                                "user": user,
                                "time": datetime.now().strftime("%Y-%m-%d"),
                                "content": fu_content,
                                "status": fu_status
                            })
                            st.success("回访记录已提交！")
                            st.rerun()
                else:
                    st.info("暂无已收养猫猫")


# ============================================
# 📄 页面：救助求助
# ============================================
def page_rescue():
    st.markdown("## 🆘 救助求助")
    st.markdown("> 发现受伤的猫猫？发布求助信息，让爱心接力！")

    user = get_user()

    if user:
        with st.expander("📝 发布救助信息", expanded=False):
            r_loc = st.text_input("发现地点", key="r_loc")
            r_desc = st.text_area("情况描述", key="r_desc", placeholder="猫猫受伤情况、外观特征等...")
            if st.button("发布求助", key="r_submit"):
                if r_loc and r_desc:
                    st.session_state.rescues.insert(0, {
                        "id": len(st.session_state.rescues)+1,
                        "user": user,
                        "time": datetime.now().strftime("%Y-%m-%d"),
                        "loc": r_loc,
                        "desc": r_desc,
                        "status": "求助中",
                        "note": ""
                    })
                    st.success("求助信息已发布！🆘")
                    st.rerun()

    for r in st.session_state.rescues:
        s_bg = "#e8f5e9" if r["status"]=="已处理" else "#ffebee"
        s_icon = "✅" if r["status"]=="已处理" else "🆘"
        st.markdown(f"""
        <div class="info-panel" style="border-left-color:{'#4caf50' if r['status']=='已处理' else '#f44336'};background:{s_bg}22;">
            <div style="display:flex;justify-content:space-between;">
                <h4 style="margin:0;">{s_icon} 救助求助 #{r['id']}</h4>
                <span class="badge" style="background:{s_bg};color:{'#2e7d32' if r['status']=='已处理' else '#c62828'};">{r['status']}</span>
            </div>
            <p style="margin:8px 0;color:#555;">{r['desc']}</p>
            <p style="color:#999;font-size:0.85em;">📍 {r['loc']} · 👤 {r['user']} · 📅 {r['time']}</p>
            {'<p style="color:#2e7d32;margin-top:4px;">📌 处理结果: '+r['note']+'</p>' if r['note'] else ''}
        </div>
        """, unsafe_allow_html=True)

        if is_admin() and r["status"]!="已处理":
            note = st.text_input("处理备注", key=f"rn_{r['id']}")
            if st.button("标记已处理", key=f"rp_{r['id']}"):
                r["status"] = "已处理"
                r["note"] = note
                st.rerun()


# ============================================
# 📄 页面：校园公告
# ============================================
def page_announcements():
    st.markdown("## 📢 校园公告")
    st.markdown("> 平台通知、喂猫规则与活动公告")

    if is_admin():
        with st.expander("📝 发布新公告", expanded=False):
            a_title = st.text_input("公告标题", key="a_title")
            a_content = st.text_area("公告内容", key="a_content")
            if st.button("发布公告", key="a_submit"):
                if a_title and a_content:
                    st.session_state.announcements.insert(0, {
                        "id": len(st.session_state.announcements)+1,
                        "title": a_title,
                        "content": a_content,
                        "time": datetime.now().strftime("%Y-%m-%d"),
                        "author": get_user()
                    })
                    st.success("公告已发布！📢")
                    st.rerun()

    for a in st.session_state.announcements:
        st.markdown(f"""
        <div class="announce-card">
            <h3 style="margin:0 0 8px;">{a['title']}</h3>
            <p style="color:#555;margin:0;line-height:1.7;">{a['content']}</p>
            <p style="color:#bbb;font-size:0.82em;margin-top:10px;">📅 {a['time']} · ✍️ {a['author']}</p>
        </div>
        """, unsafe_allow_html=True)
        if is_admin():
            if st.button("🗑️ 删除", key=f"del_a_{a['id']}"):
                st.session_state.announcements = [x for x in st.session_state.announcements if x["id"]!=a["id"]]
                st.rerun()


# ============================================
# 📄 页面：个人中心
# ============================================
def page_profile():
    st.markdown("## 👤 个人中心")

    user = get_user()
    if not user:
        st.warning("请先登录 🔑")
        return

    info = st.session_state.users[user]

    # 个人信息卡
    st.markdown(f"""
    <div class="cat-card" style="text-align:left;display:flex;align-items:center;gap:24px;">
        <div style="font-size:64px;">{info.get('avatar','👤')}</div>
        <div>
            <h2 style="margin:0;">{info['nick']}</h2>
            <p style="color:#888;margin:4px 0;">用户名: {user}</p>
            <p style="color:#888;margin:4px 0;">角色: <span class="badge badge-neutered">{
                {'admin':'管理员','certified':'认证喂猫人','user':'普通用户'}.get(info['role'],'用户')
            }</span></p>
            <p style="color:#bbb;font-size:0.85em;">📅 注册时间: {info['reg']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["❤️ 我的收藏", "💬 我的评论", "🍚 我的打卡", "⚙️ 修改信息"])

    # 收藏
    with tab1:
        favs = info.get("favs", [])
        if favs:
            fav_cats = [c for c in st.session_state.cats if c["id"] in favs]
            cols = st.columns(min(4, len(fav_cats)))
            for i, cat in enumerate(fav_cats):
                with cols[i % 4]:
                    st.markdown(render_cat_card(cat, False), unsafe_allow_html=True)
                    if st.button(f"📖 查看", key=f"pf_{cat['id']}", use_container_width=True):
                        st.session_state.detail_cat = cat["id"]
                        st.session_state.page = "📖 猫猫详情"
                        st.rerun()
        else:
            st.info("还没有收藏猫猫，去图鉴里收藏吧 ❤️")

    # 评论
    with tab2:
        my_cmts = [c for c in st.session_state.comments if c["user"]==user]
        if my_cmts:
            for c in my_cmts:
                cat = get_cat(c["cat_id"])
                cat_name = cat["name"] if cat else "未知"
                st.markdown(f"""
                <div class="comment-card">
                    <p style="color:#e91e63;font-weight:700;margin:0;">🐱 {cat_name}</p>
                    <p style="margin:6px 0;">{c['text']}</p>
                    <p style="color:#bbb;font-size:0.82em;">📅 {c['time']} · ❤️ {c['likes']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ 删除评论", key=f"del_cmt_{c['id']}"):
                    st.session_state.comments = [x for x in st.session_state.comments if x["id"]!=c["id"]]
                    st.rerun()
        else:
            st.info("还没有发表过评论")

    # 打卡
    with tab3:
        my_feeds = [f for f in st.session_state.feedings if f["user"]==user]
        if my_feeds:
            st.markdown(f"📊 累计投喂 **{len(my_feeds)}** 次")
            for f in my_feeds:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">{f['time']}</span>
                    🐱 {f['cat_name']} · 📍 {f['loc']} · 🍽️ {f['food']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("还没有投喂记录，去喂猫打卡吧 🍚")

    # 修改信息
    with tab4:
        new_nick = st.text_input("昵称", value=info["nick"], key="edit_nick")
        new_avatar = st.selectbox("头像", ["👤","😺","😸","😻","🧑‍🎓","👩‍💻","🐱","🐾"],
                                   index=["👤","😺","😸","😻","🧑‍🎓","👩‍💻","🐱","🐾"].index(info.get("avatar","👤")),
                                   key="edit_avatar")
        st.markdown("---")
        st.markdown("**修改密码**")
        old_pwd = st.text_input("当前密码", type="password", key="old_pwd")
        new_pwd = st.text_input("新密码", type="password", key="new_pwd")
        new_pwd2 = st.text_input("确认新密码", type="password", key="new_pwd2")

        if st.button("💾 保存修改", use_container_width=True):
            info["nick"] = new_nick
            info["avatar"] = new_avatar
            if old_pwd and new_pwd:
                if hashlib.sha256(old_pwd.encode()).hexdigest() == info["pwd"]:
                    if new_pwd == new_pwd2:
                        info["pwd"] = hashlib.sha256(new_pwd.encode()).hexdigest()
                        st.success("密码修改成功！")
                    else:
                        st.error("两次密码不一致")
                else:
                    st.error("当前密码错误")
            else:
                st.success("信息已更新！")
            st.rerun()


# ============================================
# 📄 页面：管理后台
# ============================================
def page_admin():
    st.markdown("## ⚙️ 管理后台")

    if not is_admin():
        st.error("🚫 无权限访问")
        return

    tab1, tab2, tab3, tab4 = st.tabs(["📊 数据统计", "👥 用户管理", "🐱 猫猫管理", "🛡️ 内容管理"])

    # TAB: 数据统计
    with tab1:
        st.markdown("### 📊 平台数据概览")
        cats = st.session_state.cats
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🐱 猫猫总数", len(cats))
        c2.metric("🏫 在校猫咪", len([c for c in cats if c["status"]=="在校"]))
        c3.metric("🏠 已收养", len([c for c in cats if c["status"]=="已收养"]))
        c4.metric("🌈 回喵星", len([c for c in cats if c["status"]=="回喵星"]))

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("👥 用户总数", len(st.session_state.users))
        c6.metric("🍚 投喂总量", len(st.session_state.feedings))
        c7.metric("💬 评论总数", len(st.session_state.comments))
        c8.metric("📋 领养申请", len(st.session_state.adoptions))

        st.markdown("---")
        st.markdown("### 🐱 猫猫状态分布")
        import pandas as pd
        status_count = {}
        for c in cats:
            status_count[c["status"]] = status_count.get(c["status"], 0) + 1
        if status_count:
            df = pd.DataFrame(list(status_count.items()), columns=["状态","数量"])
            st.bar_chart(df.set_index("状态"))

        st.markdown("### 📦 数据备份")
        if st.button("📥 导出数据备份"):
            import json
            backup = {
                "cats": st.session_state.cats,
                "users": {k:{kk:vv for kk,vv in v.items() if kk!="pwd"} for k,v in st.session_state.users.items()},
                "comments": st.session_state.comments,
                "feedings": st.session_state.feedings,
                "announcements": st.session_state.announcements,
            }
            st.download_button("💾 下载JSON备份", json.dumps(backup, ensure_ascii=False, indent=2),
                             "backup.json", "application/json")

    # TAB: 用户管理
    with tab2:
        st.markdown("### 👥 用户管理")
        for uname, uinfo in st.session_state.users.items():
            c1, c2, c3, c4 = st.columns([2,2,2,1])
            c1.markdown(f"**{uinfo.get('avatar','👤')} {uname}**")
            c2.markdown(f"{uinfo['nick']}")
            role_options = ["user","certified","admin"]
            new_role = c3.selectbox("角色", role_options,
                                     index=role_options.index(uinfo["role"]),
                                     key=f"role_{uname}")
            if c4.button("保存", key=f"save_role_{uname}"):
                uinfo["role"] = new_role
                st.success(f"{uname} 角色已更新为 {new_role}")
                st.rerun()

    # TAB: 猫猫管理
    with tab3:
        st.markdown("### 🐱 猫猫信息管理")

        # 新增猫猫
        with st.expander("➕ 新增猫猫"):
            nc1, nc2, nc3 = st.columns(3)
            new_name = nc1.text_input("名称", key="new_cat_name")
            new_gender = nc2.selectbox("性别", ["♂ 公","♀ 母"], key="new_cat_gender")
            new_age = nc3.text_input("年龄", key="new_cat_age", placeholder="如: 2岁")
            nc4, nc5, nc6 = st.columns(3)
            new_fur = nc4.text_input("毛色", key="new_cat_fur")
            new_area = nc5.text_input("常出没区域", key="new_cat_area")
            new_status = nc6.selectbox("状态", ["在校","走失","待收养","已收养","回喵星"], key="new_cat_status")
            new_desc = st.text_area("简介", key="new_cat_desc")
            new_personality = st.text_input("性格标签(逗号分隔)", key="new_cat_pers")

            if st.button("✅ 添加猫猫", key="add_cat"):
                if new_name:
                    emojis = ["😺","😸","😻","😽","😼","🐱","🐈","🐈‍⬛"]
                    colors = ["#FF8C00","#E91E63","#424242","#90CAF9","#AB47BC","#607D8B","#FFB74D","#FF7043","#78909C","#8D6E63"]
                    new_cat = {
                        "id": max(c["id"] for c in st.session_state.cats)+1,
                        "name": new_name,
                        "emoji": random.choice(emojis),
                        "color": random.choice(colors),
                        "gender": new_gender,
                        "age": new_age or "未知",
                        "breed": "中华田园猫",
                        "fur": new_fur or "未知",
                        "neutered": False,
                        "status": new_status,
                        "area": new_area or "未知",
                        "personality": [x.strip() for x in new_personality.split(",") if x.strip()] or ["待观察"],
                        "vaccine": False,
                        "deworm": False,
                        "desc": new_desc or "",
                        "events": [{"d":datetime.now().strftime("%Y-%m-%d"),"t":"🔍 发现","s":"新建档案"}],
                        "rels": []
                    }
                    st.session_state.cats.append(new_cat)
                    st.success(f"已添加猫猫: {new_name} 🎉")
                    st.rerun()

        # 编辑现有猫猫
        st.markdown("---")
        for cat in st.session_state.cats:
            with st.expander(f"{cat['emoji']} {cat['name']} ({cat['status']})"):
                ec1, ec2, ec3 = st.columns(3)
                cat["name"] = ec1.text_input("名称", cat["name"], key=f"en_{cat['id']}")
                cat["age"] = ec2.text_input("年龄", cat["age"], key=f"ea_{cat['id']}")
                cat["status"] = ec3.selectbox("状态", ["在校","走失","待收养","已收养","回喵星"],
                    index=["在校","走失","待收养","已收养","回喵星"].index(cat["status"]), key=f"es_{cat['id']}")
                ec4, ec5 = st.columns(2)
                cat["neutered"] = ec4.checkbox("已绝育", cat["neutered"], key=f"en2_{cat['id']}")
                cat["vaccine"] = ec5.checkbox("已免疫", cat["vaccine"], key=f"ev_{cat['id']}")
                cat["area"] = st.text_input("区域", cat["area"], key=f"earea_{cat['id']}")
                cat["desc"] = st.text_area("简介", cat["desc"], key=f"ed_{cat['id']}")
                if st.button("💾 保存修改", key=f"save_cat_{cat['id']}"):
                    st.success(f"{cat['name']} 信息已更新！")

    # TAB: 内容管理
    with tab4:
        st.markdown("### 🛡️ 内容管理")

        st.markdown("**💬 评论管理**")
        for cmt in st.session_state.comments:
            cat = get_cat(cmt["cat_id"])
            cat_name = cat["name"] if cat else "未知"
            c1, c2, c3 = st.columns([4,1,1])
            c1.markdown(f"**{cmt['user']}** → 🐱{cat_name}: {cmt['text'][:50]}...")
            c2.markdown(f"❤️ {cmt['likes']}")
            if c3.button("🗑️", key=f"admin_del_cmt_{cmt['id']}"):
                st.session_state.comments = [x for x in st.session_state.comments if x["id"]!=cmt["id"]]
                st.success("评论已删除")
                st.rerun()

        st.markdown("---")
        st.markdown("**🆘 求助管理**")
        for r in st.session_state.rescues:
            if r["status"] != "已处理":
                st.markdown(f"🆘 #{r['id']} {r['desc'][:40]}... — {r['status']}")


# ============================================
# 🔐 登录/注册
# ============================================
def render_auth():
    """侧边栏登录/注册组件"""
    user = get_user()
    if user:
        info = st.session_state.users[user]
        st.sidebar.markdown(f"""
        <div style="background:white;border-radius:16px;padding:16px;text-align:center;
                    box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:10px;">
            <div style="font-size:40px;">{info.get('avatar','👤')}</div>
            <p style="font-weight:700;margin:6px 0;">{info['nick']}</p>
            <p style="color:#999;font-size:0.82em;">{
                {'admin':'🔑 管理员','certified':'⭐ 认证喂猫人','user':'👤 普通用户'}.get(info['role'],'用户')
            }</p>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("🚪 退出登录", use_container_width=True):
            st.session_state.logged_in_user = None
            st.rerun()
    else:
        st.sidebar.markdown("### 🔐 登录 / 注册")
        auth_mode = st.sidebar.radio("选择操作", ["登录","注册","找回密码"], horizontal=True, label_visibility="collapsed")
        if auth_mode == "登录":
            u = st.sidebar.text_input("用户名", key="login_u")
            p = st.sidebar.text_input("密码", type="password", key="login_p")
            if st.sidebar.button("🐾 登录", use_container_width=True):
                if u in st.session_state.users:
                    if st.session_state.users[u]["pwd"] == hashlib.sha256(p.encode()).hexdigest():
                        st.session_state.logged_in_user = u
                        st.sidebar.success(f"欢迎回来，{st.session_state.users[u]['nick']}！")
                        st.rerun()
                    else:
                        st.sidebar.error("密码错误")
                else:
                    st.sidebar.error("用户不存在")
            st.sidebar.caption("测试账号: admin/admin123 或 demo/demo123")

        elif auth_mode == "注册":
            nu = st.sidebar.text_input("用户名", key="reg_u")
            nn = st.sidebar.text_input("昵称", key="reg_n")
            np1 = st.sidebar.text_input("密码", type="password", key="reg_p1")
            np2 = st.sidebar.text_input("确认密码", type="password", key="reg_p2")
            if st.sidebar.button("📝 注册", use_container_width=True):
                if not nu or not np1:
                    st.sidebar.error("请填写完整信息")
                elif nu in st.session_state.users:
                    st.sidebar.error("用户名已存在")
                elif np1 != np2:
                    st.sidebar.error("两次密码不一致")
                elif len(np1) < 4:
                    st.sidebar.error("密码至少4位")
                else:
                    st.session_state.users[nu] = {
                        "pwd": hashlib.sha256(np1.encode()).hexdigest(),
                        "role": "user",
                        "nick": nn or nu,
                        "favs": [],
                        "avatar": "👤",
                        "reg": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.logged_in_user = nu
                    st.sidebar.success("注册成功！已自动登录 🎉")
                    st.rerun()

        else:  # 找回密码
            st.sidebar.info("请联系管理员重置密码\n📧 catadmin@beihua.edu.cn")
# ============================================
# 📄 页面：评论广场
# ============================================
def page_comments():
    st.markdown("## 💬 评论广场")
    st.markdown("> 所有猫猫的评论汇总，看看大家都在说什么 🐾")

    user = get_user()

    # 按猫猫筛选
    cat_names = ["全部"] + [c["name"] for c in st.session_state.cats]
    sel = st.selectbox("筛选猫猫", cat_names)

    comments = st.session_state.comments
    if sel != "全部":
        cat = next((c for c in st.session_state.cats if c["name"]==sel), None)
        if cat:
            comments = [c for c in comments if c["cat_id"]==cat["id"]]

    if comments:
        for cmt in comments:
            cat = get_cat(cmt["cat_id"])
            cat_name = cat["name"] if cat else "未知"
            cat_emoji = cat["emoji"] if cat else "🐱"

            st.markdown(f"""
            <div class="comment-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span><b>👤 {cmt['user']}</b> → {cat_emoji} <b>{cat_name}</b></span>
                    <span style="color:#bbb;font-size:0.82em;">{cmt['time']}</span>
                </div>
                <p style="margin:10px 0;font-size:1.05em;">{cmt['text']}</p>
                <span style="color:#e91e63;">❤️ {cmt['likes']}</span>
            </div>
            """, unsafe_allow_html=True)

            # 点赞
            bc1, bc2, bc3 = st.columns([1,1,4])
            if user:
                if bc1.button("❤️ 赞", key=f"like_{cmt['id']}"):
                    cmt["likes"] += 1
                    st.rerun()
            if user and (user == cmt["user"] or is_admin()):
                if bc2.button("🗑️ 删除", key=f"del_{cmt['id']}"):
                    st.session_state.comments = [x for x in st.session_state.comments if x["id"]!=cmt["id"]]
                    st.rerun()

            # 回复
            for rep in cmt.get("replies",[]):
                st.markdown(f"""
                <div style="margin-left:30px;background:#fef9ff;border-radius:10px;padding:8px 14px;border-left:3px solid #f48fb1;margin-bottom:4px;">
                    ↪ <b>{rep['user']}</b>: {rep['text']} <span style="color:#bbb;font-size:0.8em;">· {rep['time']}</span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
    else:
        st.info("暂无评论 😺")

    # 举报功能提示
    if user:
        st.markdown("---")
        st.caption("💡 如发现违规内容，请点击评论旁的举报按钮或联系管理员处理。")


# ============================================
# 🧭 主导航
# ============================================
def main():
    init_data()

    # 侧边栏
    st.sidebar.markdown("""
    <div style="text-align:center;padding:10px 0 5px;">
        <h1 style="color:#c2185b;margin:0;font-size:1.6em;">🐾 猫猫校园</h1>
        <p style="color:#e91e63;font-size:0.9em;margin:0;">北华大学校园猫咪平台</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # 登录/用户信息
    render_auth()

    st.sidebar.markdown("---")

    # 导航菜单
    pages = [
        "🏠 首页",
        "🐱 猫猫图鉴",
        "📖 猫猫详情",
        "🍚 喂猫打卡",
        "🔍 寻猫启事",
        "🏠 领养中心",
        "🆘 救助求助",
        "💬 评论广场",
        "📢 校园公告",
        "👤 个人中心",
    ]
    if is_admin():
        pages.append("⚙️ 管理后台")

    # 隐藏"猫猫详情"不在导航中直接显示
    nav_pages = [p for p in pages if p != "📖 猫猫详情"]
    selected = st.sidebar.radio("导航菜单", nav_pages,
                                  index=nav_pages.index(st.session_state.page) if st.session_state.page in nav_pages else 0,
                                  label_visibility="collapsed")


    # 如果不是从详情页过来，更新page
    if st.session_state.page != "📖 猫猫详情":
        st.session_state.page = selected
    elif selected != nav_pages[0]:  # 用户点击了其他导航
        st.session_state.page = selected

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center;padding:10px;color:#c2185b;font-size:0.85em;">
        <p>🐱 用爱守护每一只校园猫咪</p>
        <p style="color:#ddd;">© 2024 北华大学猫猫校园</p>
        <p style="font-size:0.8em;color:#ccc;">Made with ❤️ & Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

    # 路由
    page = st.session_state.page
    if page == "🏠 首页":
        page_home()
    elif page == "🐱 猫猫图鉴":
        page_catalog()
    elif page == "📖 猫猫详情":
        page_detail()
    elif page == "🍚 喂猫打卡":
        page_feeding()
    elif page == "🔍 寻猫启事":
        page_lost()
    elif page == "🏠 领养中心":
        page_adoption()
    elif page == "🆘 救助求助":
        page_rescue()
    elif page == "💬 评论广场":
        page_comments()
    elif page == "📢 校园公告":
        page_announcements()
    elif page == "👤 个人中心":
        page_profile()
    elif page == "⚙️ 管理后台":
        page_admin()
    else:
        page_home()


if __name__ == "__main__":
    main()