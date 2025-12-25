# Chef Dish Management System

一个基于 Python 和 MySQL 的厨师菜品管理系统，支持厨师和管理员两种角色，实现菜品的增删查改功能。

## 项目功能

### 厨师功能
- **查看菜品**：查看自己管理的所有菜品
- **添加菜品**：添加新的菜品信息
- **修改菜品**：修改已有菜品的描述信息

### 管理员功能
- **管理厨师账号**：
  - 添加厨师账号
  - 删除厨师账号
- **管理菜品信息**：
  - 添加菜品信息
  - 删除菜品信息

## 技术栈

- **Python 3.x**
- **MySQL 8.0**
- **mysql-connector-python**：MySQL 数据库连接驱动
- **python-dotenv**：环境变量管理
- **Docker & Docker Compose**：容器化部署

## 环境要求

### macOS 系统要求
- Python 3.7+
- Docker Desktop for Mac 或 OrbStack（必须已安装并运行）
- pip（Python 包管理器）

**重要提示：**
- 首次使用前，请确保 Docker Desktop 或 OrbStack 应用已启动
- Docker 服务未运行时，所有 docker 命令都会失败
- 如果遇到 `docker compose` 命令错误，请先启动 Docker Desktop 应用

## 快速开始

### 方法一：使用启动脚本（推荐，macOS）

**前提条件：**
1. 确保 Docker Desktop 或 OrbStack 已启动（在应用程序中打开）
2. 等待 Docker 服务完全启动（状态栏显示 Docker 图标）

**一键启动：**
```bash
./start.sh
```

脚本会自动：
- 检查 Docker 服务状态
- 启动 MySQL 容器并导入数据
- 等待数据库就绪
- 运行 Python 程序

### 方法二：手动启动

1. **确保 Docker 服务运行**
   - 打开 Docker Desktop 或 OrbStack 应用
   - 等待服务完全启动（约 10-30 秒）

2. **启动数据库服务**
   ```bash
   # 尝试新版本命令（Docker Desktop 内置）
   docker compose up -d
   
   # 如果上面失败，尝试旧版本命令
   docker-compose up -d
   ```
   这将启动 MySQL 容器并自动导入数据库结构和初始数据。

3. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```bash
   python main.py
   ```

### 详细步骤

#### 1. 克隆或下载项目
```bash
cd chef-dish-management-system
```

#### 2. 配置环境变量
项目已包含 `.env` 文件，默认配置如下：
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=root
DB_NAME=chefdishmanagement
```

如需修改数据库配置，请编辑 `.env` 文件。

#### 3. 启动数据库
```bash
docker compose up -d
```

等待数据库完全启动（约 10-30 秒），可以通过以下命令检查：
```bash
docker compose ps
```

#### 4. 安装依赖
```bash
pip install -r requirements.txt
```

#### 5. 运行程序
```bash
python main.py
```

## 数据库信息

### 初始数据

**厨师账号：**
- ChefID: 1, Name: Chef A, Password: password1
- ChefID: 2, Name: Chef B, Password: password2

**管理员账号：**
- AdminID: 1, Name: Admin A, Password: adminpassword1

**初始菜品：**
- DishID: 1, Name: Dish A, ChefID: 1
- DishID: 2, Name: Dish B, ChefID: 2

## 使用说明

1. 运行程序后，首先选择用户类型：
   - 输入 `1` 选择厨师
   - 输入 `2` 选择管理员

2. 根据提示输入账号和密码登录

3. 登录成功后，根据菜单选择相应功能进行操作

4. 输入 `0` 退出当前菜单或程序

## 项目结构

```
chef-dish-management-system/
├── main.py                    # 主程序入口
├── requirements.txt           # Python 依赖包
├── docker-compose.yml         # Docker Compose 配置
├── .env                       # 环境变量配置
├── chefdishmanagement1.sql   # 数据库初始化脚本
├── README.md                  # 项目说明文档
└── SourceCode/                # 源代码备份
    ├── PythonSourceCode.txt
    └── SQLSourseCode.txt
```

## 停止服务

停止并删除容器：
```bash
docker compose down
```

停止容器但保留数据：
```bash
docker compose stop
```

删除容器和数据卷（**注意：会删除所有数据**）：
```bash
docker compose down -v
```

## 故障排查

### Docker 命令错误：`unknown shorthand flag: 'd' in -d`
**原因：** Docker 服务未运行或 Docker Desktop 未启动

**解决方案：**
1. 打开 Docker Desktop 应用（在应用程序文件夹中）
2. 等待 Docker 图标在状态栏显示为运行状态
3. 重新运行命令

### `docker compose` 命令不存在
**原因：** 使用的是旧版本 Docker，需要使用 `docker-compose`（带连字符）

**解决方案：**
```bash
# 使用带连字符的命令
docker-compose up -d
```

如果仍然失败，可以安装 docker-compose：
```bash
brew install docker-compose
```

### 数据库连接失败
1. 确保 Docker 容器正在运行：`docker compose ps` 或 `docker-compose ps`
2. 检查 `.env` 文件中的数据库配置是否正确
3. 等待数据库完全启动（首次启动需要初始化，约 10-30 秒）
4. 检查容器日志：`docker logs chefdish_mysql`

### 端口冲突
如果 3306 端口已被占用，可以修改 `docker-compose.yml` 中的端口映射：
```yaml
ports:
  - "3307:3306"  # 将主机端口改为 3307
```
同时需要更新 `.env` 文件中的 `DB_PORT=3307`

## 开发说明

本项目是大二时与室友一起完成的数据库课程项目，实现了基本的增删查改功能，但没有前端界面，使用命令行交互。

## 许可证

本项目仅用于学习和教育目的。
