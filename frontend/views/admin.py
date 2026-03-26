"""管理后台"""
import json
import random

import streamlit as st
import pandas as pd

from api_client import api
from utils import is_admin
# ❌ 移除了未使用的 format_time
from config import CAT_STATUS_OPTIONS, CAT_EMOJIS, CAT_COLORS


def page_admin():
    st.markdown("## ⚙️ 管理后台")
    if not is_admin():
        st.error("🚫 无权限访问")
        return

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 数据统计", "👥 用户管理", "🐱 猫猫管理", "🛡️ 内容管理"])
    with tab1:
        _tab_stats()
    with tab2:
        _tab_users()
    with tab3:
        _tab_cats()
    with tab4:
        _tab_content()


def _tab_stats():
    st.markdown("### 📊 平台数据概览")
    stats = api.admin_stats()
    if stats:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🐱 猫猫总数", stats.get("total_cats", 0))
        c2.metric("🏫 在校猫咪", stats.get("on_campus", 0))
        c3.metric("🏠 已收养", stats.get("adopted", 0))
        c4.metric("🌈 回喵星", stats.get("rainbow", 0))
        c5, c6, c7, c8 = st.columns(4)
        c5.metric("👥 用户总数", stats.get("total_users", 0))
        c6.metric("🍚 投喂总量", stats.get("total_feedings", 0))
        c7.metric("💬 评论总数", stats.get("total_comments", 0))
        c8.metric("📋 待审领养", stats.get("pending_adoptions", 0))

    st.markdown("---")
    st.markdown("### 🐱 猫猫状态分布")
    all_cats = api.list_cats()
    if all_cats:
        sc = {}
        for c in all_cats:
            s = c.get("status", "未知")
            sc[s] = sc.get(s, 0) + 1
        df = pd.DataFrame(list(sc.items()), columns=["状态", "数量"])
        st.bar_chart(df.set_index("状态"))

    st.markdown("### 📦 数据备份")
    if st.button("📥 导出数据备份"):
        backup = api.admin_backup()
        if backup:
            st.download_button(
                "💾 下载 JSON 备份",
                json.dumps(backup, ensure_ascii=False, indent=2),
                "backup.json", "application/json"
            )


def _tab_users():
    st.markdown("### 👥 用户管理")
    users = api.admin_users()
    role_options = ["user", "certified", "admin"]
    for usr in users:
        c1, c2, c3, c4 = st.columns([2, 2, 2, 1])
        c1.markdown(f"**{usr.get('avatar','👤')} {usr.get('username','')}**")
        c2.markdown(usr.get("nickname", ""))
        cur = usr.get("role", "user")
        idx = role_options.index(cur) if cur in role_options else 0
        new_role = c3.selectbox("角色", role_options, index=idx,
                                key=f"role_{usr['id']}")
        if c4.button("保存", key=f"sr_{usr['id']}"):
            result = api.admin_update_role(usr["id"], new_role)
            if result and "error" not in result:
                st.success(f"{usr.get('username','')} → {new_role}")
                st.rerun()


def _tab_cats():
    st.markdown("### 🐱 猫猫信息管理")

    with st.expander("➕ 新增猫猫"):
        nc1, nc2, nc3 = st.columns(3)
        new_name = nc1.text_input("名称", key="nc_name")
        new_gender = nc2.selectbox("性别", ["♂ 公", "♀ 母"], key="nc_gender")
        new_age = nc3.text_input("年龄", key="nc_age", placeholder="如: 2岁")
        nc4, nc5, nc6 = st.columns(3)
        new_fur = nc4.text_input("毛色", key="nc_fur")
        new_area = nc5.text_input("区域", key="nc_area")
        new_status = nc6.selectbox("状态", CAT_STATUS_OPTIONS, key="nc_status")
        new_desc = st.text_area("简介", key="nc_desc")
        new_pers = st.text_input("性格(逗号分隔)", key="nc_pers")
        if st.button("✅ 添加猫猫", key="add_cat"):
            if new_name:
                data = {
                    "name": new_name,
                    "emoji": random.choice(CAT_EMOJIS),
                    "color": random.choice(CAT_COLORS),
                    "gender": new_gender,
                    "age": new_age or "未知",
                    "breed": "中华田园猫",
                    "fur": new_fur or "未知",
                    "neutered": False,
                    "status": new_status,
                    "area": new_area or "未知",
                    "personality": [x.strip() for x in new_pers.split(",")
                                    if x.strip()] or ["待观察"],
                    "vaccine": False,
                    "deworm": False,
                    "description": new_desc or "",
                }
                result = api.create_cat(data)
                if result and "error" not in result:
                    st.success(f"已添加: {new_name} 🎉")
                    st.rerun()

    st.markdown("---")
    for cat in api.list_cats():
        with st.expander(f"{cat.get('emoji','🐱')} {cat.get('name','')} "
                         f"({cat.get('status','')})"):
            ec1, ec2, ec3 = st.columns(3)
            e_name = ec1.text_input("名称", cat.get("name", ""), key=f"en_{cat['id']}")
            e_age = ec2.text_input("年龄", cat.get("age", ""), key=f"ea_{cat['id']}")
            cur_s = cat.get("status", "在校")
            s_idx = (CAT_STATUS_OPTIONS.index(cur_s)
                     if cur_s in CAT_STATUS_OPTIONS else 0)
            e_status = ec3.selectbox("状态", CAT_STATUS_OPTIONS, index=s_idx,
                                     key=f"es_{cat['id']}")
            ec4, ec5 = st.columns(2)
            e_neutered = ec4.checkbox("已绝育", cat.get("neutered", False),
                                      key=f"en2_{cat['id']}")
            e_vaccine = ec5.checkbox("已免疫", cat.get("vaccine", False),
                                     key=f"ev_{cat['id']}")
            e_area = st.text_input("区域", cat.get("area", ""), key=f"earea_{cat['id']}")
            e_desc = st.text_area("简介", cat.get("description", ""),
                                  key=f"ed_{cat['id']}")
            if st.button("💾 保存修改", key=f"save_{cat['id']}"):
                result = api.update_cat(cat["id"], {
                    "name": e_name, "age": e_age, "status": e_status,
                    "neutered": e_neutered, "vaccine": e_vaccine,
                    "area": e_area, "description": e_desc,
                })
                if result and "error" not in result:
                    st.success(f"{e_name} 已更新！")
                    st.rerun()


def _tab_content():
    st.markdown("### 🛡️ 内容管理")
    st.markdown("**💬 评论管理**")
    for cmt in api.list_comments():
        c1, c2, c3 = st.columns([4, 1, 1])
        c1.markdown(f"**{cmt.get('username','')}** → 🐱{cmt.get('cat_name','')}: "
                    f"{cmt.get('content','')[:50]}...")
        c2.markdown(f"❤️ {cmt.get('likes', 0)}")
        if c3.button("🗑️", key=f"ad_dc_{cmt['id']}"):
            api.delete_comment(cmt["id"])
            st.success("已删除")
            st.rerun()

    st.markdown("---")
    st.markdown("**🆘 求助管理**")
    pending = [r for r in api.list_rescues() if r.get("status") != "已处理"]
    if pending:
        for r in pending:
            st.markdown(f"🆘 #{r.get('id','')} {r.get('description','')[:60]}...")
            note = st.text_input("处理备注", key=f"ad_rn_{r['id']}")
            if st.button("标记已处理", key=f"ad_rp_{r['id']}"):
                api.resolve_rescue(r["id"], note)
                st.rerun()
    else:
        st.info("暂无待处理")