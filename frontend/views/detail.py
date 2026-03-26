"""猫猫详情页"""
import streamlit as st

from api_client import api
from utils import (
    is_logged_in, is_admin, current_username,
    status_badge, format_time, ensure_list,
    render_comment_html, render_reply_html,
    # ❌ 移除了未使用的 render_timeline_item
)
from config import PAGE_CATALOG, EVENT_TYPES, API_BASE_URL


def page_detail():
    cid = st.session_state.get("detail_cat")
    if not cid:
        st.warning("请从猫猫图鉴选择一只猫猫查看")
        if st.button("← 返回图鉴"):
            st.session_state.page = PAGE_CATALOG
            st.rerun()
        return

    cat = api.get_cat(cid)
    if not cat:
        st.error("猫猫不存在或无法连接后端")
        if st.button("← 返回图鉴"):
            st.session_state.page = PAGE_CATALOG
            st.rerun()
        return

    if st.button("← 返回图鉴"):
        st.session_state.page = PAGE_CATALOG
        st.rerun()

    _render_header(cat)

    tabs = st.tabs(["📋 基本信息", "📸 相册", "⏳ 事件时间线",
                     "🔗 关系图谱", "💬 评论", "🍚 投喂记录"])
    with tabs[0]:
        _tab_basic_info(cat)
    with tabs[1]:
        _tab_photos(cat, cid)
    with tabs[2]:
        _tab_events(cat, cid)
    with tabs[3]:
        _tab_relations(cat)
    with tabs[4]:
        _tab_comments(cid)
    with tabs[5]:
        _tab_feedings(cid)


