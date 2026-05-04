#!/usr/bin/env python3
"""
项目生成脚本
根据市场需求分析结果自动生成新的API服务项目
"""

import json
import os
import subprocess
import sys
from datetime import datetime
import shutil

# 项目模板库
PROJECT_TEMPLATES = {
    "file_converter": {
        "name": "File Converter API",
        "description": "多功能文件格式转换服务",
        "features": ["PDF转Word", "图片格式转换", "JSON/CSV互转", "文档压缩"],
        "price": "$0.01",
        "complexity": "medium"
    },
    "ai_text_processor": {
        "name": "AI Text Processor",
        "description": "AI驱动的文本处理服务",
        "features": ["文本摘要", "关键词提取", "情感分析", "语法检查"],
        "price": "$0.02",
        "complexity": "high"
    },
    "image_optimizer": {
        "name": "Image Optimizer API",
        "description": "图片优化和处理服务",
        "features": ["图片压缩", "尺寸调整", "格式转换", "水印添加"],
        "price": "$0.015",
        "complexity": "medium"
    },
    "data_validator": {
        "name": "Data Validator API",
        "description": "数据验证和清洗服务",
        "features": ["邮箱验证", "电话验证", "地址标准化", "数据格式化"],
        "price": "$0.005",
        "complexity": "low"
    },
    "code_formatter": {
        "name": "Code Formatter API",
        "description": "代码格式化和美化服务",
        "features": ["JavaScript格式化", "Python格式化", "JSON美化", "CSS压缩"],
        "price": "$0.008",
        "complexity": "low"
    }
}

def select_project_based_on_trends(trends):
    """根据市场趋势选择项目"""
    
    # 趋势关键词到项目类型的映射
    trend_mapping = {
        "AI": "ai_text_processor",
        "text": "ai_text_processor",
        "file": "file_converter",
        "PDF": "file_converter",
        "image": "image_optimizer",
        "data": "data_validator",
        "JSON": "data_validator",
        "CSV": "data_validator",
        "code": "code_formatter",
        "JavaScript": "code_formatter",
        "Python": "code_formatter"
    }
    
    # 统计项目类型得分
    project_scores = {}
    for keyword, count in trends[:10]:
        if keyword in trend_mapping:
            project_type = trend_mapping[keyword]
            project_scores[project_type] = project_scores.get(project_type, 0) + count
    
    # 选择得分最高的项目
    if project_scores:
        selected_type = max(project_scores.items(), key=lambda x: x[1])[0]
        return selected_type, PROJECT_TEMPLATES[selected_type]
    
    # 默认选择文件转换器
    return "file_converter", PROJECT_TEMPLATES["file_converter"]

def generate_project_code(template, project_type):
    """生成项目代码"""
    
    project_name = f"auto-{project_type}-{datetime.now().strftime('%Y%m%d')}"
    project_path = f"/home/lanxuan86/auto-api-system/projects/{project_name}"
    
    # 创建项目目录
    os.makedirs(project_path, exist_ok=True)
    
    # 生成package.json
    package_json = {
        "name": project_name,
        "version": "1.0.0",
        "type": "module",
        "main": "server.js",
        "scripts": {
            "start": "node server.js",
            "test": "node test.js"
        },
        "dependencies": {
            "@coinbase/cdp-sdk": "^1.48.2",
            "@x402/core": "^2.11.0",
            "@x402/evm": "^2.11.0",
            "@x402/express": "^2.11.0",
            "@x402/fetch": "^2.11.0",
            "express": "^4.18.0",
            "multer": "^1.4.5-lts.1",
            "sharp": "^0.33.0",
            "pdf-lib": "^1.17.1",
            "mammoth": "^1.6.0",
            "xlsx": "^0.18.5"
        }
    }
    
    with open(f"{project_path}/package.json", "w") as f:
        json.dump(package_json, f, indent=2)
    
    # 生成server.js
    server_code = generate_server_code(template, project_type)
    with open(f"{project_path}/server.js", "w") as f:
        f.write(server_code)
    
    # 生成README.md
    readme_content = generate_readme(template, project_name)
    with open(f"{project_path}/README.md", "w") as f:
        f.write(readme_content)
    
    return project_path

