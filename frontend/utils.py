"""工具函数 & HTML 渲染组件"""
from __future__ import annotations

import streamlit as st
from typing import Optional


# ════════════════════════════════
# 用户状态判断
# ════════════════════════════════

def is_logged_in() -> bool:
    return st.session_state.get("token") is not None


def current_user() -> Optional[dict]:
    return st.session_state.get("user_info")


def current_user_id() -> Optional[int]:
    u = current_user()
    return u["id"] if u else None


def current_username() -> str:
    u = current_user()
    return u["username"] if u else ""


def is_admin() -> bool:
    u = current_user()
    return u is not None and u.get("role") == "admin"


# ════════════════════════════════
# 格式化
# ════════════════════════════════

def format_time(t) -> str:
    if not t:
        return ""
    return str(t)[:16]


def ensure_list(val) -> list:
    """确保值是列表"""
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        return [val]
    return []


# ════════════════════════════════
# HTML 渲染组件
# ════════════════════════════════

def status_badge(s: str) -> str:
    m = {"在校": "school", "走失": "lost", "待收养": "adopt",
         "已收养": "adopted", "回喵星": "star"}
    cls = m.get(s, "school")
    return f'<span class="badge badge-{cls}">{s}</span>'


def render_cat_card_html(cat: dict) -> str:
    badges = status_badge(cat.get("status", "在校"))
    if cat.get("neutered"):
        badges += ' <span class="badge badge-neutered">✅ 已绝育</span>'
    gender = cat.get("gender", "")
    g_cls = "male" if "公" in gender else "female"
    badges = f'<span class="badge badge-{g_cls}">{gender}</span> ' + badges
    color = cat.get("color", "#FF8C00")
    emoji = cat.get("emoji", "🐱")
    personality = ensure_list(cat.get("personality", []))
    return f"""
    <div class="cat-card">
        <div class="cat-avatar" style="background:linear-gradient(135deg,{color}33,{color}66);">
            {emoji}
        </div>
        <h3 style="margin:8px 0 4px;color:#333;">{cat.get('name','')}</h3>
        <p style="color:#999;font-size:0.9em;margin:2px 0;">
            {cat.get('breed','中华田园猫')} · {cat.get('age','')}</p>
        <div style="margin:8px 0;">{badges}</div>
        <p style="color:#666;font-size:0.88em;">📍 {cat.get('area','')}</p>
        <p style="color:#888;font-size:0.85em;margin-top:6px;">{'、'.join(personality)}</p>
    </div>
    """


def render_stat_card(icon: str, number: str, label: str) -> str:
    return f"""
    <div class="stat-card">
        <div style="font-size:2em;">{icon}</div>
        <div class="stat-number">{number}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def render_timeline_item(date: str, content: str) -> str:
    return f"""
    <div class="timeline-item">
        <span class="timeline-date">🕐 {date}</span>
        <span>{content}</span>
    </div>
    """


def render_comment_html(username: str, time: str, content: str, likes: int) -> str:
    return f"""
    <div class="comment-card">
        <b>👤 {username}</b>
        <span style="color:#bbb;font-size:0.82em;">· {time}</span>
        <p style="margin:8px 0;">{content}</p>
        <span style="color:#e91e63;">❤️ {likes}</span>
    </div>
    """


def render_reply_html(username: str, time: str, content: str) -> str:
    return f"""
    <div style="margin-left:30px;background:#fef9ff;border-radius:10px;
                padding:10px 14px;border-left:3px solid #f48fb1;margin-bottom:5px;">
        <b>👤 {username}</b>
        <span style="color:#bbb;font-size:0.82em;">· {time}</span>
        <p style="margin:4px 0;">{content}</p>
    </div>
    """


def render_announce_html(title: str, content: str, time: str,
                         author: str = "") -> str:
    author_text = f" · ✍️ {author}" if author else ""
    return f"""
    <div class="announce-card">
        <h3 style="margin:0 0 8px;">{title}</h3>
        <p style="color:#555;margin:0;line-height:1.7;">{content}</p>
        <p style="color:#bbb;font-size:0.82em;margin-top:10px;">📅 {time}{author_text}</p>
    </div>
    """