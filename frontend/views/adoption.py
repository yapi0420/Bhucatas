"""领养中心"""
import streamlit as st
from api_client import api
from utils import is_logged_in, is_admin, ensure_list, format_time


def page_adoption():
    st.markdown("## 🏠 领养中心")
    st.markdown("> 给流浪的它们一个温暖的家 💕")

    tab1, tab2, tab3 = st.tabs(["🐱 待收养猫咪", "📋 领养申请", "📝 领养回访"])

    with tab1:
        _tab_waiting()
    with tab2:
        _tab_applications()
    with tab3:
        _tab_followups()


def _tab_waiting():
    cats = api.list_cats(status="待收养")
    if not cats:
        st.info("目前没有待收养的猫猫 😸")
        return

    for cat in cats:
        personality = ensure_list(cat.get("personality", []))
        color = cat.get("color", "#FF8C00")
        emoji = cat.get("emoji", "🐱")
        st.markdown(f"""
        <div class="cat-card" style="text-align:left;">
            <div style="display:flex;align-items:center;gap:20px;">
                <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);
                     width:100px;height:100px;font-size:50px;line-height:100px;flex-shrink:0;">
                    {emoji}
                </div>
                <div>
                    <h3 style="margin:0;">{cat.get('name','')}
                        <span class="badge badge-adopt">待收养</span></h3>
                    <p style="color:#666;margin:6px 0;">
                        {cat.get('gender','')} · {cat.get('age','')} · {cat.get('fur','')}</p>
                    <p style="color:#888;">性格: {'、'.join(personality)}</p>
                    <p style="color:#555;">{cat.get('description','')}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_logged_in():
            with st.expander(f"📝 申请领养 {cat.get('name','')}"):
                reason = st.text_area("领养理由", key=f"adopt_r_{cat['id']}")
                contact = st.text_input("联系方式", key=f"adopt_c_{cat['id']}")
                if st.button("提交申请", key=f"adopt_s_{cat['id']}"):
                    if reason and contact:
                        result = api.create_adoption(cat["id"], reason, contact)
                        if result and "error" not in result:
                            st.success("领养申请已提交 🎉")
                            st.rerun()
                    else:
                        st.warning("请填写完整信息")


def _tab_applications():
    st.markdown("### 📋 领养申请记录")
    apps = api.list_adoptions()
    if not apps:
        st.info("暂无领养申请记录")
        return

    for a in apps:
        s_color = {"审核中": "#ff9800", "已通过": "#4caf50", "已拒绝": "#f44336"}.get(
            a.get("status", ""), "#999")
        st.markdown(f"""
        <div class="info-panel">
            <h4 style="margin:0;">🐱 {a.get('cat_name','')}
                <span style="color:{s_color};font-weight:700;">【{a.get('status','')}】</span></h4>
            <p style="color:#666;">{a.get('reason','')[:80]}...</p>
            <p style="color:#999;font-size:0.85em;">
                👤 {a.get('username','')} · 📅 {format_time(a.get('created_at',''))}
                · 📞 {a.get('contact','')}</p>
        </div>
        """, unsafe_allow_html=True)

        if is_admin() and a.get("status") == "审核中":
            bc1, bc2 = st.columns(2)
            if bc1.button("✅ 通过", key=f"ap_{a['id']}"):
                api.review_adoption(a["id"], "已通过")
                st.success("已通过！")
                st.rerun()
            if bc2.button("❌ 拒绝", key=f"ar_{a['id']}"):
                api.review_adoption(a["id"], "已拒绝")
                st.rerun()


def _tab_followups():
    st.markdown("### 📝 领养回访记录")
    for fu in api.list_followups():
        st.markdown(f"""
        <div class="info-panel" style="border-left-color:#4caf50;">
            <h4 style="margin:0;">🐱 {fu.get('cat_name','')}
                <span class="badge badge-neutered">{fu.get('status','')}</span></h4>
            <p style="color:#555;">{fu.get('content','')}</p>
            <p style="color:#999;font-size:0.85em;">
                👤 {fu.get('username','')} · 📅 {format_time(fu.get('created_at',''))}</p>
        </div>
        """, unsafe_allow_html=True)

    if is_logged_in():
        with st.expander("📤 提交回访记录"):
            adopted_cats = api.list_cats(status="已收养")
            if not adopted_cats:
                st.info("暂无已收养猫猫")
                return
            fu_cat_name = st.selectbox("回访猫猫", [c["name"] for c in adopted_cats], key="fu_cat")
            fu_content = st.text_area("近况反馈", key="fu_content")
            fu_status = st.selectbox("状态", ["良好", "一般", "需关注"], key="fu_status")
            if st.button("提交回访", key="fu_submit"):
                if fu_content:
                    fu_cat = next((c for c in adopted_cats if c["name"] == fu_cat_name), None)
                    if fu_cat:
                        api.create_followup(fu_cat["id"], fu_content, fu_status)
                        st.success("回访记录已提交！")
                        st.rerun()