def _render_header(cat: dict):
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")
    gender = cat.get("gender", "")
    h1, h2 = st.columns([1, 2])
    with h1:
        st.markdown(f"""
        <div style="text-align:center;padding:20px;">
            <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);
                 width:160px;height:160px;font-size:80px;line-height:160px;">{emoji}</div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        g_cls = "male" if "公" in gender else "female"
        badges = status_badge(cat.get("status", ""))
        nb = ('<span class="badge badge-neutered">✅ 已绝育</span>' if cat.get("neutered")
              else '<span class="badge" style="background:#fff3e0;color:#e65100;">❌ 未绝育</span>')
        vb = '<span class="badge badge-vaccine">💉 已免疫</span>' if cat.get("vaccine") else ''
        st.markdown(f"""
        <div style="padding:10px 0;">
            <h1 style="margin:0;color:#333;">{cat.get('name','')} {emoji}</h1>
            <div style="margin:10px 0;">
                <span class="badge badge-{g_cls}">{gender}</span> {badges} {nb} {vb}
            </div>
            <p style="color:#666;font-size:1.05em;margin-top:12px;">{cat.get('description','')}</p>
        </div>
        """, unsafe_allow_html=True)


def _tab_basic_info(cat: dict):
    personality = ensure_list(cat.get("personality", []))
    info_items = [
        ("🎂 年龄", cat.get("age", "")),
        ("🐾 品种", cat.get("breed", "")),
        ("🎨 毛色", cat.get("fur", "")),
        ("📍 常出没", cat.get("area", "")),
        ("✂️ 绝育", "是" if cat.get("neutered") else "否"),
        ("💉 疫苗", "已接种" if cat.get("vaccine") else "未接种"),
        ("🐛 驱虫", "已驱虫" if cat.get("deworm") else "未驱虫"),
        ("💕 性格", "、".join(personality)),
    ]
    cols = st.columns(3)
    for idx, (label, val) in enumerate(info_items):
        cols[idx % 3].markdown(f"""
        <div class="info-panel">
            <b style="color:#e91e63;">{label}</b><br/>
            <span style="font-size:1.1em;">{val}</span>
        </div>
        """, unsafe_allow_html=True)


def _tab_photos(cat: dict, cid: int):
    st.markdown("#### 📸 猫猫相册")
    photos = cat.get("photos", [])
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")

    if photos:
        pcols = st.columns(4)
        for idx, photo in enumerate(photos):
            with pcols[idx % 4]:
                img_url = f"{API_BASE_URL}/{photo.get('file_path','')}"
                st.image(img_url, caption=photo.get("caption", ""),
                         use_container_width=True)
    else:
        pcols = st.columns(4)
        for idx, m in enumerate(["😺 晒太阳", "😸 吃饭中", "😻 被摸头", "😽 打哈欠"]):
            pcols[idx].markdown(f"""
            <div style="background:linear-gradient(135deg,{color}22,{color}44);
                        border-radius:16px;padding:40px 10px;text-align:center;
                        border:2px dashed {color}66;margin:5px 0;">
                <span style="font-size:48px;">{emoji}</span>
                <p style="color:#888;margin-top:8px;">{m}</p>
            </div>
            """, unsafe_allow_html=True)

    if is_logged_in():
        st.markdown("---")
        uploaded = st.file_uploader("📤 上传照片", type=["jpg", "png", "jpeg"],
                                    accept_multiple_files=True, key=f"upload_{cid}")
        if uploaded:
            caption = st.text_input("照片说明", key=f"caption_{cid}")
            if st.button("上传", key=f"do_upload_{cid}"):
                for f in uploaded:
                    result = api.upload_cat_photo(cid, f, caption)
                    if result and "error" not in result:
                        st.success(f"{f.name} 上传成功！")
                    else:
                        st.error("上传失败")
                st.rerun()


def _tab_events(cat: dict, cid: int):
    st.markdown("#### ⏳ 事件时间线")
    events = cat.get("events", [])
    if events:
        for ev in events:
            st.markdown(f"""
            <div class="timeline-item">
                <span class="timeline-date">{ev.get('event_date','')}</span>
                <b>{ev.get('event_type','')}</b>&nbsp;&nbsp;{ev.get('description','')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("暂无记录")

    if is_admin():
        st.markdown("---")
        st.markdown("**➕ 添加新事件**")
        ec1, ec2 = st.columns(2)
        ev_date = ec1.date_input("日期", key=f"ev_d_{cid}")
        ev_type = ec2.selectbox("类型", EVENT_TYPES, key=f"ev_t_{cid}")
        ev_desc = st.text_input("描述", key=f"ev_s_{cid}")
        if st.button("添加事件", key=f"ev_add_{cid}"):
            if ev_desc:
                result = api.add_cat_event(cid, str(ev_date), ev_type, ev_desc)
                if result and "error" not in result:
                    st.success("事件已添加！")
                    st.rerun()


def _tab_relations(cat: dict):
    st.markdown("#### 🔗 社交关系图谱")
    relations = cat.get("relations", [])
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")
    if not relations:
        st.info("该猫猫暂无已知社交关系记录")
        return
    for rel in relations:
        rel_cat = api.get_cat(rel.get("related_cat_id"))
        r_emoji = rel_cat.get("emoji", "🐱") if rel_cat else "🐱"
        st.markdown(f"""
        <div style="text-align:center;margin:15px 0;">
            <span class="relation-node" style="border-color:{color}">{emoji}</span>
            <span class="relation-line">—— {rel.get('relation_type','')} ——</span>
            <span class="relation-node">{r_emoji}</span>
            <br/>
            <span style="color:#888;font-size:0.9em;">
                {cat.get('name','')}  ↔  {rel.get('related_cat_name','')}</span>
        </div>
        """, unsafe_allow_html=True)


def _tab_comments(cid: int):
    st.markdown("#### 💬 大家的评论")
    comments = api.list_comments(cat_id=cid)
    if comments:
        for cmt in comments:
            st.markdown(render_comment_html(
                cmt.get("username", ""), format_time(cmt.get("created_at", "")),
                cmt.get("content", ""), cmt.get("likes", 0)
            ), unsafe_allow_html=True)

            for rep in cmt.get("replies", []):
                st.markdown(render_reply_html(
                    rep.get("username", ""), format_time(rep.get("created_at", "")),
                    rep.get("content", "")
                ), unsafe_allow_html=True)

            if is_logged_in():
                bc1, bc2, _ = st.columns([1, 1, 4])
                with bc1:
                    if st.button("❤️ 赞", key=f"like_{cmt['id']}_{cid}"):
                        api.like_comment(cmt["id"])
                        st.rerun()
                with bc2:
                    if current_username() == cmt.get("username") or is_admin():
                        if st.button("🗑️", key=f"delc_{cmt['id']}_{cid}"):
                            api.delete_comment(cmt["id"])
                            st.rerun()
                with st.expander("💬 回复", expanded=False):
                    reply_text = st.text_input("回复内容", key=f"reply_{cmt['id']}_{cid}")
                    if st.button("发送", key=f"reply_btn_{cmt['id']}_{cid}"):
                        if reply_text:
                            api.reply_comment(cmt["id"], reply_text)
                            st.success("回复成功！")
                            st.rerun()
            st.markdown("")
    else:
        st.info("还没有评论，快来抢沙发吧！🐾")

    if is_logged_in():
        st.markdown("---")
        st.markdown("**✍️ 发表评论**")
        new_cmt = st.text_area("说点什么吧～", key=f"new_cmt_{cid}")
        if st.button("发布评论 🐾", key=f"post_cmt_{cid}"):
            if new_cmt.strip():
                result = api.create_comment(cid, new_cmt.strip())
                if result and "error" not in result:
                    st.success("评论发布成功！🎉")
                    st.rerun()
            else:
                st.warning("评论不能为空哦～")
    else:
        st.info("登录后即可发表评论 💬")


def _tab_feedings(cid: int):
    st.markdown("#### 🍚 投喂记录")
    feeds = api.list_feedings(cat_id=cid)
    if feeds:
        for fd in feeds:
            st.markdown(f"""
            <div class="timeline-item">
                <span class="timeline-date">🕐 {format_time(fd.get('created_at',''))}</span>
                👤 {fd.get('username','')} · 📍 {fd.get('location','')} · 🍽️ {fd.get('food','')}
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"\n📊 累计被投喂 **{len(feeds)}** 次")
    else:
        st.info("暂无投喂记录")