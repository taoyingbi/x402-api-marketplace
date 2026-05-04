# 贡献指南

感谢你对 x402 API Marketplace 项目的关注！

## 如何贡献

### 1. 报告Bug
- 使用GitHub Issues报告问题
- 提供详细的复现步骤
- 包含错误日志和截图

### 2. 提出新功能
- 在Issues中描述功能需求
- 说明使用场景
- 讨论实现方案

### 3. 提交代码

#### 步骤
1. Fork项目
2. 创建功能分支
```bash
git checkout -b feature/your-feature
```
3. 提交更改
```bash
git commit -m "Add: your feature"
```
4. 推送到分支
```bash
git push origin feature/your-feature
```
5. 创建Pull Request

#### 代码规范
- 使用ES6+语法
- 遵循Airbnb代码风格
- 添加必要的注释
- 编写单元测试

#### 提交信息格式
```
类型: 简短描述

详细描述（可选）

相关Issue（可选）
```

类型包括：
- `Add`: 新功能
- `Fix`: 修复Bug
- `Update`: 更新功能
- `Refactor`: 重构代码
- `Docs`: 文档更新
- `Test`: 测试相关
- `Chore`: 构建/工具相关

### 4. 改进文档
- 修正错别字
- 添加使用示例
- 翻译文档

## 开发环境

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/x402-api-marketplace.git
cd x402-api-marketplace
```

### 2. 安装依赖
```bash
npm install
```

### 3. 配置环境
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 4. 启动开发服务器
```bash
npm run dev
```

### 5. 运行测试
```bash
npm test
```

## 项目结构

```
x402-api-marketplace/
├── server.js              # 主服务器
├── package.json           # 项目配置
├── .env.example           # 环境变量示例
├── scripts/               # 自动化脚本
├── templates/             # 项目模板
├── projects/              # 生成的项目
├── logs/                  # 日志文件
├── tests/                 # 测试文件
└── docs/                  # 文档
```

## 发布流程

### 1. 版本号规范
使用语义化版本号：`主版本.次版本.修订号`

- 主版本：不兼容的API更改
- 次版本：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 2. 发布步骤
1. 更新版本号
```bash
npm version patch/minor/major
```
2. 更新CHANGELOG.md
3. 创建Git标签
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
```
4. 推送到GitHub
```bash
git push origin main --tags
```
5. 创建GitHub Release

## 行为准则

### 我们的承诺
- 营造开放、友好的环境
- 尊重不同观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情

### 不可接受的行为
- 使用性暗示的语言或图像
- 恶意评论或人身攻击
- 公开或私下骚扰
- 未经许可发布他人私人信息

## 许可证

贡献即表示你同意你的贡献将在MIT许可证下发布。

## 联系方式

如有任何问题，请通过以下方式联系：
- GitHub Issues
- Email: your@email.com

感谢你的贡献！🎉