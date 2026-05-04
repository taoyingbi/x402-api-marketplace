#!/usr/bin/env python3
"""
市场需求分析脚本
每天自动分析当前热门的API服务、SaaS产品和开发者工具需求
"""

import json
import subprocess
import sys
from datetime import datetime
import os
import requests
from urllib.parse import quote_plus

def web_search(query, max_results=5):
    """使用DuckDuckGo进行web搜索"""
    
    try:
        # 使用DuckDuckGo HTML版本
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 简单解析HTML结果
        results = []
        lines = response.text.split('\n')
        
        for i, line in enumerate(lines):
            if 'result__a' in line and 'href=' in line:
                # 提取标题和URL
                start = line.find('href="') + 6
                end = line.find('"', start)
                result_url = line[start:end]
                
                # 提取标题
                title_start = line.find('>', line.find('result__a')) + 1
                title_end = line.find('</a>', title_start)
                title = line[title_start:title_end].strip()
                
                # 提取摘要
                snippet = ""
                for j in range(i+1, min(i+5, len(lines))):
                    if 'result__snippet' in lines[j]:
                        snippet_start = lines[j].find('>', lines[j].find('result__snippet')) + 1
                        snippet_end = lines[j].find('</a>', snippet_start)
                        if snippet_end == -1:
                            snippet_end = lines[j].find('</td>', snippet_start)
                        snippet = lines[j][snippet_start:snippet_end].strip()
                        break
                
                results.append({
                    "title": title,
                    "url": result_url,
                    "snippet": snippet
                })
                
                if len(results) >= max_results:
                    break
        
        return results
        
    except Exception as e:
        print(f"搜索失败 '{query}': {e}")
        return []

def analyze_market_demand():
    """分析当前市场需求"""
    
    # 搜索关键词列表
    search_queries = [
        "trending API services 2026",
        "most popular developer tools 2026",
        "top SaaS products demand 2026",
        "GitHub trending repositories API",
        "Product Hunt top products today",
        "most needed microservices 2026",
        "popular file conversion tools",
        "AI API services demand",
        "developer productivity tools trending",
        "most requested API endpoints"
    ]
    
    results = {}
    
    for query in search_queries:
        print(f"搜索: {query}")
        search_result = web_search(query, max_results=5)
        results[query] = search_result
    
    return results

def analyze_trends(search_results):
    """分析搜索结果，识别趋势"""
    
    # 关键词频率统计
    keywords = {
        "AI": 0, "machine learning": 0, "API": 0, "file conversion": 0,
        "PDF": 0, "image": 0, "text": 0, "data": 0, "automation": 0,
        "cloud": 0, "SaaS": 0, "microservice": 0, "REST": 0, "GraphQL": 0,
        "payment": 0, "authentication": 0, "database": 0, "storage": 0,
        "analytics": 0, "monitoring": 0, "notification": 0, "email": 0,
        "SMS": 0, "voice": 0, "video": 0, "audio": 0, "document": 0,
        "spreadsheet": 0, "JSON": 0, "CSV": 0, "XML": 0, "YAML": 0,
        "markdown": 0, "HTML": 0, "CSS": 0, "JavaScript": 0, "Python": 0
    }
    
    # 分析每个搜索结果
    for query, results in search_results.items():
        for result in results:
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            content = f"{title} {snippet}"
            
            for keyword in keywords:
                if keyword.lower() in content:
                    keywords[keyword] += 1
    
    # 按频率排序
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords

def generate_report(search_results, trends):
    """生成分析报告"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""# 市场需求分析报告
生成时间: {timestamp}

## 热门趋势关键词
"""
    
    # 添加前10个热门关键词
    for i, (keyword, count) in enumerate(trends[:10], 1):
        report += f"{i}. **{keyword}**: {count}次提及\n"
    
    report += "\n## 详细搜索结果\n"
    
    for query, results in search_results.items():
        report += f"\n### {query}\n"
        if results:
            for i, result in enumerate(results[:3], 1):
                title = result.get("title", "无标题")
                snippet = result.get("snippet", "无摘要")
                url = result.get("url", "#")
                report += f"{i}. [{title}]({url})\n   {snippet}\n"
        else:
            report += "无结果\n"
    
    report += """
## 推荐项目方向
基于以上分析，建议开发以下类型的API服务：

1. **AI相关API**
   - 文本生成/处理
   - 图像识别/生成
   - 语音识别/合成

2. **文件处理API**
   - 文档转换（PDF、Word、Excel）
   - 图片处理（压缩、格式转换）
   - 数据格式转换（JSON、CSV、XML）

3. **开发者工具API**
   - 代码格式化/验证
   - API测试/监控
   - 自动化部署工具

4. **业务效率API**
   - 支付处理
   - 用户认证
   - 数据分析

## 下一步行动
1. 选择1-2个高需求领域
2. 设计API接口
3. 开发原型
4. 测试部署
"""
    
    return report

def main():
    """主函数"""
    
    print("开始市场需求分析...")
    
    # 执行搜索分析
    search_results = analyze_market_demand()
    
    # 分析趋势
    trends = analyze_trends(search_results)
    
    # 生成报告
    report = generate_report(search_results, trends)
    
    # 保存报告
    report_path = f"/home/lanxuan86/auto-api-system/logs/market-analysis-{datetime.now().strftime('%Y%m%d')}.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"分析完成，报告已保存到: {report_path}")
    
    # 输出摘要
    print("\n=== 市场趋势摘要 ===")
    for i, (keyword, count) in enumerate(trends[:5], 1):
        print(f"{i}. {keyword}: {count}次提及")
    
    return report_path

if __name__ == "__main__":
    main()