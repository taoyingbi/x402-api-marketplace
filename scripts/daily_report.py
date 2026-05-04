#!/usr/bin/env python3
"""
每日报告生成脚本
汇总市场分析、项目部署和服务监控信息
"""

import json
import os
from datetime import datetime
import subprocess

def read_latest_file(directory, prefix):
    """读取最新的文件"""
    
    try:
        files = []
        for f in os.listdir(directory):
            if f.startswith(prefix) and f.endswith('.md'):
                files.append(f)
        
        if not files:
            return None
        
        # 按文件名排序（包含日期）
        latest_file = sorted(files)[-1]
        file_path = os.path.join(directory, latest_file)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        return f"读取失败: {e}"

def read_deployment_log():
    """读取部署日志"""
    
    try:
        log_path = f"/home/lanxuan86/auto-api-system/logs/deployment-{datetime.now().strftime('%Y%m%d')}.json"
        
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return None
            
    except Exception as e:
        return {"error": str(e)}

def generate_daily_report():
    """生成每日报告"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.now().strftime("%Y%m%d")
    
    # 读取市场分析报告
    market_report = read_latest_file(
        "/home/lanxuan86/auto-api-system/logs",
        "market-analysis-"
    )
    
    # 读取监控报告
    monitoring_report = read_latest_file(
        "/home/lanxuan86/auto-api-system/logs",
        "monitoring-"
    )
    
    # 读取部署日志
    deployment_log = read_deployment_log()
    
    report = f"""# 每日自动化API服务管理报告
日期: {timestamp}

## 📊 市场趋势分析
"""
    
    if market_report:
        # 提取关键信息
        lines = market_report.split('\n')
        for line in lines[:20]:  # 只取前20行
            if line.strip():
                report += f"{line}\n"
    else:
        report += "暂无市场分析数据\n"
    
    report += f"""
## 🚀 项目部署状态
"""
    
    if deployment_log and 'error' not in deployment_log:
        report += f"- **项目类型**: {deployment_log.get('project_type', 'N/A')}\n"
        report += f"- **项目路径**: {deployment_log.get('project_path', 'N/A')}\n"
        report += f"- **部署时间**: {deployment_log.get('timestamp', 'N/A')}\n"
        
        template = deployment_log.get('template', {})
        if template:
            report += f"- **项目名称**: {template.get('name', 'N/A')}\n"
            report += f"- **项目描述**: {template.get('description', 'N/A')}\n"
            report += f"- **价格**: {template.get('price', 'N/A')}\n"
    else:
        report += "暂无部署数据\n"
    
    report += f"""
## 🔍 服务监控状态
"""
    
    if monitoring_report:
        # 提取健康状态
        for line in monitoring_report.split('\n'):
            if '**状态**:' in line:
                report += f"{line}\n"
                break
    else:
        report += "暂无监控数据\n"
    
    report += f"""
## 📈 今日关键指标
- **市场分析**: {'✅ 已完成' if market_report else '❌ 未完成'}
- **项目部署**: {'✅ 已完成' if deployment_log and 'error' not in deployment_log else '❌ 未完成'}
- **服务监控**: {'✅ 正常' if monitoring_report and 'healthy' in monitoring_report.lower() else '⚠️ 需要关注'}

## 🎯 明日计划
1. 继续监控市场趋势
2. 优化现有API服务
3. 开发新的API端点
4. 提升服务性能

---
*报告自动生成于 {timestamp}*
"""
    
    return report

def main():
    """主函数"""
    
    print("生成每日报告...")
    
    report = generate_daily_report()
    
    # 保存报告
    report_path = f"/home/lanxuan86/auto-api-system/logs/daily-report-{datetime.now().strftime('%Y%m%d')}.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"每日报告已保存: {report_path}")
    
    # 输出摘要
    print("\n=== 每日报告摘要 ===")
    lines = report.split('\n')
    for line in lines[:30]:
        if line.strip():
            print(line)
    
    return report_path

if __name__ == "__main__":
    main()