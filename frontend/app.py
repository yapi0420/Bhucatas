"""
🐱 北华大学猫猫校园 — Streamlit 前端主入口
"""
import streamlit as st

from styles import inject_css
from auth import render_auth_sidebar
from utils import is_admin
from config import NAV_PAGES, PAGE_HOME, PAGE_DETAIL, PAGE_ADMIN
from views import PAGE_REGISTRY

st.set_page_config(
    page_title="🐱 北华大学猫猫校园",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

if "page" not in st.session_state:
    st.session_state.page = PAGE_HOME
if "detail_cat" not in st.session_state:
    st.session_state.detail_cat = None

# ═══ 侧边栏 ═══

st.sidebar.markdown("""
<div style="text-align:center;padding:10px 0 5px;">
    <h1 style="color:#c2185b;margin:0;font-size:1.6em;">🐾 猫猫校园</h1>
    <p style="color:#e91e63;font-size:0.9em;margin:0;">北华大学校园猫咪平台</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
render_auth_sidebar()
st.sidebar.markdown("---")

nav_pages = list(NAV_PAGES)
if is_admin():
    nav_pages.append(PAGE_ADMIN)

cur_page = st.session_state.page
default_idx = nav_pages.index(cur_page) if cur_page in nav_pages else 0

selected = st.sidebar.radio(
    "导航菜单", nav_pages,
    index=default_idx,
    label_visibility="collapsed",
)

if st.session_state.page != PAGE_DETAIL:
    st.session_state.page = selected
elif selected != nav_pages[0]:
    st.session_state.page = selected

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align:center;padding:10px;color:#c2185b;font-size:0.85em;">
    <p>🐱 用爱守护每一只校园猫咪</p>
    <p style="color:#ddd;">© 2024 北华大学猫猫校园</p>
    <p style="font-size:0.8em;color:#ccc;">Streamlit + FastAPI</p>
</div>
""", unsafe_allow_html=True)

# ═══ 路由分发 ═══

page_func = PAGE_REGISTRY.get(st.session_state.page, PAGE_REGISTRY[PAGE_HOME])
page_func()