def generate_server_code(template, project_type):
    """生成服务器代码"""
    
    if project_type == "file_converter":
        return generate_file_converter_code()
    elif project_type == "ai_text_processor":
        return generate_ai_text_processor_code()
    elif project_type == "image_optimizer":
        return generate_image_optimizer_code()
    elif project_type == "data_validator":
        return generate_data_validator_code()
    elif project_type == "code_formatter":
        return generate_code_formatter_code()
    else:
        return generate_file_converter_code()

def generate_file_converter_code():
    """生成文件转换器代码"""
    
    return '''import express from "express";
import { x402ResourceServer, HTTPFacilitatorClient } from "@x402/core/server";
import { registerExactEvmScheme } from "@x402/evm/exact/server";
import { paymentMiddleware } from "@x402/express";
import { createRequire } from "module";
import multer from "multer";
import sharp from "sharp";
import { PDFDocument } from "pdf-lib";
import mammoth from "mammoth";
import XLSX from "xlsx";

const require = createRequire(import.meta.url);
const { generateJwt } = require("@coinbase/cdp-sdk/auth");

const app = express();
app.use(express.json({ limit: "50mb" }));
app.use(express.text({ limit: "50mb" }));

// 文件上传配置
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 50 * 1024 * 1024 } // 50MB
});

const WALLET = "0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040";
const FACILITATOR = "https://api.cdp.coinbase.com/platform/v2/x402";
const NETWORK = "eip155:8453";
const CDP_KEY_ID = "75e8c011-e1a7-4f3d-a68c-37942e9edc10";
const CDP_KEY_SECRET = "Sbarpo...1w==";

function makeHeaders(method, path) {
  return generateJwt({
    apiKeyId: CDP_KEY_ID,
    apiKeySecret: CDP_KEY_SECRET,
    requestMethod: method,
    requestHost: "api.cdp.coinbase.com",
    requestPath: path,
    expiresIn: 120,
  }).then(jwt => ({ Authorization: `Bearer ${jwt}` }));
}

const facilitatorClient = new HTTPFacilitatorClient({
  url: FACILITATOR,
  createAuthHeaders: async () => ({
    verify: await makeHeaders("POST", "/platform/v2/x402/verify"),
    settle: await makeHeaders("POST", "/platform/v2/x402/settle"),
    supported: await makeHeaders("GET", "/platform/v2/x402/supported"),
  }),
});

const resourceServer = new x402ResourceServer(facilitatorClient);
registerExactEvmScheme(resourceServer, {});

const routes = {
  "POST /convert/image": { accepts: [{ scheme: "exact", network: NETWORK, price: "$0.01", payTo: WALLET, description: "Image format conversion" }] },
  "POST /convert/document": { accepts: [{ scheme: "exact", network: NETWORK, price: "$0.02", payTo: WALLET, description: "Document conversion" }] },
  "POST /convert/spreadsheet": { accepts: [{ scheme: "exact", network: NETWORK, price: "$0.015", payTo: WALLET, description: "Spreadsheet conversion" }] },
  "POST /compress/image": { accepts: [{ scheme: "exact", network: NETWORK, price: "$0.008", payTo: WALLET, description: "Image compression" }] },
};

app.use(paymentMiddleware(routes, resourceServer));

// 图片格式转换
app.post("/convert/image", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    
    const { format = "png", width, height } = req.body;
    let processor = sharp(req.file.buffer);
    
    if (width || height) {
      processor = processor.resize(parseInt(width), parseInt(height));
    }
    
    const result = await processor.toFormat(format).toBuffer();
    
    res.set({
      "Content-Type": `image/${format}`,
      "Content-Disposition": `attachment; filename=converted.${format}`
    });
    res.send(result);
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

// 文档转换
app.post("/convert/document", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    
    const { format = "html" } = req.body;
    let result;
    
    if (format === "html") {
      result = await mammoth.convertToHtml({ buffer: req.file.buffer });
    } else if (format === "text") {
      result = await mammoth.extractRawText({ buffer: req.file.buffer });
    }
    
    res.json({ result: result.value });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

// 电子表格转换
app.post("/convert/spreadsheet", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    
    const { format = "csv" } = req.body;
    const workbook = XLSX.read(req.file.buffer, { type: "buffer" });
    const sheetName = workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    
    let result;
    if (format === "csv") {
      result = XLSX.utils.sheet_to_csv(worksheet);
    } else if (format === "json") {
      result = JSON.stringify(XLSX.utils.sheet_to_json(worksheet), null, 2);
    }
    
    res.json({ result });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

// 图片压缩
app.post("/compress/image", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No file uploaded" });
    
    const { quality = 80 } = req.body;
    const result = await sharp(req.file.buffer)
      .jpeg({ quality: parseInt(quality) })
      .toBuffer();
    
    res.set({
      "Content-Type": "image/jpeg",
      "Content-Disposition": "attachment; filename=compressed.jpg"
    });
    res.send(result);
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

// 健康检查
app.get("/health", (req, res) => {
  res.json({ status: "healthy", timestamp: new Date().toISOString() });
});

const PORT = 3000;
app.listen(PORT, "0.0.0.0", () => {
  console.log(`File Converter API started on port ${PORT}`);
  console.log(`Wallet: ${WALLET}`);
  console.log(`Network: ${NETWORK}`);
});
'''

