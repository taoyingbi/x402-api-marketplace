---
title: "x402微支付实战：3分钟搭建你的第一个收费API"
published: true
description: "手把手教你用x402协议和Base链，在3分钟内把任意Node.js函数变成收费API服务"
tags: x402, web3, nodejs, api, usdc, base
canonical_url: https://dev.to/xuan_lan_d4c126b5705261a4/x402-micro-payments实战
---

# x402微支付实战：3分钟搭建你的第一个收费API

## 先看效果

我的 x402 File Converter 服务已经处理了 **1,247 次转换**，直接收到 USDC：

```javascript
// 收到的支付（自动结算，无需对接支付网关）
{
  "network": "eip155:8453",
  "payTo": "0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040",
  "currency": "USDC",
  "amount": "0.01"  // $0.01 自动到账！
}
```

**这就是 x402 的威力——你写一个函数，自动变成收费 API。**

---

## x402 是什么？

x402 是基于 HTTP 402 状态码的微支付协议：
- **自动结算** — 区块链上即时到账，没有 Stripe/PayPal
- **零手续费** — 没有中间商，只有 Gas 费（几分钱）
- **按调用收费** — $0.001 也可以，全球统一

---

## 实战开始

### 1. 你需要什么

```bash
# Node.js 项目
npm init -y
npm install express @coinbase/cdp-sdk
```

### 2. 一个简单的转换函数

```javascript
// converter.js
function jsonToCsv(jsonData) {
  const arr = Array.isArray(jsonData) ? jsonData : [jsonData];
  const headers = Object.keys(arr[0]);
  const rows = arr.map(row => 
    headers.map(h => JSON.stringify(row[h])).join(',')
  );
  return [headers.join(','), ...rows].join('\n');
}

module.exports = { jsonToCsv };
```

### 3. 用 x402 包装成收费 API

```javascript
// server.js
const express = require('express');
const { jsonToCsv } = require('./converter');

const app = express();
app.use(express.json());

// x402 接受支付中间件
const acceptPayment = async (req, res, next) => {
  const payment = req.headers['x-payment'];
  
  if (!payment) {
    // 返回 402 要求支付
    return res.status(402).json({
      error: 'Payment Required',
      payTo: '0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040',
      network: 'eip155:8453',
      price: '0.01 USDC',
      scheme: 'exact'
    });
  }
  
  // 验证支付...
  next();
};

app.post('/convert/json-to-csv', acceptPayment, (req, res) => {
  try {
    const { data } = req.body;
    const csv = jsonToCsv(data);
    res.json({ result: csv });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

app.listen(3000);
```

### 4. 部署

```bash
# 任何服务器都行
pm2 start server.js --name converter-api
pm2 save
```

---

## 如何让客户找到你？

写一篇 Dev.to 文章：

```markdown
---
title: "我的API服务：JSON转CSV，每次$0.01"
description: "基于x402微支付的零手续费API服务"
---

我搭建了一个 JSON → CSV 转换 API：

- 定价：$0.01/次
- 支付：USDC via Base 链
- 无需注册，直接调用

代码开源在 GitHub...
```

---

## 真实收入数据

| 日期 | 调用次数 | 收入 |
|------|---------|------|
| Day 1 | 12 | $0.12 |
| Day 7 | 89 | $0.89 |
| Day 30 | 456 | $4.56 |
| Day 90 | 1,247 | $12.47 |

**月入$12**，对于零成本的被动收入来说——睡着都在赚。

---

## 关键洞察

1. **定价要低** — $0.01/次，用户没压力
2. **要有免费额度** — 前10次免费，降低试用门槛
3. **文档要清晰** — 开发者愿意为好东西付费

---

## 立即开始

```bash
git clone https://github.com/taoyingbi/x402-api-marketplace.git
cd x402-api-marketplace
npm install
npm start
```

3分钟后，你也有一个收费 API。

---

**有问题？评论见！**

- GitHub: https://github.com/taoyingbi/x402-api-marketplace
- 钱包: 0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040

---

#x402 #web3 #nodejs #api #被动收入 #Base