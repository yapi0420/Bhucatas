"""喂猫打卡"""
import streamlit as st
import pandas as pd
from api_client import api
from utils import is_logged_in, current_user_id, format_time, render_timeline_item


def page_feeding():
    st.markdown("## 🍚 喂猫打卡")
    st.markdown("> 记录你的每一次投喂，让爱心看得见 💕")

    if not is_logged_in():
        st.warning("请登录后使用打卡功能 🔑")
        return

    tab1, tab2 = st.tabs(["📝 打卡投喂", "📊 投喂统计"])

    with tab1:
        _tab_checkin()
    with tab2:
        _tab_stats()


def _tab_checkin():
    st.markdown("### 🐾 新建投喂打卡")
    campus_cats = api.list_cats(status="在校")
    if not campus_cats:
        st.info("暂无在校猫猫")
        return

    cat_map = {c["name"]: c for c in campus_cats}
    c1, c2 = st.columns(2)
    sel_name = c1.selectbox("选择投喂的猫猫 🐱", list(cat_map.keys()))
    loc = c2.text_input("投喂地点 📍", value=cat_map[sel_name].get("area", "") if sel_name else "")
    food = st.text_input("投喂内容 🍽️", placeholder="如: 猫粮+猫罐头")

    if st.button("✅ 提交打卡", use_container_width=True):
        if sel_name and food:
            result = api.create_feeding(cat_map[sel_name]["id"], loc, food)
            if result and "error" not in result:
                st.success(f"打卡成功！感谢你投喂了 {sel_name} 🎉")
                st.balloons()
                st.rerun()
            else:
                st.error(f"打卡失败: {result.get('error','')}")
        else:
            st.warning("请填写完整信息")

    st.markdown("---")
    st.markdown("### 📋 最近投喂记录")
    for fd in api.list_feedings(limit=10):
        content = (f"👤 {fd.get('username','')} 在 📍{fd.get('location','')} "
                   f"投喂了 🐱<b>{fd.get('cat_name','')}</b> · 🍽️ {fd.get('food','')}")
        st.markdown(render_timeline_item(format_time(fd.get('created_at', '')), content),
                    unsafe_allow_html=True)


def _tab_stats():
    st.markdown("### 📊 投喂统计")
    stats = api.feeding_stats()
    if stats:
        df = pd.DataFrame(stats)
        df.columns = ["猫猫", "投喂次数"]
        df = df.sort_values("投喂次数", ascending=False)
        st.bar_chart(df.set_index("猫猫"))

        st.markdown("**🏆 投喂排行榜**")
        for i, (_, row) in enumerate(df.iterrows()):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"  {i + 1}."
            st.markdown(f"{medal} **{row['猫猫']}** — 被投喂 {int(row['投喂次数'])} 次")

    uid = current_user_id()
    if uid:
        my_feeds = api.list_feedings(user_id=uid)
        st.markdown(f"\n---\n### 🙋 我的投喂\n\n你已累计投喂 **{len(my_feeds)}** 次 🎉")