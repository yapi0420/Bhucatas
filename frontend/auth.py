"""侧边栏登录 / 注册组件"""
import streamlit as st
from api_client import api
from utils import is_logged_in, current_user
from config import ROLE_LABELS


def render_auth_sidebar():
    """渲染侧边栏的登录/注册/用户信息区域"""
    if is_logged_in():
        _render_user_info()
    else:
        _render_login_register()


def _render_user_info():
    """已登录 → 显示用户信息 + 退出按钮"""
    u = current_user()
    st.sidebar.markdown(f"""
    <div style="background:white;border-radius:16px;padding:16px;text-align:center;
                box-shadow:0 2px 10px rgba(0,0,0,0.06);margin-bottom:10px;">
        <div style="font-size:40px;">{u.get('avatar','👤')}</div>
        <p style="font-weight:700;margin:6px 0;">{u.get('nickname','')}</p>
        <p style="color:#999;font-size:0.82em;">
            {ROLE_LABELS.get(u.get('role','user'), '用户')}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("🚪 退出登录", use_container_width=True):
        for key in ["token", "user_info"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


def _render_login_register():
    """未登录 → 登录 / 注册 / 找回密码"""
    st.sidebar.markdown("### 🔐 登录 / 注册")
    mode = st.sidebar.radio(
        "auth_mode", ["登录", "注册", "找回密码"],
        horizontal=True, label_visibility="collapsed"
    )

    if mode == "登录":
        _do_login()
    elif mode == "注册":
        _do_register()
    else:
        st.sidebar.info("请联系管理员重置密码\n📧 catadmin@beihua.edu.cn")


def _do_login():
    u = st.sidebar.text_input("用户名", key="login_u")
    p = st.sidebar.text_input("密码", type="password", key="login_p")
    if st.sidebar.button("🐾 登录", use_container_width=True):
        if not u or not p:
            st.sidebar.error("请输入用户名和密码")
            return
        result = api.login(u, p)
        if "error" in result:
            st.sidebar.error(result["error"])
        else:
            st.session_state["token"] = result["access_token"]
            st.session_state["user_info"] = result["user"]
            st.sidebar.success(f"欢迎回来，{result['user'].get('nickname','')}！")
            st.rerun()
    st.sidebar.caption("测试: admin/admin123 · demo/demo123")


def _do_register():
    nu = st.sidebar.text_input("用户名", key="reg_u")
    nn = st.sidebar.text_input("昵称", key="reg_n")
    np1 = st.sidebar.text_input("密码", type="password", key="reg_p1")
    np2 = st.sidebar.text_input("确认密码", type="password", key="reg_p2")
    if st.sidebar.button("📝 注册", use_container_width=True):
        if not nu or not np1:
            st.sidebar.error("请填写完整信息")
        elif np1 != np2:
            st.sidebar.error("两次密码不一致")
        elif len(np1) < 4:
            st.sidebar.error("密码至少4位")
        else:
            result = api.register(nu, np1, nn)
            if "error" in result:
                st.sidebar.error(result["error"])
            else:
                st.session_state["token"] = result["access_token"]
                st.session_state["user_info"] = result["user"]
                st.sidebar.success("注册成功！已自动登录 🎉")
                st.rerun()