#!/bin/bash
# GitHub 自动更新脚本
# 定期更新 README 和项目状态

set -e

PROJECT_DIR="/home/lanxuan86/auto-api-system"
cd "$PROJECT_DIR"

echo "📝 更新 GitHub 仓库..."

# 添加所有更改
git add -A

# 检查是否有更改
if git diff --staged --quiet; then
    echo "✅ 没有新的更改需要提交"
    exit 0
fi

# 提交更改
git commit -m "Update: $(date '+%Y-%m-%d %H:%M') - Promotion content update"

# 推送到 GitHub
git push origin master

echo "✅ GitHub 已更新"