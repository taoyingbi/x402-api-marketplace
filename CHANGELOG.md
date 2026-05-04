# 更新日志

所有重要更改都会记录在此文件中。

格式基于[Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
并且本项目遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [未发布]

### 新增
- 市场需求分析系统
- 自动项目生成器
- 服务监控和自动重启
- 每日报告生成

### 优化
- PM2进程管理
- x402微支付集成
- API性能优化

## [1.0.0] - 2026-05-04

### 新增
- 初始版本发布
- 文件转换API
  - JSON转CSV
  - CSV转JSON
  - JSON格式化
  - CSV转Markdown
- 图片处理API
  - 图片压缩
  - 图片格式转换
- 文档转换API
  - 文档转HTML
  - 文档转文本
- 电子表格转换API
  - Excel转CSV
  - Excel转JSON
- x402微支付集成
- Base链USDC支付
- PM2进程管理
- 健康检查端点
- API文档

### 技术栈
- Node.js 18+
- Express.js 4.x
- x402 Protocol
- Base Chain (EIP155:8453)
- PM2

## [0.1.0] - 2026-05-03

### 新增
- 项目初始化
- 基础架构搭建
- 开发环境配置

---

## 版本号说明

- **主版本号**：不兼容的API更改
- **次版本号**：向下兼容的功能性新增
- **修订号**：向下兼容的问题修正

## 如何更新

1. 拉取最新代码
```bash
git pull origin main
```

2. 安装新依赖
```bash
npm install
```

3. 重启服务
```bash
pm2 restart x402-api-service
```

## 贡献指南

请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码。