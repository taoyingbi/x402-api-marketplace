---
name: Bug报告
about: 报告一个bug
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug描述
简要描述bug是什么。

## 复现步骤
1. 调用 '...'
2. 发送请求 '...'
3. 看到错误 '...'

## 预期行为
描述你期望发生什么。

## 实际行为
描述实际发生了什么。

## 环境信息
- 操作系统: [例如 Ubuntu 22.04]
- Node.js版本: [例如 18.17.0]
- npm版本: [例如 9.6.7]
- API版本: [例如 1.0.0]

## 请求信息
```bash
# 请求命令
curl -X POST http://localhost:3000/convert/json-to-csv \
  -H "Content-Type: application/json" \
  -d '[{"name":"Alice","age":30}]'
```

## 响应信息
```json
{
  "error": "错误信息"
}
```

## 日志信息
```
粘贴相关的日志信息
```

## 截图
如果适用，添加截图来帮助解释问题。

## 其他信息
添加任何其他有关问题的信息。