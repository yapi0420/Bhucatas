"""全局 CSS 样式"""
import streamlit as st


def inject_css():
    """注入全局 CSS"""
    st.markdown(CSS, unsafe_allow_html=True)


CSS = """
<style>
/* ══════════ 整体背景 ══════════ */
.stApp {
    background: linear-gradient(160deg, #fff0f5 0%, #fce4ec 30%, #f3e5f5 60%, #e8eaf6 100%);
}

/* ══════════ 侧边栏 ══════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce4ec 0%, #f8bbd0 100%);
    border-right: 3px solid #f48fb1;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #c2185b;
}

/* ══════════ 卡片 ══════════ */
.cat-card {
    background: white; border-radius: 20px; padding: 24px; margin: 10px 0;
    box-shadow: 0 4px 20px rgba(233,30,99,0.10); border: 2px solid #fce4ec;
    transition: all 0.3s ease; text-align: center;
}
.cat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 30px rgba(233,30,99,0.18); border-color: #f48fb1;
}

/* ══════════ 头像 ══════════ */
.cat-avatar {
    width: 120px; height: 120px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 60px; margin: 0 auto 12px auto;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08); border: 4px solid white;
}

/* ══════════ 标签 ══════════ */
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

/* ══════════ 信息面板 ══════════ */
.info-panel {
    background: linear-gradient(135deg, #ffffff, #fff5f7);
    border-radius: 16px; padding: 20px; margin: 10px 0;
    border-left: 5px solid #f48fb1;
    box-shadow: 0 2px 12px rgba(233,30,99,0.06);
}

/* ══════════ 统计卡片 ══════════ */
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

/* ══════════ 时间线 ══════════ */
.timeline-item {
    background: white; border-radius: 12px; padding: 14px 18px;
    margin: 8px 0; border-left: 4px solid #f48fb1;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    display: flex; align-items: center; gap: 12px;
}
.timeline-date {
    color: #e91e63; font-weight: 700; font-size: 0.88em; white-space: nowrap;
}

/* ══════════ 评论 ══════════ */
.comment-card {
    background: white; border-radius: 14px; padding: 16px; margin: 8px 0;
    border: 1px solid #f8bbd0; box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}

/* ══════════ 公告 ══════════ */
.announce-card {
    background: linear-gradient(135deg, #fff8e1, #fff3e0);
    border-radius: 14px; padding: 18px; margin: 8px 0;
    border-left: 5px solid #ffb300; box-shadow: 0 2px 10px rgba(255,179,0,0.1);
}

/* ══════════ 欢迎横幅 ══════════ */
.welcome-banner {
    background: linear-gradient(135deg, #ec407a 0%, #ab47bc 50%, #7c4dff 100%);
    border-radius: 24px; padding: 40px; color: white; text-align: center;
    margin-bottom: 24px; box-shadow: 0 8px 32px rgba(233,30,99,0.25);
}
.welcome-banner h1 {
    font-size: 2.4em; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.15);
}
.welcome-banner p { font-size: 1.15em; opacity: 0.92; margin-top: 8px; }

/* ══════════ 按钮 ══════════ */
.stButton > button {
    border-radius: 25px !important; padding: 0.4rem 1.6rem !important;
    font-weight: 600 !important; border: 2px solid #f48fb1 !important;
    transition: all 0.3s !important;
}
.stButton > button:hover {
    background: #fce4ec !important; border-color: #ec407a !important;
    transform: scale(1.03);
}

/* ══════════ 选项卡 ══════════ */
.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] {
    border-radius: 12px 12px 0 0; padding: 8px 20px; font-weight: 600;
}

/* ══════════ 关系图谱 ══════════ */
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

/* ══════════ 隐藏默认元素 ══════════ */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""