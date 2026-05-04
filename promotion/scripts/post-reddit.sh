#!/bin/bash
# Reddit 自动发布脚本
# 使用 Reddit API + PRAW (Python)
# 
# 设置方法：
# 1. 在 https://www.reddit.com/prefs/apps 创建一个脚本应用
# 2. 获取 client_id, client_secret
# 3. 设置环境变量或修改下方配置

set -e

SUBREDDIT="${1:-webdev}"
TITLE="${2:-I built a zero-cost API marketplace with x402 micro-payments}"
TEXT_FILE="${3:-../social-media-posts.md}"

# Reddit API 配置
CLIENT_ID="${REDDIT_CLIENT_ID:-}"
CLIENT_SECRET="${REDDIT_CLIENT_SECRET:-}"
USERNAME="${REDDIT_USERNAME:-}"
PASSWORD="${REDDIT_PASSWORD:-}"

if [ -z "$CLIENT_ID" ] || [ -z "$CLIENT_SECRET" ]; then
    echo "❌ 请设置 Reddit API 凭据:"
    echo "   export REDDIT_CLIENT_ID=your_client_id"
    echo "   export REDDIT_CLIENT_SECRET=your_client_secret"
    echo "   export REDDIT_USERNAME=your_username"
    echo "   export REDDIT_PASSWORD=your_password"
    exit 1
fi

# 获取 access token
TOKEN_RESP=$(curl -s -X POST "https://www.reddit.com/api/v1/access_token" \
  -d "grant_type=password&username=$USERNAME&password=$PASSWORD" \
  -H "User-Agent: x402-api-marketplace/1.0" \
  -u "$CLIENT_ID:$CLIENT_SECRET")

ACCESS_TOKEN=$(echo "$TOKEN_RESP" | python3 -c "import json,sys; print(json.load(sys.stdin).get('access_token',''))")

if [ -z "$ACCESS_TOKEN" ]; then
    echo "❌ 获取 Access Token 失败: $TOKEN_RESP"
    exit 1
fi

# 读取帖子内容
TEXT=$(cat "$TEXT_FILE" | sed -n '/r\/webdev/,/^---$/p' | head -n -1 | tail -n +2)

# JSON escape
TEXT_JSON=$(echo "$TEXT" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

# 发布到 subreddit
RESP=$(curl -s -X POST "https://oauth.reddit.com/r/$SUBREDDIT/submit" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "User-Agent: x402-api-marketplace/1.0" \
  -d "title=$TITLE&text=$TEXT_JSON&sr=$SUBREDDIT&kind=self")

if echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('json',{}).get('data',{}).get('url') else 1)" 2>/dev/null; then
    URL=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['json']['data']['url'])")
    echo "✅ Posted to r/$SUBREDDIT: $URL"
else
    echo "❌ 发布失败: $RESP"
fi