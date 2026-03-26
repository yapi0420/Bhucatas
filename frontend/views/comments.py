"""评论广场"""
import streamlit as st

from api_client import api
from utils import (
    is_logged_in, is_admin, current_username,
    format_time, render_reply_html,
    # ❌ 移除了未使用的 render_comment_html（此页面用含 cat_name 的自定义 HTML）
)


def page_comments():
    st.markdown("## 💬 评论广场")
    st.markdown("> 所有猫猫的评论汇总 🐾")

    all_cats = api.list_cats()
    cat_names = ["全部"] + [c["name"] for c in all_cats]
    sel = st.selectbox("筛选猫猫", cat_names)

    cat_id = None
    if sel != "全部":
        matched = next((c for c in all_cats if c["name"] == sel), None)
        if matched:
            cat_id = matched["id"]

    comments = api.list_comments(cat_id=cat_id)

    if not comments:
        st.info("暂无评论 😺")
        return

    for cmt in comments:
        # 评论广场需要显示 cat_name，所以用自定义 HTML 而非 render_comment_html
        st.markdown(f"""
        <div class="comment-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span><b>👤 {cmt.get('username','')}</b> → 🐱
                    <b>{cmt.get('cat_name','')}</b></span>
                <span style="color:#bbb;font-size:0.82em;">
                    {format_time(cmt.get('created_at',''))}</span>
            </div>
            <p style="margin:10px 0;font-size:1.05em;">{cmt.get('content','')}</p>
            <span style="color:#e91e63;">❤️ {cmt.get('likes',0)}</span>
        </div>
        """, unsafe_allow_html=True)

        for rep in cmt.get("replies", []):
            st.markdown(render_reply_html(
                rep.get("username", ""), format_time(rep.get("created_at", "")),
                rep.get("content", "")
            ), unsafe_allow_html=True)

        if is_logged_in():
            bc1, bc2, _ = st.columns([1, 1, 4])
            with bc1:
                if st.button("❤️ 赞", key=f"sq_like_{cmt['id']}"):
                    api.like_comment(cmt["id"])
                    st.rerun()
            with bc2:
                if current_username() == cmt.get("username") or is_admin():
                    if st.button("🗑️ 删除", key=f"sq_del_{cmt['id']}"):
                        api.delete_comment(cmt["id"])
                        st.rerun()
        st.markdown("")

    if is_logged_in():
        st.markdown("---")
        st.caption("💡 如发现违规内容，请联系管理员处理。")