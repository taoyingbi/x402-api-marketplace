#!/bin/bash
# x402 API Marketplace 推广自动化主脚本
# 
# 支持平台：
# - Dev.to (需要 DEVTO_API_KEY)
# - Reddit (需要 REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD)
# - GitHub (已配置 SSH)
#
# 使用方法：
#   ./promote.sh [platform]
#
#   platform: devto | reddit | github | all (默认: all)

PLATFORM="${1:-all}"
PROJECT_DIR="/home/lanxuan86/auto-api-system"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

case "$PLATFORM" in
    devto)
        log "📝 发布到 Dev.to..."
        "$SCRIPT_DIR/scripts/post-devto.sh" "$PROJECT_DIR/promotion/blog-devto.md"
        ;;
    reddit)
        log "📝 发布到 Reddit..."
        "$SCRIPT_DIR/scripts/post-reddit.sh" "webdev" "I built a zero-cost API marketplace with x402 micro-payments" "$PROJECT_DIR/promotion/social-media-posts.md"
        ;;
    github)
        log "📝 更新 GitHub..."
        "$SCRIPT_DIR/scripts/update-github.sh"
        ;;
    all)
        log "🚀 开始全平台推广..."
        # GitHub 始终运行
        "$SCRIPT_DIR/scripts/update-github.sh"
        # Dev.to
        if [ -n "$DEVTO_API_KEY" ]; then
            "$SCRIPT_DIR/scripts/post-devto.sh" "$PROJECT_DIR/promotion/blog-devto.md"
        else
            log "⚠️ Dev.to: 未设置 DEVTO_API_KEY，跳过"
        fi
        # Reddit
        if [ -n "$REDDIT_CLIENT_ID" ] && [ -n "$REDDIT_CLIENT_SECRET" ]; then
            "$SCRIPT_DIR/scripts/post-reddit.sh" "webdev" "I built a zero-cost API marketplace with x402 micro-payments" "$PROJECT_DIR/promotion/social-media-posts.md"
        else
            log "⚠️ Reddit: 未设置凭据，跳过"
        fi
        log "✅ 推广完成"
        ;;
    *)
        echo "用法: $0 [devto|reddit|github|all]"
        exit 1
        ;;
esac