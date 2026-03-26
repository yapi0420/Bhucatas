"""首页"""
import streamlit as st
from api_client import api
from utils import render_cat_card_html, render_stat_card, render_timeline_item, format_time
from config import PAGE_DETAIL


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

    # 统计
    all_cats = api.list_cats()
    feedings = api.list_feedings(limit=5)
    announcements = api.list_announcements()

    on_campus = len([c for c in all_cats if c.get("status") == "在校"])
    adopted = len([c for c in all_cats if c.get("status") == "已收养"])

    cols = st.columns(4)
    stat_data = [
        ("🐱", str(len(all_cats)), "猫猫总数"),
        ("🏫", str(on_campus), "在校猫咪"),
        ("🏠", str(adopted), "已收养"),
        ("🍚", str(len(feedings)), "近期投喂"),
    ]
    for col, (icon, num, label) in zip(cols, stat_data):
        col.markdown(render_stat_card(icon, num, label), unsafe_allow_html=True)

    st.markdown("---")

    # 随机推荐
    st.markdown("### ✨ 今日推荐猫猫")
    random_cats = api.random_cats(4)
    if random_cats:
        rcols = st.columns(len(random_cats))
        for col, cat in zip(rcols, random_cats):
            with col:
                st.markdown(render_cat_card_html(cat), unsafe_allow_html=True)
                if st.button(f"查看 {cat['name']} 详情", key=f"home_{cat['id']}",
                             use_container_width=True):
                    st.session_state.detail_cat = cat["id"]
                    st.session_state.page = PAGE_DETAIL
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
    for f in feedings:
        content = (f"👤 {f.get('username','')} 在 📍{f.get('location','')} "
                   f"投喂了 🐱<b>{f.get('cat_name','')}</b> ({f.get('food','')})")
        st.markdown(render_timeline_item(format_time(f.get('created_at', '')), content),
                    unsafe_allow_html=True)