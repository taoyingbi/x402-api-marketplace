# File Converter API

多功能文件格式转换服务

## 功能特性

- PDF转Word
- 图片格式转换
- JSON/CSV互转
- 文档压缩

## API端点

所有端点都需要x402微支付（USDC）：

| 端点 | 功能 | 价格 |
|------|------|------|
| POST /convert/image | 图片格式转换 | $0.01 |
| POST /convert/document | 文档转换 | $0.02 |
| POST /convert/spreadsheet | 电子表格转换 | $0.015 |
| POST /compress/image | 图片压缩 | $0.008 |

## 技术栈

- Express.js
- Sharp (图片处理)
- PDF-lib (PDF处理)
- Mammoth (文档转换)
- SheetJS (电子表格处理)
- x402微支付协议

## 安装运行

```bash
npm install
npm start
```

## 测试

```bash
curl http://localhost:3000/health
```

## 钱包配置

- 钱包地址: 0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040
- 网络: Base链 (eip155:8453)
- 支付协议: x402微支付

---

*自动生成于 2026-05-04 09:01:01*
