"""
API Client — 封装所有后端 HTTP 请求
Streamlit 前端通过此模块与 FastAPI 后端通信
"""
import requests
from typing import Optional, List
import streamlit as st

BASE_URL = "http://localhost:8000"


class ApiClient:
    """与后端通信的统一客户端"""

    def __init__(self):
        self.base = BASE_URL

    @property
    def token(self) -> Optional[str]:
        return st.session_state.get("token")

    @property
    def headers(self) -> dict:
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _get(self, path: str, params: dict = None) -> dict | list | None:
        try:
            r = requests.get(f"{self.base}{path}", headers=self.headers,
                             params=params, timeout=10)
            if r.status_code == 200:
                return r.json()
            return None
        except requests.ConnectionError:
            st.error("⚠️ 无法连接到后端服务，请确认 FastAPI 已启动")
            return None

    def _post(self, path: str, data: dict = None, files=None) -> dict | None:
        try:
            if files:
                headers = {}
                if self.token:
                    headers["Authorization"] = f"Bearer {self.token}"
                r = requests.post(f"{self.base}{path}", headers=headers,
                                  data=data, files=files, timeout=30)
            else:
                r = requests.post(f"{self.base}{path}", headers=self.headers,
                                  json=data, timeout=10)
            return r.json() if r.status_code in (200, 201) else {"error": r.json().get("detail", "请求失败")}
        except requests.ConnectionError:
            return {"error": "无法连接后端"}

    def _put(self, path: str, data: dict = None) -> dict | None:
        try:
            r = requests.put(f"{self.base}{path}", headers=self.headers, json=data, timeout=10)
            return r.json() if r.status_code == 200 else {"error": r.json().get("detail", "请求失败")}
        except requests.ConnectionError:
            return {"error": "无法连接后端"}

    def _delete(self, path: str) -> dict | None:
        try:
            r = requests.delete(f"{self.base}{path}", headers=self.headers, timeout=10)
            return r.json() if r.status_code == 200 else None
        except requests.ConnectionError:
            return None

    # ════════════════════════════════
    #  认证
    # ════════════════════════════════
    def login(self, username: str, password: str) -> dict:
        return self._post("/api/auth/login", {"username": username, "password": password})

    def register(self, username: str, password: str, nickname: str = "") -> dict:
        return self._post("/api/auth/register",
                          {"username": username, "password": password, "nickname": nickname})

    def get_me(self) -> dict | None:
        return self._get("/api/auth/me")

    def update_me(self, nickname: str = None, avatar: str = None) -> dict:
        data = {}
        if nickname is not None: data["nickname"] = nickname
        if avatar is not None: data["avatar"] = avatar
        return self._put("/api/auth/me", data)

    def change_password(self, old_password: str, new_password: str) -> dict:
        return self._post("/api/auth/change-password",
                          {"old_password": old_password, "new_password": new_password})

    # ════════════════════════════════
    #  猫猫
    # ════════════════════════════════
    def list_cats(self, name=None, gender=None, status=None, neutered=None) -> list:
        params = {}
        if name: params["name"] = name
        if gender and gender != "全部": params["gender"] = gender
        if status and status != "全部": params["status"] = status
        if neutered is not None and neutered != "全部":
            params["neutered"] = neutered == "已绝育"
        return self._get("/api/cats", params) or []

    def get_cat(self, cat_id: int) -> dict | None:
        return self._get(f"/api/cats/{cat_id}")

    def random_cats(self, count: int = 4) -> list:
        return self._get("/api/cats/random", {"count": count}) or []

    def create_cat(self, data: dict) -> dict:
        return self._post("/api/cats", data)

    def update_cat(self, cat_id: int, data: dict) -> dict:
        return self._put(f"/api/cats/{cat_id}", data)

    def add_cat_event(self, cat_id: int, event_date: str,
                      event_type: str, description: str) -> dict:
        return self._post(f"/api/cats/{cat_id}/events",
                          {"event_date": event_date, "event_type": event_type,
                           "description": description})

    def upload_cat_photo(self, cat_id: int, file, caption: str = "") -> dict:
        return self._post(f"/api/cats/{cat_id}/photos",
                          data={"caption": caption},
                          files={"file": (file.name, file.read(), file.type)})

    # ════════════════════════════════
    #  评论
    # ════════════════════════════════
    def list_comments(self, cat_id: int = None) -> list:
        params = {}
        if cat_id: params["cat_id"] = cat_id
        return self._get("/api/comments", params) or []

    def create_comment(self, cat_id: int, content: str) -> dict:
        return self._post("/api/comments", {"cat_id": cat_id, "content": content})

    def like_comment(self, comment_id: int) -> dict:
        return self._post(f"/api/comments/{comment_id}/like")

    def reply_comment(self, comment_id: int, content: str) -> dict:
        return self._post(f"/api/comments/{comment_id}/reply", {"content": content})

    def delete_comment(self, comment_id: int) -> dict:
        return self._delete(f"/api/comments/{comment_id}")

    # ════════════════════════════════
    #  投喂打卡
    # ════════════════════════════════
    def list_feedings(self, cat_id: int = None, user_id: int = None, limit: int = 50) -> list:
        params = {"limit": limit}
        if cat_id: params["cat_id"] = cat_id
        if user_id: params["user_id"] = user_id
        return self._get("/api/feedings", params) or []

    def create_feeding(self, cat_id: int, location: str, food: str) -> dict:
        return self._post("/api/feedings",
                          {"cat_id": cat_id, "location": location, "food": food})

    def feeding_stats(self) -> list:
        return self._get("/api/feedings/stats") or []

    # ════════════════════════════════
    #  寻猫启事
    # ════════════════════════════════
    def list_lost(self) -> list:
        return self._get("/api/lost") or []

    def create_lost(self, cat_name: str, description: str, location: str) -> dict:
        return self._post("/api/lost",
                          {"cat_name": cat_name, "description": description, "location": location})

    def mark_found(self, notice_id: int, found_note: str = "") -> dict:
        return self._put(f"/api/lost/{notice_id}/found", {"found_note": found_note})

    # ════════════════════════════════
    #  领养
    # ════════════════════════════════
    def list_adoptions(self) -> list:
        return self._get("/api/adoptions") or []

    def create_adoption(self, cat_id: int, reason: str, contact: str) -> dict:
        return self._post("/api/adoptions",
                          {"cat_id": cat_id, "reason": reason, "contact": contact})

    def review_adoption(self, app_id: int, status: str) -> dict:
        return self._put(f"/api/adoptions/{app_id}/review", {"status": status})

    # ════════════════════════════════
    #  救助
    # ════════════════════════════════
    def list_rescues(self) -> list:
        return self._get("/api/rescues") or []

    def create_rescue(self, location: str, description: str) -> dict:
        return self._post("/api/rescues", {"location": location, "description": description})

    def resolve_rescue(self, rescue_id: int, note: str = "") -> dict:
        return self._put(f"/api/rescues/{rescue_id}/resolve", {"note": note})

    # ════════════════════════════════
    #  公告
    # ════════════════════════════════
    def list_announcements(self) -> list:
        return self._get("/api/announcements") or []

    def create_announcement(self, title: str, content: str) -> dict:
        return self._post("/api/announcements", {"title": title, "content": content})

    def delete_announcement(self, ann_id: int) -> dict:
        return self._delete(f"/api/announcements/{ann_id}")

    # ════════════════════════════════
    #  收藏
    # ════════════════════════════════

    def my_favorites(self) -> list:
        return self._get("/api/favorites") or []

    def add_favorite(self, cat_id: int) -> dict:
        return self._post(f"/api/favorites/{cat_id}")

    def remove_favorite(self, cat_id: int) -> dict:
        return self._delete(f"/api/favorites/{cat_id}")

    def check_favorite(self, cat_id: int) -> bool:
        r = self._get(f"/api/favorites/check/{cat_id}")
        return r.get("favorited", False) if r else False

    # ════════════════════════════════
    #  领养回访
    # ════════════════════════════════
    def list_followups(self) -> list:
        return self._get("/api/followups") or []

    def create_followup(self, cat_id: int, content: str, status: str = "良好") -> dict:
        return self._post("/api/followups",
                          {"cat_id": cat_id, "content": content, "status": status})

    # ════════════════════════════════
    #  管理后台
    # ════════════════════════════════
    def admin_stats(self) -> dict | None:
        return self._get("/api/admin/stats")

    def admin_users(self) -> list:
        return self._get("/api/admin/users") or []

    def admin_update_role(self, user_id: int, role: str) -> dict:
        return self._put(f"/api/admin/users/{user_id}/role", {"role": role})

    def admin_backup(self) -> dict | None:
        return self._get("/api/admin/backup")


# 全局单例
api = ApiClient()