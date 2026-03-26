"""全局 CSS 样式 - 增强对比度优化版"""
import streamlit as st

CSS = """
<style>
/* ══════════ 1. 全局文字与背景控制 ══════════ */
/* 强制所有基础文字颜色为深灰色，确保在浅色背景上清晰 */
html, body, [data-testid="stWidgetLabel"], .stMarkdown, p, span {
    color: #333333 !important;
    font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}

.stApp {
    background: linear-gradient(160deg, #fff0f5 0%, #fce4ec 30%, #f3e5f5 60%, #e8eaf6 100%);
}

/* ══════════ 2. 侧边栏样式优化 ══════════ */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fce4ec 0%, #f8bbd0 100%);
    border-right: 3px solid #f48fb1;
}

/* 侧边栏标题颜色加深 */
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #880e4f !important; /* 深紫色/深粉色 */
}

/* 侧边栏单选框、输入框标签颜色 */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #6a1b9a !important;
    font-weight: 600 !important;
}

/* ══════════ 3. 输入框/下拉框/文本框优化 (解决看不清的问题) ══════════ */
/* 强制输入框背景为白色，文字为深色 */
input, select, textarea, [data-baseweb="select"] {
    background-color: #ffffff !important;
    color: #222222 !important;
    border-radius: 10px !important;
}

/* 针对下拉列表选中的项 */
[data-baseweb="popover"] {
    background-color: #ffffff !important;
}
[data-baseweb="select"] div {
    color: #222222 !important;
}

/* ══════════ 4. 猫猫卡片样式增强 ══════════ */
.cat-card {
    background: #ffffff; /* 纯白背景 */
    border-radius: 20px;
    padding: 24px;
    margin: 10px 0;
    box-shadow: 0 4px 20px rgba(233,30,99,0.12);
    border: 2px solid #f8bbd0;
    transition: all 0.3s ease;
    text-align: center;
}

.cat-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 30px rgba(233,30,99,0.2);
    border-color: #f06292;
}

.cat-card h3 {
    color: #2c3e50 !important; /* 深青黑色 */
    margin: 8px 0 4px !important;
    font-weight: 800 !important;
}

.cat-card p {
    color: #546e7a !important; /* 深蓝灰色 */
    font-size: 0.9em;
}

/* ══════════ 5. 信息面板 (info-panel) ══════════ */
.info-panel {
    background: #ffffff !important;
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    border-left: 6px solid #f06292;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.info-panel b {
    color: #ad1457 !important; /* 深红色标题 */
}

.info-panel span {
    color: #333333 !important; /* 深色内容 */
}

/* ══════════ 6. 标签 (Badge) 优化 ══════════ */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: 800;
    margin: 3px;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.badge-school   { background: #e8f5e9; color: #1b5e20 !important; }
.badge-lost     { background: #fff3e0; color: #e65100 !important; }
.badge-adopt    { background: #e3f2fd; color: #0d47a1 !important; }
.badge-adopted  { background: #f3e5f5; color: #4a148c !important; }
.badge-star     { background: #ffebee; color: #b71c1c !important; }
.badge-male     { background: #e1f5fe; color: #01579b !important; }
.badge-female   { background: #fdf2f8; color: #880e4f !important; }
.badge-neutered { background: #f1f8e9; color: #33691e !important; }
.badge-vaccine  { background: #e0f7fa; color: #006064 !important; }

/* ══════════ 7. 统计卡片与横幅 ══════════ */
.stat-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 2px solid #f8bbd0;
}
.stat-number {
    font-size: 2.6em;
    font-weight: 900;
    color: #d81b60 !important; /* 强制深粉色数字 */
}
.stat-label {
    color: #455a64 !important;
    font-weight: 600;
}

.welcome-banner {
    background: linear-gradient(135deg, #d81b60 0%, #8e24aa 50%, #5e35b1 100%);
    border-radius: 24px;
    padding: 40px;
    color: #ffffff !important;
    text-align: center;
    margin-bottom: 24px;
}
.welcome-banner h1, .welcome-banner p {
    color: #ffffff !important; /* 强制白色文字 */
}

/* ══════════ 8. 按钮与选项卡 ══════════ */
.stButton > button {
    background-color: #ffffff !important;
    color: #ad1457 !important;
    border: 2px solid #f06292 !important;
    font-weight: 700 !important;
}
.stButton > button:hover {
    background-color: #f06292 !important;
    color: #ffffff !important;
}

/* 选项卡标题文字颜色 */
.stTabs [data-baseweb="tab"] {
    color: #880e4f !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    color: #d81b60 !important;
    border-bottom-color: #d81b60 !important;
}

/* ══════════ 9. 隐藏默认元素 ══════════ */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)