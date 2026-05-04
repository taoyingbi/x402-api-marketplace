# 🚀 x402 API Marketplace 快速启动指南

## 📋 前置条件

- Node.js 18+
- npm 或 yarn
- Git
- Python 3.8+（用于自动化脚本）

## ⚡ 5分钟快速开始

### 1. 克隆仓库
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
# 编辑 .env 文件，配置你的钱包地址和API密钥
```

### 4. 启动服务
```bash
npm start
```

### 5. 测试API
```bash
# 健康检查
curl http://localhost:3000/health

# 查看可用端点
curl http://localhost:3000/

# 运行演示
node demo.js
```

## 🎯 核心功能演示

### 文件转换API

#### JSON转CSV
```bash
curl -X POST http://localhost:3000/convert/json-to-csv \
  -H "Content-Type: application/json" \
  -d '[{"name":"Alice","age":30},{"name":"Bob","age":25}]'
```

**响应：**
```json
{
  "result": "name,age\nAlice,30\nBob,25"
}
```

#### CSV转JSON
```bash
curl -X POST http://localhost:3000/convert/csv-to-json \
  -H "Content-Type: text/plain" \
  -d "name,age\nAlice,30\nBob,25"
```

**响应：**
```json
{
  "result": [
    {"name": "Alice", "age": "30"},
    {"name": "Bob", "age": "25"}
  ]
}
```

### 图片处理API

#### 图片压缩
```bash
curl -X POST http://localhost:3000/compress/image \
  -F "file=@image.jpg" \
  -F "quality=80"
```

#### 图片格式转换
```bash
curl -X POST http://localhost:3000/convert/image \
  -F "file=@image.png" \
  -F "format=webp"
```

## 💰 支付集成

### x402微支付配置

1. **获取钱包地址**
   - 使用MetaMask或其他钱包
   - 切换到Base链网络

2. **配置环境变量**
   ```bash
   # .env 文件
   WALLET_ADDRESS=0xYourWalletAddress
   WALLET_PRIVATE_KEY=0xYourPrivateKey
   CDP_KEY_ID=your-cdp-key-id
   CDP_KEY_SECRET=your-cdp-key-secret
   ```

3. **测试支付流程**
   ```bash
   # 使用测试脚本
   WALLET_PRIVATE_KEY=your_private_key node test-pay.js
   ```

### 定价策略

| API端点 | 功能 | 价格 |
|---------|------|------|
| POST /convert/json-to-csv | JSON转CSV | $0.01 |
| POST /convert/csv-to-json | CSV转JSON | $0.01 |
| POST /convert/json-format | JSON格式化 | $0.005 |
| POST /convert/csv-to-markdown | CSV转Markdown | $0.01 |
| POST /convert/image | 图片格式转换 | $0.01 |
| POST /convert/document | 文档转换 | $0.02 |
| POST /convert/spreadsheet | 电子表格转换 | $0.015 |
| POST /compress/image | 图片压缩 | $0.008 |

## 🔧 高级配置

### PM2进程管理

#### 启动服务
```bash
# 使用PM2启动
npm run pm2:start

# 查看状态
pm2 list

# 查看日志
npm run pm2:logs

# 监控
npm run pm2:monit
```

#### PM2配置
```bash
# 自动重启
pm2 startup

# 保存配置
pm2 save
```

### 自动化系统

#### 市场需求分析
```bash
# 手动执行
npm run market-analysis

# 查看报告
cat logs/market-analysis-$(date +%Y%m%d).md
```

#### 项目生成
```bash
# 手动生成
npm run generate-project

# 查看生成的项目
ls projects/
```

#### 服务监控
```bash
# 手动监控
npm run monitor

# 查看监控报告
cat logs/monitoring-*.md
```

### 定时任务

#### 查看定时任务
```bash
hermes cron list
```

#### 手动执行
```bash
hermes cron run <job_id>
```

## 📊 监控和报告

### 健康检查
```bash
curl http://localhost:3000/health
```

**响应：**
```json
{
  "status": "healthy",
  "timestamp": "2026-05-04T00:47:26.580Z"
}
```

### 查看日志
```bash
# PM2日志
pm2 logs x402-api-service

