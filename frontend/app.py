import streamlit as st
import pandas as pd
import json
from datetime import datetime
from api_client import api

# ╔══════════════════════════════════════════╗
# ║  🐱 北华大学猫猫校园 — 前后端分离版前端     ║
# ╚══════════════════════════════════════════╝

st.set_page_config(
    page_title="🐱 北华大学猫猫校园",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 🎨 全局 CSS 样式
# ============================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #fff0f5 0%, #fce4ec 30%, #f3e5f5 60%, #e8eaf6 100%);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce4ec 0%, #f8bbd0 100%);
    border-right: 3px solid #f48fb1;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c2185b;
}
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
.cat-avatar {
    width: 120px; height: 120px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 60px; margin: 0 auto 12px auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 4px solid white;
}
.badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 0.82em; font-weight: 700; margin: 3px; letter-spacing: 0.5px;
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
.info-panel {
    background: linear-gradient(135deg, #ffffff, #fff5f7);
    border-radius: 16px; padding: 20px; margin: 10px 0;
    border-left: 5px solid #f48fb1;
    box-shadow: 0 2px 12px rgba(233, 30, 99, 0.06);
}
.stat-card {
    background: white; border-radius: 16px; padding: 20px;
    text-align: center; box-shadow: 0 3px 15px rgba(0,0,0,0.06);
    border: 2px solid #fce4ec;
}
.stat-number {
    font-size: 2.4em; font-weight: 800;
    background: linear-gradient(135deg, #ec407a, #ab47bc);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-label { color: #888; font-size: 0.95em; margin-top: 4px; }
.timeline-item {
    background: white; border-radius: 12px; padding: 14px 18px;
    margin: 8px 0; border-left: 4px solid #f48fb1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    display: flex; align-items: center; gap: 12px;
}
.timeline-date { color: #e91e63; font-weight: 700; font-size: 0.88em; white-space: nowrap; }
.comment-card {
    background: white; border-radius: 14px; padding: 16px; margin: 8px 0;
    border: 1px solid #f8bbd0; box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.announce-card {
    background: linear-gradient(135deg, #fff8e1, #fff3e0);
    border-radius: 14px; padding: 18px; margin: 8px 0;
    border-left: 5px solid #ffb300; box-shadow: 0 2px 10px rgba(255,179,0,0.1);
}
.welcome-banner {
    background: linear-gradient(135deg, #ec407a 0%, #ab47bc 50%, #7c4dff 100%);
    border-radius: 24px; padding: 40px; color: white; text-align: center;
    margin-bottom: 24px; box-shadow: 0 8px 32px rgba(233, 30, 99, 0.25);
}
.welcome-banner h1 { font-size: 2.4em; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.15); }
.welcome-banner p  { font-size: 1.15em; opacity: 0.92; margin-top: 8px; }
.stButton > button {
    border-radius: 25px !important; padding: 0.4rem 1.6rem !important;
    font-weight: 600 !important; border: 2px solid #f48fb1 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: #fce4ec !important; border-color: #ec407a !important;
    transform: scale(1.03);
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0; padding: 8px 20px; font-weight: 600; }
#MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
.relation-node {
    display: inline-block; background: white; border: 3px solid #f48fb1;
    border-radius: 50%; width: 80px; height: 80px; line-height: 80px;
    text-align: center; font-size: 36px; margin: 5px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.08);
}
.relation-line {
    display: inline-block; color: #e91e63; font-size: 0.9em;
    vertical-align: middle; margin: 0 8px; font-weight: 700;
}
</style>
""", unsafe_allow_html=True)


# ============================================
# 🔧 工具函数
# ============================================
def is_logged_in() -> bool:
    return st.session_state.get("token") is not None


def current_user() -> dict | None:
    return st.session_state.get("user_info")


def is_admin() -> bool:
    u = current_user()
    return u is not None and u.get("role") == "admin"


def current_user_id() -> int | None:
    u = current_user()
    return u["id"] if u else None


def current_username() -> str:
    u = current_user()
    return u["username"] if u else ""


def status_badge(s: str) -> str:
    m = {"在校": "school", "走失": "lost", "待收养": "adopt", "已收养": "adopted", "回喵星": "star"}
    cls = m.get(s, "school")
    return f'<span class="badge badge-{cls}">{s}</span>'


def render_cat_card_html(cat: dict) -> str:
    badges = status_badge(cat.get("status", "在校"))
    if cat.get("neutered"):
        badges += ' <span class="badge badge-neutered">✅ 已绝育</span>'
    gender = cat.get("gender", "")
    gender_cls = "male" if "公" in gender else "female"
    badges = f'<span class="badge badge-{gender_cls}">{gender}</span> ' + badges
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")
    personality = cat.get("personality", [])
    if isinstance(personality, str):
        personality = [personality]
    return f"""
    <div class="cat-card">
        <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);">
            {emoji}
        </div>
        <h3 style="margin:8px 0 4px;color:#333;">{cat.get('name','')}</h3>
        <p style="color:#999;font-size:0.9em;margin:2px 0;">{cat.get('breed','中华田园猫')} · {cat.get('age','')}</p>
        <div style="margin:8px 0;">{badges}</div>
        <p style="color:#666;font-size:0.88em;">📍 {cat.get('area','')}</p>
        <p style="color:#888;font-size:0.85em;margin-top:6px;">{'、'.join(personality)}</p>
    </div>
    """


def format_time(t) -> str:
    """兼容处理不同格式的时间字符串"""
    if not t:
        return ""
    if isinstance(t, str):
        return t[:16]
    return str(t)[:16]


# ============================================
# 🔐 侧边栏登录 / 注册
# ============================================
def render_auth():
    if is_logged_in():
        u = current_user()
        st.sidebar.markdown(f"""
        <div style="background:white;border-radius:16px;padding:16px;text-align:center;
                    box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:10px;">
            <div style="font-size:40px;">{u.get('avatar','👤')}</div>
            <p style="font-weight:700;margin:6px 0;">{u.get('nickname','')}</p>
            <p style="color:#999;font-size:0.82em;">{
                {'admin':'🔑 管理员','certified':'⭐ 认证喂猫人','user':'👤 普通用户'}.get(u.get('role','user'),'用户')
            }</p>
        </div>
        """, unsafe_allow_html=True)
        if st.sidebar.button("🚪 退出登录", use_container_width=True):
            for key in ["token", "user_info"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.sidebar.markdown("### 🔐 登录 / 注册")
        auth_mode = st.sidebar.radio(
            "选择操作", ["登录", "注册", "找回密码"],
            horizontal=True, label_visibility="collapsed"
        )

        if auth_mode == "登录":
            u = st.sidebar.text_input("用户名", key="login_u")
            p = st.sidebar.text_input("密码", type="password", key="login_p")
            if st.sidebar.button("🐾 登录", use_container_width=True):
                result = api.login(u, p)
                if "error" in result:
                    st.sidebar.error(result["error"])
                else:
                    st.session_state["token"] = result["access_token"]
                    st.session_state["user_info"] = result["user"]
                    st.sidebar.success(f"欢迎回来，{result['user'].get('nickname','')}！")
                    st.rerun()
            st.sidebar.caption("测试: admin/admin123 · demo/demo123")

        elif auth_mode == "注册":
            nu = st.sidebar.text_input("用户名", key="reg_u")
            nn = st.sidebar.text_input("昵称", key="reg_n")
            np1 = st.sidebar.text_input("密码", type="password", key="reg_p1")
            np2 = st.sidebar.text_input("确认密码", type="password", key="reg_p2")
            if st.sidebar.button("📝 注册", use_container_width=True):
                if not nu or not np1:
                    st.sidebar.error("请填写完整信息")
                elif np1 != np2:
                    st.sidebar.error("两次密码不一致")
                elif len(np1) < 4:
                    st.sidebar.error("密码至少4位")
                else:
                    result = api.register(nu, np1, nn)
                    if "error" in result:
                        st.sidebar.error(result["error"])
                    else:
                        st.session_state["token"] = result["access_token"]
                        st.session_state["user_info"] = result["user"]
                        st.sidebar.success("注册成功！已自动登录 🎉")
                        st.rerun()

        else:
            st.sidebar.info("请联系管理员重置密码\n📧 catadmin@beihua.edu.cn")


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
    all_cats = api.list_cats()
    feedings = api.list_feedings(limit=5)
    announcements = api.list_announcements()

    on_campus = len([c for c in all_cats if c.get("status") == "在校"])
    adopted = len([c for c in all_cats if c.get("status") == "已收养"])

    cols = st.columns(4)
    stats = [
        ("🐱", str(len(all_cats)), "猫猫总数"),
        ("🏫", str(on_campus), "在校猫咪"),
        ("🏠", str(adopted), "已收养"),
        ("🍚", str(len(feedings)), "近期投喂"),
    ]
    for col, (icon, num, label) in zip(cols, stats):
        col.markdown(f"""
        <div class="stat-card">
            <div style="font-size:2em;">{icon}</div>
            <div class="stat-number">{num}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 随机推荐猫猫
    st.markdown("### ✨ 今日推荐猫猫")
    random_cats = api.random_cats(4)
    if random_cats:
        rcols = st.columns(len(random_cats))
        for col, cat in zip(rcols, random_cats):
            with col:
                st.markdown(render_cat_card_html(cat), unsafe_allow_html=True)
                if st.button(f"查看 {cat['name']} 详情", key=f"home_{cat['id']}", use_container_width=True):
                    st.session_state.detail_cat = cat["id"]
                    st.session_state.page = "📖 猫猫详情"
                    st.rerun()
    else:
        st.info("暂无在校猫猫数据")

    st.markdown("---")

    # 最新公告
    st.markdown("### 📢 最新公告")
    for a in announcements[:2]:
        st.markdown(f"""
        <div class="announce-card">
            <h4 style="margin:0 0 6px;">{a.get('title','')}</h4>
            <p style="color:#666;margin:0;font-size:0.92em;">{a.get('content','')[:120]}...</p>
            <p style="color:#bbb;font-size:0.82em;margin-top:6px;">📅 {format_time(a.get('created_at',''))}</p>
        </div>
        """, unsafe_allow_html=True)

    # 最新投喂
    st.markdown("### 🍚 最近投喂动态")
    for f in feedings[:5]:
        st.markdown(f"""
        <div class="timeline-item">
            <span class="timeline-date">🕐 {format_time(f.get('created_at',''))}</span>
            <span>👤 {f.get('username','')} 在 📍{f.get('location','')} 投喂了 🐱<b>{f.get('cat_name','')}</b> ({f.get('food','')})</span>
        </div>
        """, unsafe_allow_html=True)


# ============================================
# 📄 页面：猫猫图鉴
# ============================================
def page_catalog():
    st.markdown("## 🐱 猫猫图鉴")
    st.markdown("> 北华大学全部喵星人档案，点击查看详细信息")

    # 搜索筛选
    with st.expander("🔍 搜索与筛选", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        search_name = c1.text_input("🔎 搜索名字", "")
        filter_gender = c2.selectbox("性别", ["全部", "♂ 公", "♀ 母"])
        filter_status = c3.selectbox("状态", ["全部", "在校", "走失", "待收养", "已收养", "回喵星"])
        filter_neutered = c4.selectbox("绝育状态", ["全部", "已绝育", "未绝育"])

    cats = api.list_cats(
        name=search_name if search_name else None,
        gender=filter_gender,
        status=filter_status,
        neutered=filter_neutered
    )

    st.markdown(f"共找到 **{len(cats)}** 只猫猫 🐾")

    if cats:
        rows = [cats[i:i + 4] for i in range(0, len(cats), 4)]
        for row in rows:
            cols = st.columns(4)
            for i, cat in enumerate(row):
                with cols[i]:
                    st.markdown(render_cat_card_html(cat), unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("📖 详情", key=f"cat_{cat['id']}", use_container_width=True):
                            st.session_state.detail_cat = cat["id"]
                            st.session_state.page = "📖 猫猫详情"
                            st.rerun()
                    with bc2:
                        if is_logged_in():
                            is_fav = api.check_favorite(cat["id"])
                            if is_fav:
                                if st.button("💔 取消", key=f"unfav_{cat['id']}", use_container_width=True):
                                    api.remove_favorite(cat["id"])
                                    st.rerun()
                            else:
                                if st.button("❤️ 收藏", key=f"fav_{cat['id']}", use_container_width=True):
                                    api.add_favorite(cat["id"])
                                    st.toast(f"已收藏 {cat['name']} ❤️")
                                    st.rerun()
                        else:
                            st.button("❤️ 收藏", key=f"fav_no_{cat['id']}", disabled=True,
                                      use_container_width=True, help="请先登录")
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

    cat = api.get_cat(cid)
    if not cat:
        st.error("猫猫不存在或无法连接后端")
        if st.button("← 返回图鉴"):
            st.session_state.page = "🐱 猫猫图鉴"
            st.rerun()
        return

    if st.button("← 返回图鉴"):
        st.session_state.page = "🐱 猫猫图鉴"
        st.rerun()

    # 头部信息
    h1, h2 = st.columns([1, 2])
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")
    gender = cat.get("gender", "")
    with h1:
        st.markdown(f"""
        <div style="text-align:center; padding:20px;">
            <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);
                 width:160px;height:160px;font-size:80px;line-height:160px;">
                {emoji}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        badges = status_badge(cat.get("status", ""))
        g_cls = "male" if "公" in gender else "female"
        neutered_badge = '<span class="badge badge-neutered">✅ 已绝育</span>' if cat.get("neutered") else '<span class="badge" style="background:#fff3e0;color:#e65100;">❌ 未绝育</span>'
        vaccine_badge = '<span class="badge badge-vaccine">💉 已免疫</span>' if cat.get("vaccine") else ''
        st.markdown(f"""
        <div style="padding:10px 0;">
            <h1 style="margin:0;color:#333;">{cat.get('name','')} {emoji}</h1>
            <div style="margin:10px 0;">
                <span class="badge badge-{g_cls}">{gender}</span>
                {badges} {neutered_badge} {vaccine_badge}
            </div>
            <p style="color:#666;font-size:1.05em;margin-top:12px;">{cat.get('description','')}</p>
        </div>
        """, unsafe_allow_html=True)

    # 选项卡
    tabs = st.tabs(["📋 基本信息", "📸 相册", "⏳ 事件时间线", "🔗 关系图谱", "💬 评论", "🍚 投喂记录"])

    # ── TAB: 基本信息 ──
    with tabs[0]:
        personality = cat.get("personality", [])
        if isinstance(personality, str):
            personality = [personality]
        info_items = [
            ("🎂 年龄", cat.get("age", "")),
            ("🐾 品种", cat.get("breed", "")),
            ("🎨 毛色", cat.get("fur", "")),
            ("📍 常出没", cat.get("area", "")),
            ("✂️ 绝育", "是" if cat.get("neutered") else "否"),
            ("💉 疫苗", "已接种" if cat.get("vaccine") else "未接种"),
            ("🐛 驱虫", "已驱虫" if cat.get("deworm") else "未驱虫"),
            ("💕 性格", "、".join(personality)),
        ]
        ic1, ic2, ic3 = st.columns(3)
        for idx, (label, val) in enumerate(info_items):
            col = [ic1, ic2, ic3][idx % 3]
            col.markdown(f"""
            <div class="info-panel">
                <b style="color:#e91e63;">{label}</b><br/>
                <span style="font-size:1.1em;">{val}</span>
            </div>
            """, unsafe_allow_html=True)

    # ── TAB: 相册 ──
    with tabs[1]:
        st.markdown("#### 📸 猫猫相册")
        photos = cat.get("photos", [])
        if photos:
            pcols = st.columns(4)
            for idx, photo in enumerate(photos):
                with pcols[idx % 4]:
                    file_path = photo.get("file_path", "")
                    caption = photo.get("caption", "")
                    # 后端会返回 file_path，通过静态文件路由访问
                    from api_client import BASE_URL
                    img_url = f"{BASE_URL}/{file_path}"
                    st.image(img_url, caption=caption, use_container_width=True)
        else:
            pcols = st.columns(4)
            moments = ["😺 晒太阳", "😸 吃饭中", "😻 被摸头", "😽 打哈欠"]
            for idx, m in enumerate(moments):
                pcols[idx].markdown(f"""
                <div style="background:linear-gradient(135deg,{color}22,{color}44);
                            border-radius:16px;padding:40px 10px;text-align:center;
                            border:2px dashed {color}66;margin:5px 0;">
                    <span style="font-size:48px;">{emoji}</span>
                    <p style="color:#888;margin-top:8px;">{m}</p>
                </div>
                """, unsafe_allow_html=True)

        if is_logged_in():
            st.markdown("---")
            uploaded = st.file_uploader("📤 上传猫猫照片", type=["jpg", "png", "jpeg"],
                                        accept_multiple_files=True, key=f"upload_{cid}")
            if uploaded:
                caption = st.text_input("照片说明", key=f"caption_{cid}")
                if st.button("上传", key=f"do_upload_{cid}"):
                    for f in uploaded:
                        result = api.upload_cat_photo(cid, f, caption)
                        if result and "error" not in result:
                            st.success(f"照片 {f.name} 上传成功！")
                        else:
                            st.error(f"上传失败: {result.get('error','未知错误')}")
                    st.rerun()

    # ── TAB: 事件时间线 ──
    with tabs[2]:
        st.markdown("#### ⏳ 事件时间线")
        events = cat.get("events", [])
        if events:
            for ev in events:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">{ev.get('event_date','')}</span>
                    <b>{ev.get('event_type','')}</b>&nbsp;&nbsp;{ev.get('description','')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无记录")

        if is_admin():
            st.markdown("---")
            st.markdown("**➕ 添加新事件**")
            ec1, ec2 = st.columns(2)
            ev_date = ec1.date_input("日期", key=f"ev_d_{cid}")
            ev_type = ec2.selectbox("类型",
                                     ["🔍 发现", "✂️ 绝育", "💉 疫苗", "🏥 受伤", "🏠 收养", "🌈 离世", "🌟 事件"],
                                     key=f"ev_t_{cid}")
            ev_desc = st.text_input("描述", key=f"ev_s_{cid}")
            if st.button("添加事件", key=f"ev_add_{cid}"):
                if ev_desc:
                    result = api.add_cat_event(cid, str(ev_date), ev_type, ev_desc)
                    if result and "error" not in result:
                        st.success("事件已添加！")
                        st.rerun()
                    else:
                        st.error("添加失败")

    # ── TAB: 关系图谱 ──
    with tabs[3]:
        st.markdown("#### 🔗 社交关系图谱")
        relations = cat.get("relations", [])
        if relations:
            for rel in relations:
                # 获取关系猫猫的信息
                rel_cat = api.get_cat(rel.get("related_cat_id"))
                r_emoji = rel_cat.get("emoji", "🐱") if rel_cat else "🐱"
                st.markdown(f"""
                <div style="text-align:center;margin:15px 0;">
                    <span class="relation-node" style="border-color:{color}">{emoji}</span>
                    <span class="relation-line">—— {rel.get('relation_type','')} ——</span>
                    <span class="relation-node">{r_emoji}</span>
                    <br/>
                    <span style="color:#888;font-size:0.9em;">{cat.get('name','')}  ↔  {rel.get('related_cat_name','')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("该猫猫暂无已知社交关系记录")

    # ── TAB: 评论 ──
    with tabs[4]:
        st.markdown("#### 💬 大家的评论")
        comments = api.list_comments(cat_id=cid)
        if comments:
            for cmt in comments:
                st.markdown(f"""
                <div class="comment-card">
                    <b>👤 {cmt.get('username','')}</b>
                    <span style="color:#bbb;font-size:0.82em;">· {format_time(cmt.get('created_at',''))}</span>
                    <p style="margin:8px 0;">{cmt.get('content','')}</p>
                    <span style="color:#e91e63;">❤️ {cmt.get('likes',0)}</span>
                </div>
                """, unsafe_allow_html=True)

                # 楼中楼回复
                for rep in cmt.get("replies", []):
                    st.markdown(f"""
                    <div style="margin-left:30px;background:#fef9ff;border-radius:10px;
                                padding:10px 14px;border-left:3px solid #f48fb1;margin-bottom:5px;">
                        <b>👤 {rep.get('username','')}</b>
                        <span style="color:#bbb;font-size:0.82em;">· {format_time(rep.get('created_at',''))}</span>
                        <p style="margin:4px 0;">{rep.get('content','')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                # 互动按钮
                if is_logged_in():
                    btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 4])
                    with btn_c1:
                        if st.button("❤️ 赞", key=f"like_{cmt['id']}_{cid}"):
                            api.like_comment(cmt["id"])
                            st.rerun()
                    with btn_c2:
                        uname = current_username()
                        if uname == cmt.get("username") or is_admin():
                            if st.button("🗑️", key=f"delc_{cmt['id']}_{cid}"):
                                api.delete_comment(cmt["id"])
                                st.rerun()

                    with st.expander("💬 回复", expanded=False):
                        reply_text = st.text_input("回复内容", key=f"reply_{cmt['id']}_{cid}")
                        if st.button("发送", key=f"reply_btn_{cmt['id']}_{cid}"):
                            if reply_text:
                                result = api.reply_comment(cmt["id"], reply_text)
                                if result and "error" not in result:
                                    st.success("回复成功！")
                                    st.rerun()
                st.markdown("")
        else:
            st.info("还没有评论，快来抢沙发吧！🐾")

        # 发表评论
        if is_logged_in():
            st.markdown("---")
            st.markdown("**✍️ 发表评论**")
            new_cmt = st.text_area("说点什么吧～", key=f"new_cmt_{cid}", placeholder="这只猫猫也太可爱了吧！")
            if st.button("发布评论 🐾", key=f"post_cmt_{cid}"):
                if new_cmt.strip():
                    result = api.create_comment(cid, new_cmt.strip())
                    if result and "error" not in result:
                        st.success("评论发布成功！🎉")
                        st.rerun()
                    else:
                        st.error(f"发布失败: {result.get('error','')}")
                else:
                    st.warning("评论不能为空哦～")
        else:
            st.info("登录后即可发表评论 💬")

    # ── TAB: 投喂记录 ──
    with tabs[5]:
        st.markdown("#### 🍚 投喂记录")
        cat_feeds = api.list_feedings(cat_id=cid)
        if cat_feeds:
            for fd in cat_feeds:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">🕐 {format_time(fd.get('created_at',''))}</span>
                    👤 {fd.get('username','')} · 📍 {fd.get('location','')} · 🍽️ {fd.get('food','')}
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

    if not is_logged_in():
        st.warning("请登录后使用打卡功能 🔑")
        return

    tab1, tab2 = st.tabs(["📝 打卡投喂", "📊 投喂统计"])

    with tab1:
        st.markdown("### 🐾 新建投喂打卡")
        campus_cats = api.list_cats(status="在校")
        if not campus_cats:
            st.info("暂无在校猫猫")
            return

        cat_map = {c["name"]: c for c in campus_cats}
        c1, c2 = st.columns(2)
        sel_name = c1.selectbox("选择投喂的猫猫 🐱", list(cat_map.keys()))
        loc = c2.text_input("投喂地点 📍", value=cat_map[sel_name].get("area", "") if sel_name else "")
        food = st.text_input("投喂内容 🍽️", placeholder="如: 猫粮+猫罐头")

        if st.button("✅ 提交打卡", use_container_width=True):
            if sel_name and food:
                sel_cat = cat_map[sel_name]
                result = api.create_feeding(sel_cat["id"], loc, food)
                if result and "error" not in result:
                    st.success(f"打卡成功！感谢你投喂了 {sel_name} 🎉")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"打卡失败: {result.get('error','')}")
            else:
                st.warning("请填写完整信息")

        st.markdown("---")
        st.markdown("### 📋 最近投喂记录")
        recent_feeds = api.list_feedings(limit=10)
        for fd in recent_feeds:
            st.markdown(f"""
            <div class="timeline-item">
                <span class="timeline-date">🕐 {format_time(fd.get('created_at',''))}</span>
                👤 {fd.get('username','')} 在 📍{fd.get('location','')} 投喂了
                🐱<b>{fd.get('cat_name','')}</b> · 🍽️ {fd.get('food','')}
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📊 投喂统计")
        stats = api.feeding_stats()
        if stats:
            df = pd.DataFrame(stats)
            df.columns = ["猫猫", "投喂次数"]
            df = df.sort_values("投喂次数", ascending=False)
            st.bar_chart(df.set_index("猫猫"))

            st.markdown("**🏆 投喂排行榜**")
            for i, (_, row) in enumerate(df.iterrows()):
                medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"  {i + 1}."
                st.markdown(f"{medal} **{row['猫猫']}** — 被投喂 {int(row['投喂次数'])} 次")

        # 我的投喂
        uid = current_user_id()
        if uid:
            my_feeds = api.list_feedings(user_id=uid)
            st.markdown(f"\n---\n### 🙋 我的投喂\n\n你已累计投喂 **{len(my_feeds)}** 次 🎉")


# ============================================
# 📄 页面：寻猫启事
# ============================================
def page_lost():
    st.markdown("## 🔍 寻猫启事")
    st.markdown("> 找不到猫猫？发布寻猫启事，大家一起帮忙找！")

    # 发布寻猫
    if is_logged_in():
        with st.expander("📝 发布寻猫启事", expanded=False):
            l_name = st.text_input("走失猫猫名称/特征", key="lost_name")
            l_loc = st.text_input("最后出现地点", key="lost_loc")
            l_desc = st.text_area("详细描述", key="lost_desc", placeholder="毛色、体型、最后见到的时间...")
            if st.button("发布启事", key="lost_submit"):
                if l_name and l_desc:
                    result = api.create_lost(l_name, l_desc, l_loc)
                    if result and "error" not in result:
                        st.success("寻猫启事发布成功！🐾")
                        st.rerun()
                    else:
                        st.error("发布失败")

    # 展示列表
    notices = api.list_lost()
    for notice in notices:
        found = notice.get("found", False)
        status_text = "✅ 已找回" if found else "🔍 寻找中"
        bg = "#e8f5e9" if found else "#fff3e0"
        border_color = "#4caf50" if found else "#ff9800"
        text_color = "#2e7d32" if found else "#e65100"
        found_note = notice.get("found_note", "")
        st.markdown(f"""
        <div class="info-panel" style="border-left-color:{border_color};background:{bg}22;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <h4 style="margin:0;">🐱 {notice.get('cat_name','')}</h4>
                <span class="badge" style="background:{bg};color:{text_color};">{status_text}</span>
            </div>
            <p style="margin:8px 0;color:#555;">{notice.get('description','')}</p>
            <p style="color:#999;font-size:0.85em;">📍 {notice.get('location','')} · 👤 {notice.get('username','')} · 📅 {format_time(notice.get('created_at',''))}</p>
            {'<p style="color:#2e7d32;margin-top:6px;">📌 '+found_note+'</p>' if found and found_note else ''}
        </div>
        """, unsafe_allow_html=True)

        # 标记找回
        if is_logged_in() and not found:
            uname = current_username()
            if uname == notice.get("username") or is_admin():
                mc1, mc2 = st.columns([3, 1])
                fn = mc1.text_input("找回备注", key=f"fn_{notice['id']}")
                if mc2.button("标记已找回", key=f"found_{notice['id']}"):
                    result = api.mark_found(notice["id"], fn)
                    if result and "error" not in result:
                        st.success("已标记为找回！🎉")
                        st.rerun()


# ============================================
# 📄 页面：领养中心
# ============================================
def page_adoption():
    st.markdown("## 🏠 领养中心")
    st.markdown("> 给流浪的它们一个温暖的家 💕")

    tab1, tab2, tab3 = st.tabs(["🐱 待收养猫咪", "📋 领养申请", "📝 领养回访"])

    # TAB1: 待收养
    with tab1:
        adopt_cats = api.list_cats(status="待收养")
        if adopt_cats:
            for cat in adopt_cats:
                color = cat.get("color", "#FF8C00")
                emoji = cat.get("emoji", "🐱")
                personality = cat.get("personality", [])
                if isinstance(personality, str):
                    personality = [personality]
                st.markdown(f"""
                <div class="cat-card" style="text-align:left;">
                    <div style="display:flex;align-items:center;gap:20px;">
                        <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);
                             width:100px;height:100px;font-size:50px;line-height:100px;flex-shrink:0;">
                            {emoji}
                        </div>
                        <div>
                            <h3 style="margin:0;">{cat.get('name','')} <span class="badge badge-adopt">待收养</span></h3>
                            <p style="color:#666;margin:6px 0;">{cat.get('gender','')} · {cat.get('age','')} · {cat.get('fur','')}</p>
                            <p style="color:#888;margin:4px 0;">性格: {'、'.join(personality)}</p>
                            <p style="color:#555;margin:4px 0;">{cat.get('description','')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if is_logged_in():
                    with st.expander(f"📝 申请领养 {cat.get('name','')}"):
                        reason = st.text_area("领养理由", key=f"adopt_r_{cat['id']}",
                                              placeholder="请描述你的养猫经验、居住条件等...")
                        contact = st.text_input("联系方式", key=f"adopt_c_{cat['id']}")
                        if st.button("提交申请", key=f"adopt_s_{cat['id']}"):
                            if reason and contact:
                                result = api.create_adoption(cat["id"], reason, contact)
                                if result and "error" not in result:
                                    st.success("领养申请已提交，请等待管理员审核 🎉")
                                    st.rerun()
                                else:
                                    st.error(f"提交失败: {result.get('error','')}")
                            else:
                                st.warning("请填写完整信息")
        else:
            st.info("目前没有待收养的猫猫 😸 所有猫猫都有归宿啦！")

    # TAB2: 申请记录
    with tab2:
        st.markdown("### 📋 领养申请记录")
        apps = api.list_adoptions()
        if apps:
            for a in apps:
                s_color = {"审核中": "#ff9800", "已通过": "#4caf50", "已拒绝": "#f44336"}.get(
                    a.get("status", ""), "#999")
                st.markdown(f"""
                <div class="info-panel">
                    <h4 style="margin:0;">🐱 {a.get('cat_name','')}
                        <span style="color:{s_color};font-weight:700;">【{a.get('status','')}】</span>
                    </h4>
                    <p style="color:#666;">{a.get('reason','')[:80]}...</p>
                    <p style="color:#999;font-size:0.85em;">
                        👤 {a.get('username','')} · 📅 {format_time(a.get('created_at',''))} · 📞 {a.get('contact','')}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # 管理员审核
                if is_admin() and a.get("status") == "审核中":
                    bc1, bc2 = st.columns(2)
                    if bc1.button("✅ 通过", key=f"ap_{a['id']}"):
                        result = api.review_adoption(a["id"], "已通过")
                        if result and "error" not in result:
                            st.success("已通过！猫猫状态已更新为已收养")
                            st.rerun()
                    if bc2.button("❌ 拒绝", key=f"ar_{a['id']}"):
                        result = api.review_adoption(a["id"], "已拒绝")
                        if result and "error" not in result:
                            st.info("已拒绝")
                            st.rerun()
        else:
            st.info("暂无领养申请记录")

    # TAB3: 回访
    with tab3:
        st.markdown("### 📝 领养回访记录")
        followups = api.list_followups()
        for fu in followups:
            st.markdown(f"""
            <div class="info-panel" style="border-left-color:#4caf50;">
                <h4 style="margin:0;">🐱 {fu.get('cat_name','')}
                    <span class="badge badge-neutered">{fu.get('status','')}</span>
                </h4>
                <p style="color:#555;">{fu.get('content','')}</p>
                <p style="color:#999;font-size:0.85em;">👤 {fu.get('username','')} · 📅 {format_time(fu.get('created_at',''))}</p>
            </div>
            """, unsafe_allow_html=True)

        if is_logged_in():
            with st.expander("📤 提交回访记录"):
                adopted_cats = api.list_cats(status="已收养")
                if adopted_cats:
                    fu_cat_name = st.selectbox("回访猫猫", [c["name"] for c in adopted_cats], key="fu_cat")
                    fu_content = st.text_area("近况反馈", key="fu_content", placeholder="猫猫最近怎么样？")
                    fu_status = st.selectbox("状态", ["良好", "一般", "需关注"], key="fu_status")
                    if st.button("提交回访", key="fu_submit"):
                        if fu_content:
                            fu_cat = next((c for c in adopted_cats if c["name"] == fu_cat_name), None)
                            if fu_cat:
                                result = api.create_followup(fu_cat["id"], fu_content, fu_status)
                                if result and "error" not in result:
                                    st.success("回访记录已提交！")
                                    st.rerun()
                        else:
                            st.warning("请填写内容")
                else:
                    st.info("暂无已收养猫猫")


# ============================================
# 📄 页面：救助求助
# ============================================
def page_rescue():
    st.markdown("## 🆘 救助求助")
    st.markdown("> 发现受伤的猫猫？发布求助信息，让爱心接力！")

    if is_logged_in():
        with st.expander("📝 发布救助信息", expanded=False):
            r_loc = st.text_input("发现地点", key="r_loc")
            r_desc = st.text_area("情况描述", key="r_desc", placeholder="猫猫受伤情况、外观特征等...")
            if st.button("发布求助", key="r_submit"):
                if r_loc and r_desc:
                    result = api.create_rescue(r_loc, r_desc)
                    if result and "error" not in result:
                        st.success("求助信息已发布！🆘")
                        st.rerun()
                    else:
                        st.error("发布失败")

    rescues = api.list_rescues()
    for r in rescues:
        is_done = r.get("status") == "已处理"
        s_bg = "#e8f5e9" if is_done else "#ffebee"
        s_icon = "✅" if is_done else "🆘"
        s_color = "#4caf50" if is_done else "#f44336"
        t_color = "#2e7d32" if is_done else "#c62828"
        st.markdown(f"""
        <div class="info-panel" style="border-left-color:{s_color};background:{s_bg}22;">
            <div style="display:flex;justify-content:space-between;">
                <h4 style="margin:0;">{s_icon} 救助求助 #{r.get('id','')}</h4>
                <span class="badge" style="background:{s_bg};color:{t_color};">{r.get('status','')}</span>
            </div>
            <p style="margin:8px 0;color:#555;">{r.get('description','')}</p>
            <p style="color:#999;font-size:0.85em;">
                📍 {r.get('location','')} · 👤 {r.get('username','')} · 📅 {format_time(r.get('created_at',''))}
            </p>
            {'<p style="color:#2e7d32;margin-top:4px;">📌 处理结果: '+r.get("note","")+'</p>' if r.get("note") else ''}
        </div>
        """, unsafe_allow_html=True)

        if is_admin() and not is_done:
            note = st.text_input("处理备注", key=f"rn_{r['id']}")
            if st.button("标记已处理", key=f"rp_{r['id']}"):
                result = api.resolve_rescue(r["id"], note)
                if result and "error" not in result:
                    st.success("已处理！")
                    st.rerun()


# ============================================
# 📄 页面：评论广场
# ============================================
def page_comments():
    st.markdown("## 💬 评论广场")
    st.markdown("> 所有猫猫的评论汇总，看看大家都在说什么 🐾")

    # 按猫猫筛选
    all_cats = api.list_cats()
    cat_names = ["全部"] + [c["name"] for c in all_cats]
    sel = st.selectbox("筛选猫猫", cat_names)

    cat_id = None
    if sel != "全部":
        matched = next((c for c in all_cats if c["name"] == sel), None)
        if matched:
            cat_id = matched["id"]

    comments = api.list_comments(cat_id=cat_id)

    if comments:
        for cmt in comments:
            st.markdown(f"""
            <div class="comment-card">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span><b>👤 {cmt.get('username','')}</b> → 🐱 <b>{cmt.get('cat_name','')}</b></span>
                    <span style="color:#bbb;font-size:0.82em;">{format_time(cmt.get('created_at',''))}</span>
                </div>
                <p style="margin:10px 0;font-size:1.05em;">{cmt.get('content','')}</p>
                <span style="color:#e91e63;">❤️ {cmt.get('likes',0)}</span>
            </div>
            """, unsafe_allow_html=True)

            # 回复列表
            for rep in cmt.get("replies", []):
                st.markdown(f"""
                <div style="margin-left:30px;background:#fef9ff;border-radius:10px;
                            padding:8px 14px;border-left:3px solid #f48fb1;margin-bottom:4px;">
                    ↪ <b>{rep.get('username','')}</b>: {rep.get('content','')}
                    <span style="color:#bbb;font-size:0.8em;">· {format_time(rep.get('created_at',''))}</span>
                </div>
                """, unsafe_allow_html=True)

            # 互动
            if is_logged_in():
                bc1, bc2, bc3 = st.columns([1, 1, 4])
                with bc1:
                    if st.button("❤️ 赞", key=f"sq_like_{cmt['id']}"):
                        api.like_comment(cmt["id"])
                        st.rerun()
                with bc2:
                    uname = current_username()
                    if uname == cmt.get("username") or is_admin():
                        if st.button("🗑️ 删除", key=f"sq_del_{cmt['id']}"):
                            api.delete_comment(cmt["id"])
                            st.rerun()
            st.markdown("")
    else:
        st.info("暂无评论 😺")

    if is_logged_in():
        st.markdown("---")
        st.caption("💡 如发现违规内容，请联系管理员处理。")


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
                    result = api.create_announcement(a_title, a_content)
                    if result and "error" not in result:
                        st.success("公告已发布！📢")
                        st.rerun()
                    else:
                        st.error("发布失败")

    announcements = api.list_announcements()
    for a in announcements:
        st.markdown(f"""
        <div class="announce-card">
            <h3 style="margin:0 0 8px;">{a.get('title','')}</h3>
            <p style="color:#555;margin:0;line-height:1.7;">{a.get('content','')}</p>
            <p style="color:#bbb;font-size:0.82em;margin-top:10px;">
                📅 {format_time(a.get('created_at',''))} · ✍️ {a.get('author_name','')}
            </p>
        </div>
        """, unsafe_allow_html=True)
        if is_admin():
            if st.button("🗑️ 删除", key=f"del_a_{a['id']}"):
                api.delete_announcement(a["id"])
                st.rerun()


# ============================================
# 📄 页面：个人中心
# ============================================
def page_profile():
    st.markdown("## 👤 个人中心")

    if not is_logged_in():
        st.warning("请先登录 🔑")
        return

    # 刷新用户信息
    me = api.get_me()
    if me:
        st.session_state["user_info"] = me
    else:
        st.error("获取用户信息失败")
        return

    u = me
    role_map = {'admin': '管理员', 'certified': '认证喂猫人', 'user': '普通用户'}

    st.markdown(f"""
    <div class="cat-card" style="text-align:left;display:flex;align-items:center;gap:24px;">
        <div style="font-size:64px;">{u.get('avatar','👤')}</div>
        <div>
            <h2 style="margin:0;">{u.get('nickname','')}</h2>
            <p style="color:#888;margin:4px 0;">用户名: {u.get('username','')}</p>
            <p style="color:#888;margin:4px 0;">角色:
                <span class="badge badge-neutered">{role_map.get(u.get('role','user'),'用户')}</span>
            </p>
            <p style="color:#bbb;font-size:0.85em;">📅 注册时间: {format_time(u.get('created_at',''))}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["❤️ 我的收藏", "💬 我的评论", "🍚 我的打卡", "⚙️ 修改信息"])

    # 收藏
    with tab1:
        fav_cats = api.my_favorites()
        if fav_cats:
            cols = st.columns(min(4, len(fav_cats)))
            for i, cat in enumerate(fav_cats):
                with cols[i % 4]:
                    st.markdown(render_cat_card_html(cat), unsafe_allow_html=True)
                    bc1, bc2 = st.columns(2)
                    with bc1:
                        if st.button("📖 查看", key=f"pf_{cat['id']}", use_container_width=True):
                            st.session_state.detail_cat = cat["id"]
                            st.session_state.page = "📖 猫猫详情"
                            st.rerun()
                    with bc2:
                        if st.button("💔 取消", key=f"pf_unfav_{cat['id']}", use_container_width=True):
                            api.remove_favorite(cat["id"])
                            st.rerun()
        else:
            st.info("还没有收藏猫猫，去图鉴里收藏吧 ❤️")

    # 我的评论
    with tab2:
        all_cmts = api.list_comments()
        my_cmts = [c for c in all_cmts if c.get("username") == u.get("username")]
        if my_cmts:
            for c in my_cmts:
                st.markdown(f"""
                <div class="comment-card">
                    <p style="color:#e91e63;font-weight:700;margin:0;">🐱 {c.get('cat_name','')}</p>
                    <p style="margin:6px 0;">{c.get('content','')}</p>
                    <p style="color:#bbb;font-size:0.82em;">📅 {format_time(c.get('created_at',''))} · ❤️ {c.get('likes',0)}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ 删除评论", key=f"pf_del_cmt_{c['id']}"):
                    api.delete_comment(c["id"])
                    st.rerun()
        else:
            st.info("还没有发表过评论")

    # 我的打卡
    with tab3:
        uid = current_user_id()
        my_feeds = api.list_feedings(user_id=uid) if uid else []
        if my_feeds:
            st.markdown(f"📊 累计投喂 **{len(my_feeds)}** 次")
            for f in my_feeds:
                st.markdown(f"""
                <div class="timeline-item">
                    <span class="timeline-date">{format_time(f.get('created_at',''))}</span>
                    🐱 {f.get('cat_name','')} · 📍 {f.get('location','')} · 🍽️ {f.get('food','')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("还没有投喂记录，去喂猫打卡吧 🍚")

    # 修改信息
    with tab4:
        new_nick = st.text_input("昵称", value=u.get("nickname", ""), key="edit_nick")
        avatars = ["👤", "😺", "😸", "😻", "🧑‍🎓", "👩‍💻", "🐱", "🐾"]
        cur_avatar = u.get("avatar", "👤")
        avatar_idx = avatars.index(cur_avatar) if cur_avatar in avatars else 0
        new_avatar = st.selectbox("头像", avatars, index=avatar_idx, key="edit_avatar")

        if st.button("💾 保存基本信息", use_container_width=True):
            result = api.update_me(nickname=new_nick, avatar=new_avatar)
            if result and "error" not in result:
                st.session_state["user_info"] = result
                st.success("信息已更新！")
                st.rerun()
            else:
                st.error(f"更新失败: {result.get('error','')}")

        st.markdown("---")
        st.markdown("**🔒 修改密码**")
        old_pwd = st.text_input("当前密码", type="password", key="old_pwd")
        new_pwd = st.text_input("新密码", type="password", key="new_pwd")
        new_pwd2 = st.text_input("确认新密码", type="password", key="new_pwd2")
        if st.button("🔐 修改密码", use_container_width=True):
            if not old_pwd or not new_pwd:
                st.warning("请填写完整")
            elif new_pwd != new_pwd2:
                st.error("两次密码不一致")
            else:
                result = api.change_password(old_pwd, new_pwd)
                if result and "error" not in result:
                    st.success("密码修改成功！")
                else:
                    st.error(f"修改失败: {result.get('error','')}")


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
        stats = api.admin_stats()
        if stats:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("🐱 猫猫总数", stats.get("total_cats", 0))
            c2.metric("🏫 在校猫咪", stats.get("on_campus", 0))
            c3.metric("🏠 已收养", stats.get("adopted", 0))
            c4.metric("🌈 回喵星", stats.get("rainbow", 0))

            c5, c6, c7, c8 = st.columns(4)
            c5.metric("👥 用户总数", stats.get("total_users", 0))
            c6.metric("🍚 投喂总量", stats.get("total_feedings", 0))
            c7.metric("💬 评论总数", stats.get("total_comments", 0))
            c8.metric("📋 待审领养", stats.get("pending_adoptions", 0))

        st.markdown("---")
        st.markdown("### 🐱 猫猫状态分布")
        all_cats = api.list_cats()
        if all_cats:
            status_count = {}
            for c in all_cats:
                s = c.get("status", "未知")
                status_count[s] = status_count.get(s, 0) + 1
            df = pd.DataFrame(list(status_count.items()), columns=["状态", "数量"])
            st.bar_chart(df.set_index("状态"))

        st.markdown("### 📦 数据备份")
        if st.button("📥 导出数据备份"):
            backup = api.admin_backup()
            if backup:
                st.download_button("💾 下载 JSON 备份",
                                   json.dumps(backup, ensure_ascii=False, indent=2),
                                   "backup.json", "application/json")

    # TAB: 用户管理
    with tab2:
        st.markdown("### 👥 用户管理")
        users = api.admin_users()
        for usr in users:
            c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
            c1.markdown(f"**{usr.get('avatar','👤')} {usr.get('username','')}**")
            c2.markdown(f"{usr.get('nickname','')}")
            role_options = ["user", "certified", "admin"]
            cur_role = usr.get("role", "user")
            role_idx = role_options.index(cur_role) if cur_role in role_options else 0
            new_role = c3.selectbox("角色", role_options, index=role_idx, key=f"role_{usr['id']}")
            if c4.button("保存", key=f"save_role_{usr['id']}"):
                result = api.admin_update_role(usr["id"], new_role)
                if result and "error" not in result:
                    st.success(f"{usr.get('username','')} 角色已更新为 {new_role}")
                    st.rerun()

    # TAB: 猫猫管理
    with tab3:
        st.markdown("### 🐱 猫猫信息管理")

        # 新增猫猫
        with st.expander("➕ 新增猫猫"):
            nc1, nc2, nc3 = st.columns(3)
            new_name = nc1.text_input("名称", key="new_cat_name")
            new_gender = nc2.selectbox("性别", ["♂ 公", "♀ 母"], key="new_cat_gender")
            new_age = nc3.text_input("年龄", key="new_cat_age", placeholder="如: 2岁")
            nc4, nc5, nc6 = st.columns(3)
            new_fur = nc4.text_input("毛色", key="new_cat_fur")
            new_area = nc5.text_input("常出没区域", key="new_cat_area")
            new_status = nc6.selectbox("状态",
                                        ["在校", "走失", "待收养", "已收养", "回喵星"],
                                        key="new_cat_status")
            new_desc = st.text_area("简介", key="new_cat_desc")
            new_personality = st.text_input("性格标签(逗号分隔)", key="new_cat_pers")

            if st.button("✅ 添加猫猫", key="add_cat"):
                if new_name:
                    import random
                    emojis = ["😺", "😸", "😻", "😽", "😼", "🐱", "🐈", "🐈‍⬛"]
                    colors = ["#FF8C00", "#E91E63", "#424242", "#90CAF9", "#AB47BC",
                              "#607D8B", "#FFB74D", "#FF7043", "#78909C", "#8D6E63"]
                    cat_data = {
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
                        "description": new_desc or "",
                    }
                    result = api.create_cat(cat_data)
                    if result and "error" not in result:
                        st.success(f"已添加猫猫: {new_name} 🎉")
                        st.rerun()
                    else:
                        st.error(f"添加失败: {result.get('error','')}")

        # 编辑现有猫猫
        st.markdown("---")
        all_cats = api.list_cats()
        for cat in all_cats:
            with st.expander(f"{cat.get('emoji','🐱')} {cat.get('name','')} ({cat.get('status','')})"):
                ec1, ec2, ec3 = st.columns(3)
                edit_name = ec1.text_input("名称", cat.get("name", ""), key=f"en_{cat['id']}")
                edit_age = ec2.text_input("年龄", cat.get("age", ""), key=f"ea_{cat['id']}")
                status_options = ["在校", "走失", "待收养", "已收养", "回喵星"]
                cur_status = cat.get("status", "在校")
                s_idx = status_options.index(cur_status) if cur_status in status_options else 0
                edit_status = ec3.selectbox("状态", status_options, index=s_idx, key=f"es_{cat['id']}")

                ec4, ec5 = st.columns(2)
                edit_neutered = ec4.checkbox("已绝育", cat.get("neutered", False), key=f"en2_{cat['id']}")
                edit_vaccine = ec5.checkbox("已免疫", cat.get("vaccine", False), key=f"ev_{cat['id']}")
                edit_area = st.text_input("区域", cat.get("area", ""), key=f"earea_{cat['id']}")
                edit_desc = st.text_area("简介", cat.get("description", ""), key=f"ed_{cat['id']}")

                if st.button("💾 保存修改", key=f"save_cat_{cat['id']}"):
                    update_data = {
                        "name": edit_name,
                        "age": edit_age,
                        "status": edit_status,
                        "neutered": edit_neutered,
                        "vaccine": edit_vaccine,
                        "area": edit_area,
                        "description": edit_desc,
                    }
                    result = api.update_cat(cat["id"], update_data)
                    if result and "error" not in result:
                        st.success(f"{edit_name} 信息已更新！")
                        st.rerun()
                    else:
                        st.error(f"更新失败: {result.get('error','')}")

    # TAB: 内容管理
    with tab4:
        st.markdown("### 🛡️ 内容管理")

        st.markdown("**💬 评论管理**")
        all_cmts = api.list_comments()
        for cmt in all_cmts:
            c1, c2, c3 = st.columns([4, 1, 1])
            c1.markdown(
                f"**{cmt.get('username','')}** → 🐱{cmt.get('cat_name','')}: {cmt.get('content','')[:50]}...")
            c2.markdown(f"❤️ {cmt.get('likes', 0)}")
            if c3.button("🗑️", key=f"admin_del_cmt_{cmt['id']}"):
                api.delete_comment(cmt["id"])
                st.success("评论已删除")
                st.rerun()

        st.markdown("---")
        st.markdown("**🆘 求助管理**")
        rescues = api.list_rescues()
        pending_rescues = [r for r in rescues if r.get("status") != "已处理"]
        if pending_rescues:
            for r in pending_rescues:
                st.markdown(
                    f"🆘 #{r.get('id','')} {r.get('description','')[:60]}... — **{r.get('status','')}**")
                note = st.text_input("处理备注", key=f"admin_rn_{r['id']}")
                if st.button("标记已处理", key=f"admin_rp_{r['id']}"):
                    api.resolve_rescue(r["id"], note)
                    st.rerun()
        else:
            st.info("暂无待处理的求助")


# ============================================
# 🧭 主导航
# ============================================
def main():
    # 初始化导航状态
    if "page" not in st.session_state:
        st.session_state.page = "🏠 首页"
    if "detail_cat" not in st.session_state:
        st.session_state.detail_cat = None

    # ── 侧边栏 ──
    st.sidebar.markdown("""
    <div style="text-align:center;padding:10px 0 5px;">
        <h1 style="color:#c2185b;margin:0;font-size:1.6em;">🐾 猫猫校园</h1>
        <p style="color:#e91e63;font-size:0.9em;margin:0;">北华大学校园猫咪平台</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    render_auth()
    st.sidebar.markdown("---")

    # 导航菜单
    pages = [
        "🏠 首页",
        "🐱 猫猫图鉴",
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

    # 猫猫详情页不出现在导航列表
    cur_page = st.session_state.page
    default_idx = 0
    if cur_page in pages:
        default_idx = pages.index(cur_page)

    selected = st.sidebar.radio("导航菜单", pages, index=default_idx, label_visibility="collapsed")

    # 处理导航跳转逻辑
    if st.session_state.page != "📖 猫猫详情":
        st.session_state.page = selected
    elif selected != pages[0]:
        # 用户在详情页时点击了其他导航
        st.session_state.page = selected

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align:center;padding:10px;color:#c2185b;font-size:0.85em;">
        <p>🐱 用爱守护每一只校园猫咪</p>
        <p style="color:#ddd;">© 2024 北华大学猫猫校园</p>
        <p style="font-size:0.8em;color:#ccc;">Made with ❤️ & Streamlit + FastAPI</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 页面路由 ──
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