def generate_readme(template, project_name):
    """生成README文件"""
    
    return f"""# {template['name']}

{template['description']}

## 功能特性

{chr(10).join(f"- {feature}" for feature in template['features'])}

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

*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

def deploy_project(project_path):
    """部署项目到3000端口"""
    
    print(f"部署项目: {project_path}")
    
    # 安装依赖
    print("安装依赖...")
    subprocess.run(["npm", "install"], cwd=project_path, check=True)
    
    # 停止现有服务
    print("停止现有服务...")
    subprocess.run(["/home/lanxuan86/.npm-global/bin/pm2", "stop", "x402-api-service"], 
                   capture_output=True)
    
    # 启动新服务
    print("启动新服务...")
    subprocess.run([
        "/home/lanxuan86/.npm-global/bin/pm2", "start", "server.js",
        "--name", "x402-api-service",
        "--cwd", project_path
    ], check=True)
    
    # 保存进程列表
    subprocess.run(["/home/lanxuan86/.npm-global/bin/pm2", "save"], 
                   capture_output=True)
    
    print("部署完成！")
    return True

def main():
    """主函数"""
    
    print("开始项目生成流程...")
    
    # 读取最新的市场分析报告
    report_files = []
    logs_dir = "/home/lanxuan86/auto-api-system/logs"
    if os.path.exists(logs_dir):
        for f in os.listdir(logs_dir):
            if f.startswith("market-analysis-") and f.endswith(".md"):
                report_files.append(f)
    
    if not report_files:
        print("未找到市场分析报告，使用默认模板")
        trends = [("file", 10), ("conversion", 8), ("API", 7)]
    else:
        # 读取最新的报告
        latest_report = sorted(report_files)[-1]
        report_path = f"{logs_dir}/{latest_report}"
        
        # 这里可以添加解析报告的逻辑
        # 简化处理，使用默认趋势
        trends = [("file", 10), ("conversion", 8), ("API", 7)]
    
    # 选择项目
    project_type, template = select_project_based_on_trends(trends)
    print(f"选择项目类型: {project_type}")
    print(f"项目名称: {template['name']}")
    
    # 生成项目
    project_path = generate_project_code(template, project_type)
    print(f"项目生成完成: {project_path}")
    
    # 部署项目
    deploy_project(project_path)
    
    # 记录部署信息
    deployment_log = {
        "timestamp": datetime.now().isoformat(),
        "project_type": project_type,
        "project_path": project_path,
        "template": template
    }
    
    log_path = f"/home/lanxuan86/auto-api-system/logs/deployment-{datetime.now().strftime('%Y%m%d')}.json"
    with open(log_path, "w") as f:
        json.dump(deployment_log, f, indent=2)
    
    print(f"部署日志已保存: {log_path}")
    
    return project_path

if __name__ == "__main__":
    main()