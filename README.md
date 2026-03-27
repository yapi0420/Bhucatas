<div align="center">

# 🐾 北华大学猫猫校园

### Campus Cat — 校园流浪猫信息管理与互动平台

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*用爱守护每一只校园猫咪 · 记录每一个温暖的故事*

---

[功能特性](#-功能特性) •
[项目架构](#-项目架构) •
[快速开始](#-快速开始) •
[API 文档](#-api-文档) •
[页面展示](#-页面展示) •
[开发指南](#-开发指南)

</div>

---

## 📖 项目简介

**北华大学猫猫校园** 是一个面向高校的校园流浪猫信息管理与社区互动平台。平台致力于为校园流浪猫建立完整的数字化档案，方便师生了解、关注和帮助这些可爱的小生命。

平台采用 **前后端分离架构**，前端使用 **Streamlit** 构建精美可爱的用户界面，后端使用 **FastAPI** 提供高性能 RESTful API 服务，数据层支持 **SQLite / MySQL / PostgreSQL** 多种数据库。

### 🎯 核心理念

- 🐱 **为每只猫建档** — 姓名、照片、性格、健康状态、社交关系，一只都不少
- 🍚 **记录每份爱心** — 喂猫打卡、投喂统计，让爱心看得见
- 🏠 **促进科学领养** — 领养申请 → 审核 → 回访，全流程跟踪
- 🆘 **快速救助响应** — 发现受伤猫咪一键求助，爱心接力

---

## ✨ 功能特性

### 一、猫猫图鉴模块（核心）

| 功能 | 描述 |
|------|------|
| 📋 基础信息 | 图片、性别、年龄、绝育状态、收养状态、性格、社交关系 |
| ✏️ 信息维护 | 支持猫猫信息的新增、修改、动态更新 |
| 🎨 扩展信息 | 常出没区域、毛色特征、疫苗/驱虫状态 |
| 🏷️ 状态标签 | 在校、走失、待收养、已收养、回喵星 |
| 📸 多图相册 | 支持上传生活照、成长照 |
| ⏳ 事件时间线 | 记录救助、绝育、走失、收养等关键历程 |
| 🔗 关系图谱 | 可视化展示母子、同伴、冤家等社交关系 |
| 🔍 搜索筛选 | 按名字、性别、区域、绝育/收养状态筛选查找 |

### 二、用户系统模块

| 功能 | 描述 |
|------|------|
| 🔐 账号基础 | 用户名、密码（bcrypt 加密 + JWT 令牌） |
| 📝 核心操作 | 注册、登录、找回密码 |
| 👥 权限分级 | 游客（仅浏览）、普通用户、认证喂猫/救助人、管理员 |
| 👤 个人中心 | 个人信息、我的评论、我的收藏、我的打卡记录 |
| ⚙️ 账号管理 | 修改个人信息、重置密码 |

### 三、评论互动模块

| 功能 | 描述 |
|------|------|
| 💬 发布评论 | 支持文字发布 |
| ❤️ 互动功能 | 评论点赞、楼中楼回复、违规举报 |
| 🗑️ 评论管理 | 用户删除自身评论，管理员删除违规评论 |
| 📄 列表展示 | 按猫猫分页展示所有评论 |

### 四、校园特色功能

| 功能 | 描述 |
|------|------|
| 🍚 喂猫打卡 | 记录投喂时间、地点、对应猫猫，统计投喂频次 |
| 📊 投喂记录 | 查看单只猫猫的历史投喂数据及排行榜 |
| 🔍 寻猫启事 | 发布走失信息，支持标记「已找回」 |
| 🏠 领养申请 | 为待收养猫猫提交申请，管理员审核 |
| 🆘 救助求助 | 发布受伤猫猫救助信息 |
| 📝 领养回访 | 已收养猫猫上传近况反馈 |

### 五、通用附加功能

| 功能 | 描述 |
|------|------|
| ❤️ 收藏猫猫 | 收藏/取消收藏，查看个人收藏列表 |
| 📢 校园公告 | 管理员发布平台通知、喂猫规则 |
| 📊 数据统计 | 猫猫总数、在校/收养数量、用户数、投喂总量 |
| 📦 数据备份 | 支持 JSON 格式数据导出备份 |

---

## 🏗️ 项目架构

### 系统架构图

```
┌─────────────────────┐     HTTP/JSON       ┌─────────────────────┐
│                     │                     │                     │
│   Streamlit 前端     │ ◄═══════════════► │   FastAPI 后端        │
│   (端口 8501)        │   requests 调用    │   (端口 8000)        │
│                     │                     │                     │
│  ┌───────────────┐  │                     │  ┌───────────────┐  │
│  │ views/        │  │                     │  │ routers/      │  │
│  │  home.py      │  │                     │  │  auth.py      │  │
│  │  catalog.py   │  │                     │  │  cats.py      │  │
│  │  detail.py    │  │                     │  │  comments.py  │  │
│  │  feeding.py   │  │                     │  │  feedings.py  │  │
│  │  lost.py      │  │                     │  │  lost.py      │  │
│  │  adoption.py  │  │                     │  │  adoptions.py │  │
│  │  rescue.py    │  │                     │  │  ...          │  │
│  │  ...          │  │                     │  └───────┬───────┘  │
│  └───────┬───────┘  │                     │          │          │
│          │          │                     │  ┌───────▼───────┐  │
│  ┌───────▼───────┐  │                     │  │ SQLAlchemy    │  │
│  │ api_client.py │  │                     │  │ ORM Models    │  │
│  └───────────────┘  │                     │  └───────┬───────┘  │
└─────────────────────┘                     │          │          │
                                            │  ┌───────▼───────┐  │
                                            │  │  Database     │  │
                                            │  │  SQLite/MySQL │  │
                                            │  └───────────────┘  │
                                            └─────────────────────┘
```

### 目录结构

```
campus-cat/
│
├── backend/                          # 🔧 后端服务
│   ├── main.py                       # FastAPI 应用入口
│   ├── database.py                   # 数据库连接配置
│   ├── security.py                   # JWT 认证 & 密码加密
│   ├── models.py                     # SQLAlchemy 数据模型
│   ├── schemas.py                    # Pydantic 请求/响应模型
│   ├── deps.py                       # 依赖注入（权限校验）
│   ├── init_data.py                  # 初始化种子数据
│   ├── requirements.txt              # 后端依赖
│   └── routers/                      # API 路由
│       ├── __init__.py
│       ├── auth.py                   # 登录注册
│       ├── cats.py                   # 猫猫 CRUD + 事件/关系/照片
│       ├── comments.py               # 评论（含楼中楼回复）
│       ├── feedings.py               # 投喂打卡 + 统计
│       ├── lost.py                   # 寻猫启事
│       ├── adoptions.py              # 领养申请 + 审核
│       ├── rescues.py                # 救助求助
│       ├── announcements.py          # 校园公告
│       ├── favorites.py              # 收藏
│       ├── followups.py              # 领养回访
│       └── admin.py                  # 管理后台 + 数据统计
│
├── frontend/                         # 🎨 前端界面
│   ├── app.py                        # Streamlit 主入口（~60行）
│   ├── api_client.py                 # API 调用封装
│   ├── config.py                     # 全局配置常量
│   ├── styles.py                     # CSS 样式
│   ├── utils.py                      # 工具函数 & HTML 渲染
│   ├── auth.py                       # 登录注册组件
│   ├── requirements.txt              # 前端依赖
│   ├── .streamlit/                   # Streamlit 配置
│   │   └── config.toml               # 主题配置
│   └── views/                        # 页面模块
│       ├── __init__.py               # 页面注册表
│       ├── home.py                   # 🏠 首页
│       ├── catalog.py                # 🐱 猫猫图鉴
│       ├── detail.py                 # 📖 猫猫详情
│       ├── feeding.py                # 🍚 喂猫打卡
│       ├── lost.py                   # 🔍 寻猫启事
│       ├── adoption.py               # 🏠 领养中心
│       ├── rescue.py                 # 🆘 救助求助
│       ├── comments.py               # 💬 评论广场
│       ├── announcements.py          # 📢 校园公告
│       ├── profile.py                # 👤 个人中心
│       └── admin.py                  # ⚙️ 管理后台
│
└── uploads/                          # 📁 图片上传目录
```

### 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| **前端** | Streamlit | 1.29+ | 响应式 Web 界面 |
| **前端** | Requests | 2.31+ | HTTP API 调用 |
| **前端** | Pandas | 2.1+ | 数据统计图表 |
| **后端** | FastAPI | 0.104+ | RESTful API 服务 |
| **后端** | Uvicorn | 0.24+ | ASGI 服务器 |
| **后端** | SQLAlchemy | 2.0+ | ORM 数据库操作 |
| **后端** | Pydantic | 2.5+ | 数据校验 |
| **认证** | python-jose | 3.3+ | JWT Token |
| **认证** | passlib | 1.7+ | bcrypt 密码加密 |
| **数据库** | SQLite | — | 开发环境（零配置） |
| **数据库** | MySQL | 5.7+ | 生产环境（可选） |

---

## 🚀 快速开始

### 前置条件

- Python 3.10 或更高版本
- pip 包管理器

### 1️⃣ 克隆项目

```bash
git clone https://github.com/your-username/campus-cat.git
cd campus-cat
```

### 2️⃣ 安装后端依赖并启动

```bash
cd backend
pip install -r requirements.txt

# 启动后端（默认端口 8000）
python main.py
```

启动成功后可访问：
- API 服务：http://localhost:8000
- 交互式文档：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc

> 💡 首次启动会自动创建数据库并填充种子数据

### 3️⃣ 安装前端依赖并启动

```bash
# 新开一个终端
cd frontend
pip install -r requirements.txt

# 启动前端（默认端口 8501）
streamlit run app.py
```

启动成功后访问：http://localhost:8501

### 4️⃣ 测试账号

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | `admin` | `admin123` | 全部功能 + 后台管理 |
| 认证喂猫人 | `catfan` | `cat123` | 全部用户功能 |
| 普通用户 | `demo` | `demo123` | 基础功能 |
| 游客 | — | — | 仅浏览 |

---

## 📡 API 文档

启动后端后，访问 http://localhost:8000/docs 查看完整的 Swagger 交互式文档。

### API 概览

| 模块 | 路径前缀 | 主要接口 |
|------|---------|---------|
| 🔐 认证 | `/api/auth` | `POST /login` · `POST /register` · `GET /me` |
| 🐱 猫猫 | `/api/cats` | `GET /` · `GET /{id}` · `POST /` · `PUT /{id}` · `POST /{id}/events` · `POST /{id}/photos` |
| 💬 评论 | `/api/comments` | `GET /` · `POST /` · `POST /{id}/like` · `POST /{id}/reply` · `DELETE /{id}` |
| 🍚 投喂 | `/api/feedings` | `GET /` · `POST /` · `GET /stats` |
| 🔍 寻猫 | `/api/lost` | `GET /` · `POST /` · `PUT /{id}/found` |
| 🏠 领养 | `/api/adoptions` | `GET /` · `POST /` · `PUT /{id}/review` |
| 🆘 救助 | `/api/rescues` | `GET /` · `POST /` · `PUT /{id}/resolve` |
| 📢 公告 | `/api/announcements` | `GET /` · `POST /` · `DELETE /{id}` |
| ❤️ 收藏 | `/api/favorites` | `GET /` · `POST /{cat_id}` · `DELETE /{cat_id}` |
| 📝 回访 | `/api/followups` | `GET /` · `POST /` |
| ⚙️ 管理 | `/api/admin` | `GET /stats` · `GET /users` · `PUT /users/{id}/role` · `GET /backup` |

### 认证方式

所有需要登录的接口使用 **Bearer Token** 认证：

```bash
# 1. 登录获取 Token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# 返回: {"access_token":"eyJ...","token_type":"bearer","user":{...}}

# 2. 使用 Token 访问接口
curl http://localhost:8000/api/cats \
  -H "Authorization: Bearer eyJ..."
```

---

## 🖼️ 页面展示

### 页面导航

| 页面 | 路由 | 权限 | 描述 |
|------|------|------|------|
| 🏠 首页 | 首页 | 全部 | 统计数据、推荐猫猫、最新公告、投喂动态 |
| 🐱 猫猫图鉴 | 图鉴 | 全部 | 猫猫卡片列表、搜索筛选、收藏 |
| 📖 猫猫详情 | 详情 | 全部 | 基本信息、相册、时间线、关系图谱、评论、投喂 |
| 🍚 喂猫打卡 | 打卡 | 登录 | 新建打卡、投喂统计、排行榜 |
| 🔍 寻猫启事 | 寻猫 | 登录发布 | 发布/查看走失信息、标记找回 |
| 🏠 领养中心 | 领养 | 登录申请 | 待收养列表、申请、审核、回访 |
| 🆘 救助求助 | 救助 | 登录发布 | 发布/查看求助、管理员处理 |
| 💬 评论广场 | 评论 | 全部 | 全站评论汇总、点赞、回复 |
| 📢 校园公告 | 公告 | 全部 | 公告列表、管理员发布/删除 |
| 👤 个人中心 | 个人 | 登录 | 收藏、评论、打卡记录、修改信息 |
| ⚙️ 管理后台 | 管理 | 管理员 | 数据统计、用户/猫猫/内容管理、备份 |

---

## 🗄️ 数据库

### 数据模型关系图

```
┌──────────┐    ┌──────────────┐    ┌──────────┐
│  User    │───<│  Comment     │>───│  Cat     │
│          │    │              │    │          │
│  id      │    │  id          │    │  id      │
│  username│    │  user_id     │    │  name    │
│  password│    │  cat_id      │    │  gender  │
│  role    │    │  content     │    │  status  │
│  nickname│    │  likes       │    │  ...     │
└────┬─────┘    └──────┬───────┘    └────┬─────┘
     │                 │                 │
     │    ┌────────────┘                 │
     │    │                              │
     ├───<│ CommentReply                 ├───< CatEvent
     │    │                              │
     ├───<│ Feeding ─────────────────>───┤
     │    │                              ├───< CatRelation
     ├───<│ Favorite ────────────────>───┤
     │    │                              ├───< CatPhoto
     ├───<│ LostNotice                   │
     │    │                              │
     ├───<│ AdoptionApplication ─────>───┤
     │    │                              │
     ├───<│ Rescue                       │
     │    │                              │
     ├───<│ Announcement                 │
     │    │                              │
     └───<│ Followup ────────────────>───┘
```

### 切换数据库

编辑 `backend/database.py`：

```python
# SQLite（开发环境，默认）
DATABASE_URL = "sqlite:///./campus_cat.db"

# MySQL（生产环境）
DATABASE_URL = "mysql+pymysql://user:password@localhost:3306/campus_cat?charset=utf8mb4"

# PostgreSQL
DATABASE_URL = "postgresql://user:password@localhost:5432/campus_cat"
```

---

## 🛠️ 开发指南

### 前端新增页面（3 步完成）

```python
# 1. 新建 frontend/views/new_page.py
import streamlit as st
from api_client import api
from utils import is_logged_in

def page_new():
    st.markdown("## 🆕 新页面")
    st.write("页面内容...")
```

```python
# 2. 在 frontend/views/__init__.py 注册
from .new_page import page_new

PAGE_REGISTRY["🆕 新功能"] = page_new
```

```python
# 3. 在 frontend/config.py 添加到导航
NAV_PAGES = [
    ...
    "🆕 新功能",
]
```

### 后端新增 API（3 步完成）

```python
# 1. 在 backend/models.py 添加数据模型（如需要）
class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    ...
```

```python
# 2. 新建 backend/routers/new_router.py
from fastapi import APIRouter, Depends
router = APIRouter(prefix="/api/new", tags=["新模块"])

@router.get("")
def list_items():
    return [...]
```

```python
# 3. 在 backend/main.py 注册路由
from routers import new_router
app.include_router(new_router.router)
```

### 前端导包规则

```
config.py           ← 纯常量，不导入任何项目模块
    ↑
api_client.py       ← 从 config 导入 API_BASE_URL
    ↑
utils.py            ← 仅导入 streamlit
    ↑
styles.py           ← 仅导入 streamlit
    ↑
auth.py             ← 导入 api_client, utils, config
    ↑
views/*.py          ← 导入 api_client, utils, config（绝对导入）
    ↑
views/__init__.py   ← from .xxx import（相对导入）+ from config import（绝对导入）
    ↑
app.py              ← 导入 styles, auth, utils, config, views
```

> ⚠️ **注意**：前端页面目录必须命名为 `views/` 而非 `pages/`，因为 Streamlit 会自动识别 `pages/` 目录作为内置多页面导航，会产生冲突。

---

## 🎨 主题配置

在 `frontend/.streamlit/config.toml` 中自定义主题：

```toml
[theme]
primaryColor = "#d81b60"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#fce4ec"
textColor = "#333333"
font = "sans serif"
```

---

## 📋 权限矩阵

| 功能 | 游客 | 普通用户 | 认证喂猫人 | 管理员 |
|------|:----:|:-------:|:---------:|:-----:|
| 浏览猫猫图鉴 | ✅ | ✅ | ✅ | ✅ |
| 查看猫猫详情 | ✅ | ✅ | ✅ | ✅ |
| 查看评论/公告 | ✅ | ✅ | ✅ | ✅ |
| 收藏猫猫 | ❌ | ✅ | ✅ | ✅ |
| 发表评论 | ❌ | ✅ | ✅ | ✅ |
| 喂猫打卡 | ❌ | ✅ | ✅ | ✅ |
| 发布寻猫/求助 | ❌ | ✅ | ✅ | ✅ |
| 提交领养申请 | ❌ | ✅ | ✅ | ✅ |
| 上传猫猫照片 | ❌ | ✅ | ✅ | ✅ |
| 删除自己的评论 | ❌ | ✅ | ✅ | ✅ |
| 新增/编辑猫猫 | ❌ | ❌ | ❌ | ✅ |
| 审核领养申请 | ❌ | ❌ | ❌ | ✅ |
| 发布/删除公告 | ❌ | ❌ | ❌ | ✅ |
| 管理用户权限 | ❌ | ❌ | ❌ | ✅ |
| 删除他人评论 | ❌ | ❌ | ❌ | ✅ |
| 数据备份导出 | ❌ | ❌ | ❌ | ✅ |

---

## 📦 依赖清单

### 后端 (`backend/requirements.txt`)

```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pymysql==1.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
aiofiles==23.2.1
```

### 前端 (`frontend/requirements.txt`)

```txt
streamlit==1.29.0
requests==2.31.0
pandas==2.1.3
```

---

## ❓ 常见问题

<details>
<summary><b>Q: 前端启动后显示"无法连接到后端服务"？</b></summary>

确保后端已启动并运行在 `http://localhost:8000`。如果后端端口不同，请修改 `frontend/config.py` 中的 `API_BASE_URL`。

```python
# frontend/config.py
API_BASE_URL = "http://localhost:8000"  # 修改为你的后端地址
```
</details>

<details>
<summary><b>Q: 页面文字颜色看不清怎么办？</b></summary>

在 `frontend/.streamlit/config.toml` 中强制使用浅色主题：

```toml
[theme]
primaryColor = "#d81b60"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#fce4ec"
textColor = "#333333"
```

然后在浏览器中按 `Ctrl + F5` 强制刷新。
</details>

<details>
<summary><b>Q: 为什么前端目录用 views/ 而不是 pages/？</b></summary>

Streamlit 会自动将 `pages/` 目录识别为内置多页面导航功能，在侧边栏生成额外的页面链接，与我们自定义的导航系统冲突。因此必须重命名为 `views/`。
</details>

<details>
<summary><b>Q: 如何切换到 MySQL 数据库？</b></summary>

1. 安装 MySQL 驱动：`pip install pymysql`
2. 创建数据库：`CREATE DATABASE campus_cat CHARACTER SET utf8mb4;`
3. 修改 `backend/database.py`：
   ```python
   DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/campus_cat?charset=utf8mb4"
   ```
4. 重启后端，自动建表并填充种子数据。
</details>

<details>
<summary><b>Q: 如何部署到服务器？</b></summary>

```bash
# 后端（使用 gunicorn + uvicorn worker）
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

# 前端
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

建议使用 Nginx 做反向代理，将两个服务统一到 80/443 端口。
</details>

---

## 🤝 参与贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

---

<div align="center">

**🐱 用爱守护每一只校园猫咪 🐾**

Made with ❤️ for 北华大学

</div>