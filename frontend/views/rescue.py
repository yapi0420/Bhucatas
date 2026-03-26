"""救助求助"""
import streamlit as st
from api_client import api
from utils import is_logged_in, is_admin, format_time


def page_rescue():
    st.markdown("## 🆘 救助求助")
    st.markdown("> 发现受伤的猫猫？发布求助信息，让爱心接力！")

    if is_logged_in():
        with st.expander("📝 发布救助信息", expanded=False):
            r_loc = st.text_input("发现地点", key="r_loc")
            r_desc = st.text_area("情况描述", key="r_desc")
            if st.button("发布求助", key="r_submit"):
                if r_loc and r_desc:
                    result = api.create_rescue(r_loc, r_desc)
                    if result and "error" not in result:
                        st.success("求助信息已发布！🆘")
                        st.rerun()

    for r in api.list_rescues():
        done = r.get("status") == "已处理"
        bg = "#e8f5e9" if done else "#ffebee"
        icon = "✅" if done else "🆘"
        border = "#4caf50" if done else "#f44336"
        txt_c = "#2e7d32" if done else "#c62828"
        st.markdown(f"""
        <div class="info-panel" style="border-left-color:{border};background:{bg}22;">
            <div style="display:flex;justify-content:space-between;">
                <h4 style="margin:0;">{icon} 救助求助 #{r.get('id','')}</h4>
                <span class="badge" style="background:{bg};color:{txt_c};">{r.get('status','')}</span>
            </div>
            <p style="margin:8px 0;color:#555;">{r.get('description','')}</p>
            <p style="color:#999;font-size:0.85em;">
                📍 {r.get('location','')} · 👤 {r.get('username','')}
                · 📅 {format_time(r.get('created_at',''))}</p>
            {'<p style="color:#2e7d32;margin-top:4px;">📌 '+r.get("note","")+'</p>' if r.get("note") else ''}
        </div>
        """, unsafe_allow_html=True)

        if is_admin() and not done:
            note = st.text_input("处理备注", key=f"rn_{r['id']}")
            if st.button("标记已处理", key=f"rp_{r['id']}"):
                api.resolve_rescue(r["id"], note)
                st.success("已处理！")
                st.rerun()