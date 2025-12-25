#!/bin/bash

# 启动脚本 - 兼容不同的 Docker Compose 命令格式

echo "正在检查 Docker 服务..."

# 检查 Docker 是否运行
if ! docker ps > /dev/null 2>&1; then
    echo "错误: Docker 服务未运行"
    echo "请先启动 Docker Desktop 或 OrbStack"
    exit 1
fi

echo "Docker 服务运行正常"

# 尝试使用 docker compose (新版本)
if docker compose version > /dev/null 2>&1; then
    echo "使用 docker compose 启动服务..."
    docker compose up -d
# 尝试使用 docker-compose (旧版本)
elif command -v docker-compose > /dev/null 2>&1; then
    echo "使用 docker-compose 启动服务..."
    docker-compose up -d
else
    echo "错误: 未找到 docker compose 或 docker-compose 命令"
    echo "请安装 Docker Compose:"
    echo "  brew install docker-compose"
    exit 1
fi

# 等待数据库启动
echo "等待数据库启动..."
sleep 5

# 检查数据库是否就绪
max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if docker exec chefdish_mysql mysqladmin ping -h localhost -u root -proot > /dev/null 2>&1; then
        echo "数据库已就绪"
        break
    fi
    attempt=$((attempt + 1))
    echo "等待数据库启动... ($attempt/$max_attempts)"
    sleep 2
done

if [ $attempt -eq $max_attempts ]; then
    echo "警告: 数据库可能尚未完全启动，但继续运行程序..."
fi

# 运行 Python 程序
echo "启动 Python 程序..."
python main.py

