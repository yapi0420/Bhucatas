"""猫猫图鉴"""
import streamlit as st
from api_client import api
from utils import is_logged_in, render_cat_card_html
from config import PAGE_DETAIL


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
        name=search_name or None,
        gender=filter_gender,
        status=filter_status,
        neutered=filter_neutered,
    )

    st.markdown(f"共找到 **{len(cats)}** 只猫猫 🐾")

    if not cats:
        st.info("没有找到匹配的猫猫 😿")
        return

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
                        st.session_state.page = PAGE_DETAIL
                        st.rerun()
                with bc2:
                    _render_fav_button(cat)


def _render_fav_button(cat: dict):
    """收藏 / 取消收藏按钮"""
    if not is_logged_in():
        st.button("❤️ 收藏", key=f"fav_no_{cat['id']}", disabled=True,
                  use_container_width=True, help="请先登录")
        return

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