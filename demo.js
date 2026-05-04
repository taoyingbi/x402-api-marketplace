#!/usr/bin/env node

/**
 * x402 API Marketplace 演示脚本
 * 
 * 使用方法：
 * node demo.js
 */

const BASE_URL = 'http://localhost:3000';

// 颜色输出
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m'
};

function log(color, message) {
  console.log(`${color}${message}${colors.reset}`);
}

async function testEndpoint(name, url, options = {}) {
  log(colors.blue, `\n🧪 测试: ${name}`);
  log(colors.yellow, `   URL: ${url}`);
  
  try {
    const response = await fetch(url, options);
    const data = await response.json();
    
    if (response.ok) {
      log(colors.green, `   ✅ 成功 (${response.status})`);
      console.log('   响应:', JSON.stringify(data, null, 2));
      return true;
    } else {
      log(colors.red, `   ❌ 失败 (${response.status})`);
      console.log('   错误:', data);
      return false;
    }
  } catch (error) {
    log(colors.red, `   ❌ 错误: ${error.message}`);
    return false;
  }
}

async function runDemo() {
  log(colors.blue, '🚀 x402 API Marketplace 演示');
  log(colors.blue, '============================\n');

  // 测试1: 健康检查
  await testEndpoint('健康检查', `${BASE_URL}/health`);

  // 测试2: 根端点
  await testEndpoint('根端点', `${BASE_URL}/`);

  // 测试3: JSON转CSV
  await testEndpoint('JSON转CSV', `${BASE_URL}/convert/json-to-csv`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify([
      { name: 'Alice', age: 30, city: 'Beijing' },
      { name: 'Bob', age: 25, city: 'Shanghai' }
    ])
  });

  // 测试4: CSV转JSON
  await testEndpoint('CSV转JSON', `${BASE_URL}/convert/csv-to-json`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: 'name,age,city\nAlice,30,Beijing\nBob,25,Shanghai'
  });

  // 测试5: JSON格式化
  await testEndpoint('JSON格式化', `${BASE_URL}/convert/json-format`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Alice', age: 30, hobbies: ['reading', 'coding'] })
  });

  // 测试6: CSV转Markdown
  await testEndpoint('CSV转Markdown', `${BASE_URL}/convert/csv-to-markdown`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: 'name,age,city\nAlice,30,Beijing\nBob,25,Shanghai'
  });

  log(colors.blue, '\n✨ 演示完成！');
  log(colors.green, '\n💡 提示: 所有端点都需要x402微支付（USDC）');
  log(colors.yellow, '   钱包地址: 0xBF7acFa355aB8fd397fd30f34Bdaf5c437EF3040');
  log(colors.yellow, '   网络: Base链 (eip155:8453)');
}

// 运行演示
runDemo().catch(console.error);