"""寻猫启事"""
import streamlit as st
from api_client import api
from utils import is_logged_in, is_admin, current_username, format_time


def page_lost():
    st.markdown("## 🔍 寻猫启事")
    st.markdown("> 找不到猫猫？发布寻猫启事，大家一起帮忙找！")

    if is_logged_in():
        with st.expander("📝 发布寻猫启事", expanded=False):
            l_name = st.text_input("走失猫猫名称/特征", key="lost_name")
            l_loc = st.text_input("最后出现地点", key="lost_loc")
            l_desc = st.text_area("详细描述", key="lost_desc")
            if st.button("发布启事", key="lost_submit"):
                if l_name and l_desc:
                    result = api.create_lost(l_name, l_desc, l_loc)
                    if result and "error" not in result:
                        st.success("寻猫启事发布成功！🐾")
                        st.rerun()

    for notice in api.list_lost():
        found = notice.get("found", False)
        _render_lost_card(notice, found)

        if is_logged_in() and not found:
            uname = current_username()
            if uname == notice.get("username") or is_admin():
                mc1, mc2 = st.columns([3, 1])
                fn = mc1.text_input("找回备注", key=f"fn_{notice['id']}")
                if mc2.button("标记已找回", key=f"found_{notice['id']}"):
                    api.mark_found(notice["id"], fn)
                    st.success("已标记为找回！🎉")
                    st.rerun()


def _render_lost_card(notice: dict, found: bool):
    bg = "#e8f5e9" if found else "#fff3e0"
    border = "#4caf50" if found else "#ff9800"
    color = "#2e7d32" if found else "#e65100"
    label = "✅ 已找回" if found else "🔍 寻找中"
    found_note = notice.get("found_note", "")
    st.markdown(f"""
    <div class="info-panel" style="border-left-color:{border};background:{bg}22;">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <h4 style="margin:0;">🐱 {notice.get('cat_name','')}</h4>
            <span class="badge" style="background:{bg};color:{color};">{label}</span>
        </div>
        <p style="margin:8px 0;color:#555;">{notice.get('description','')}</p>
        <p style="color:#999;font-size:0.85em;">
            📍 {notice.get('location','')} · 👤 {notice.get('username','')}
            · 📅 {format_time(notice.get('created_at',''))}
        </p>
        {'<p style="color:#2e7d32;margin-top:6px;">📌 '+found_note+'</p>' if found and found_note else ''}
    </div>
    """, unsafe_allow_html=True)