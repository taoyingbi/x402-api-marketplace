#!/bin/bash
# Dev.to 自动发布脚本
# 需要设置 DEVTO_API_KEY 环境变量

set -e

API_KEY="${DEVTO_API_KEY:-}"
ARTICLE_FILE="${1:-../blog-devto.md}"

if [ -z "$API_KEY" ]; then
    echo "❌ 请设置 DEVTO_API_KEY 环境变量"
    echo "   export DEVTO_API_KEY=your_api_key"
    exit 1
fi

# 读取 markdown 文件
CONTENT=$(cat "$ARTICLE_FILE")

# 提取 frontmatter
TITLE=$(echo "$CONTENT" | grep -m1 "^title:" | sed 's/title: *"\(.*\)"/\1/')
DESCRIPTION=$(echo "$CONTENT" | grep -m1 "^description:" | sed 's/description: *"\(.*\)"/\1/')
TAGS=$(echo "$CONTENT" | grep -m1 "^tags:" | sed 's/tags: *\(.*\)/\1/' | tr ',' ' ')
CANONICAL=$(echo "$CONTENT" | grep -m1 "^canonical_url:" | sed 's/canonical_url: *\(.*\)/\1/')

# 移除 frontmatter，只保留正文
BODY=$(echo "$CONTENT" | sed '1,/^---$/d')

# JSON escape
BODY_JSON=$(echo "$BODY" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')

curl -s -X POST "https://dev.to/api/articles" \
  -H "Content-Type: application/json" \
  -H "api-key: $API_KEY" \
  -d "{
    \"article\": {
      \"title\": $TITLE,
      \"body_markdown\": $BODY_JSON,
      \"description\": $DESCRIPTION,
      \"published\": true,
      \"tags\": [$TAGS],
      \"canonical_url\": $CANONICAL
    }
  }" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(f"✅ Posted: {d.get(\"url\", d)}")'