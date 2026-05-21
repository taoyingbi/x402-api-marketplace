import express from "express";
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
