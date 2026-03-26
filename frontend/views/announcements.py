"""校园公告"""
import streamlit as st
from api_client import api
from utils import is_admin, format_time, render_announce_html


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

    for a in api.list_announcements():
        st.markdown(render_announce_html(
            a.get("title", ""), a.get("content", ""),
            format_time(a.get("created_at", "")), a.get("author_name", "")
        ), unsafe_allow_html=True)
        if is_admin():
            if st.button("🗑️ 删除", key=f"del_a_{a['id']}"):
                api.delete_announcement(a["id"])
                st.rerun()