# 应用日志
tail -f logs/app.log
```

### 生成报告
```bash
# 每日报告
npm run daily-report

# 查看报告
cat logs/daily-report-$(date +%Y%m%d).md
```

## 🚀 部署到生产环境

### 1. 服务器准备
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装PM2
sudo npm install -g pm2
```

### 2. 部署应用
```bash
# 克隆代码
git clone https://github.com/yourusername/x402-api-marketplace.git
cd x402-api-marketplace

# 安装依赖
npm install --production

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 启动服务
pm2 start server.js --name x402-api-service

# 保存配置
pm2 save

# 设置开机自启
pm2 startup
```

### 3. 配置Nginx（可选）
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4. 配置SSL（可选）
```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com
```

## 📈 推广和盈利

### 推广渠道

1. **GitHub**
   - 完善README
   - 添加示例代码
   - 配置GitHub Actions

2. **社交媒体**
   - Twitter/X
   - LinkedIn
   - 微信公众号

3. **技术社区**
   - Stack Overflow
   - Reddit
   - Hacker News

4. **内容营销**
   - 技术博客
   - 视频教程
   - 在线课程

### 盈利模式

1. **按调用次数收费**
   - 设置合理定价
   - 提供批量优惠
   - 自动结算

2. **订阅制**
   - 基础版：$9.99/月
   - 专业版：$29.99/月
   - 企业版：$99.99/月

3. **免费增值**
   - 免费层：每天100次调用
   - 付费层：超出后按次收费

### 收益预测

| 阶段 | 时间 | 日均调用 | 月收入 |
|------|------|---------|--------|
| 启动期 | 1-3月 | 1,000 | $450 |
| 成长期 | 3-6月 | 10,000 | $6,000 |
| 成熟期 | 6-12月 | 50,000 | $37,500 |

## 🔍 故障排除

### 常见问题

#### 1. 服务无法启动
```bash
# 检查端口占用
lsof -i :3000

# 检查日志
pm2 logs x402-api-service

# 重启服务
pm2 restart x402-api-service
```

#### 2. 支付失败
```bash
# 检查钱包配置
cat .env | grep WALLET

# 检查网络连接
curl https://api.cdp.coinbase.com/platform/v2/x402/supported

# 查看支付日志
grep "payment" logs/*.log
```

#### 3. 性能问题
```bash
# 监控资源使用
pm2 monit

# 查看系统资源
top
free -h
df -h
```

### 获取帮助

1. **查看文档**
   - README.md
   - API文档
   - 部署指南

2. **社区支持**
   - GitHub Issues
   - 讨论区
   - 社交媒体

3. **联系作者**
   - Email
   - Twitter
   - LinkedIn

## 📚 相关资源

### 官方文档
- [x402 Protocol](https://x402.org)
- [Base Chain](https://base.org)
- [Express.js](https://expressjs.com)
- [PM2](https://pm2.io)

### 学习资源
- [Node.js教程](https://nodejs.org/en/docs/)
- [Express.js指南](https://expressjs.com/en/guide/)
- [Web3开发](https://web3js.readthedocs.io/)

### 工具推荐
- [Postman](https://www.postman.com/) - API测试
- [VS Code](https://code.visualstudio.com/) - 代码编辑器
- [Docker](https://www.docker.com/) - 容器化部署

## 🎉 总结

x402 API Marketplace让你能够：

1. ✅ **零成本启动** - 无需服务器成本
2. ✅ **自动盈利** - x402微支付集成
3. ✅ **智能运营** - 市场分析和项目生成
4. ✅ **稳定运行** - PM2进程管理
5. ✅ **持续优化** - 监控和报告系统

**立即开始构建你的API服务市场！**

---

**📧 联系方式**
- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)
- Email: your@email.com

**⭐ 如果这个项目对你有帮助，请给个Star！**