"""个人中心"""
import streamlit as st

from api_client import api
from utils import (
    is_logged_in, current_user_id,
    format_time, render_cat_card_html,
    # ❌ 移除了未使用的 current_username
)
from config import PAGE_DETAIL, ROLE_LABELS_SHORT, AVATAR_OPTIONS


def page_profile():
    st.markdown("## 👤 个人中心")
    if not is_logged_in():
        st.warning("请先登录 🔑")
        return

    me = api.get_me()
    if not me:
        st.error("获取用户信息失败")
        return
    st.session_state["user_info"] = me

    _render_user_card(me)

    tab1, tab2, tab3, tab4 = st.tabs(
        ["❤️ 我的收藏", "💬 我的评论", "🍚 我的打卡", "⚙️ 修改信息"])
    with tab1:
        _tab_favorites()
    with tab2:
        _tab_my_comments(me)
    with tab3:
        _tab_my_feedings()
    with tab4:
        _tab_settings(me)


def _render_user_card(u: dict):
    st.markdown(f"""
    <div class="cat-card" style="text-align:left;display:flex;align-items:center;gap:24px;">
        <div style="font-size:64px;">{u.get('avatar','👤')}</div>
        <div>
            <h2 style="margin:0;">{u.get('nickname','')}</h2>
            <p style="color:#888;margin:4px 0;">用户名: {u.get('username','')}</p>
            <p style="color:#888;margin:4px 0;">角色:
                <span class="badge badge-neutered">
                    {ROLE_LABELS_SHORT.get(u.get('role','user'),'用户')}</span></p>
            <p style="color:#bbb;font-size:0.85em;">
                📅 注册: {format_time(u.get('created_at',''))}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _tab_favorites():
    fav_cats = api.my_favorites()
    if not fav_cats:
        st.info("还没有收藏猫猫，去图鉴里收藏吧 ❤️")
        return
    cols = st.columns(min(4, len(fav_cats)))
    for i, cat in enumerate(fav_cats):
        with cols[i % 4]:
            st.markdown(render_cat_card_html(cat), unsafe_allow_html=True)
            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("📖 查看", key=f"pf_{cat['id']}",
                             use_container_width=True):
                    st.session_state.detail_cat = cat["id"]
                    st.session_state.page = PAGE_DETAIL
                    st.rerun()
            with bc2:
                if st.button("💔 取消", key=f"pf_unfav_{cat['id']}",
                             use_container_width=True):
                    api.remove_favorite(cat["id"])
                    st.rerun()


def _tab_my_comments(me: dict):
    all_cmts = api.list_comments()
    my_username = me.get("username", "")
    my_cmts = [c for c in all_cmts if c.get("username") == my_username]
    if not my_cmts:
        st.info("还没有发表过评论")
        return
    for c in my_cmts:
        st.markdown(f"""
        <div class="comment-card">
            <p style="color:#e91e63;font-weight:700;margin:0;">
                🐱 {c.get('cat_name','')}</p>
            <p style="margin:6px 0;">{c.get('content','')}</p>
            <p style="color:#bbb;font-size:0.82em;">
                📅 {format_time(c.get('created_at',''))} · ❤️ {c.get('likes',0)}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🗑️ 删除评论", key=f"pf_del_cmt_{c['id']}"):
            api.delete_comment(c["id"])
            st.rerun()


def _tab_my_feedings():
    uid = current_user_id()
    feeds = api.list_feedings(user_id=uid) if uid else []
    if not feeds:
        st.info("还没有投喂记录，去喂猫打卡吧 🍚")
        return
    st.markdown(f"📊 累计投喂 **{len(feeds)}** 次")
    for f in feeds:
        st.markdown(f"""
        <div class="timeline-item">
            <span class="timeline-date">{format_time(f.get('created_at',''))}</span>
            🐱 {f.get('cat_name','')} · 📍 {f.get('location','')}
            · 🍽️ {f.get('food','')}
        </div>
        """, unsafe_allow_html=True)


def _tab_settings(me: dict):
    new_nick = st.text_input("昵称", value=me.get("nickname", ""), key="edit_nick")
    cur_avatar = me.get("avatar", "👤")
    idx = AVATAR_OPTIONS.index(cur_avatar) if cur_avatar in AVATAR_OPTIONS else 0
    new_avatar = st.selectbox("头像", AVATAR_OPTIONS, index=idx, key="edit_avatar")

    if st.button("💾 保存基本信息", use_container_width=True):
        result = api.update_me(nickname=new_nick, avatar=new_avatar)
        if result and "error" not in result:
            st.session_state["user_info"] = result
            st.success("信息已更新！")
            st.rerun()
        else:
            st.error(f"更新失败: {result.get('error','')}")

    st.markdown("---")
    st.markdown("**🔒 修改密码**")
    old_pwd = st.text_input("当前密码", type="password", key="old_pwd")
    new_pwd = st.text_input("新密码", type="password", key="new_pwd")
    new_pwd2 = st.text_input("确认新密码", type="password", key="new_pwd2")
    if st.button("🔐 修改密码", use_container_width=True):
        if not old_pwd or not new_pwd:
            st.warning("请填写完整")
        elif new_pwd != new_pwd2:
            st.error("两次密码不一致")
        else:
            result = api.change_password(old_pwd, new_pwd)
            if result and "error" not in result:
                st.success("密码修改成功！")
            else:
                st.error(f"修改失败: {result.get('error','')}")