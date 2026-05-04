#!/usr/bin/env python3
"""
服务监控脚本
监控3000端口服务的运行状态和性能
"""

import json
import subprocess
import time
from datetime import datetime
import os

def check_service_health():
    """检查服务健康状态"""
    
    try:
        # 检查服务是否响应
        result = subprocess.run(
            ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:3000/health"],
            capture_output=True, text=True, timeout=10
        )
        
        http_code = result.stdout.strip()
        
        if http_code == "200":
            return {
                "status": "healthy",
                "http_code": http_code,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "unhealthy",
                "http_code": http_code,
                "timestamp": datetime.now().isoformat()
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def check_pm2_status():
    """检查PM2进程状态"""
    
    try:
        result = subprocess.run(
            ["/home/lanxuan86/.npm-global/bin/pm2", "jlist"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            processes = json.loads(result.stdout)
            process_info = []
            
            for proc in processes:
                process_info.append({
                    "name": proc.get("name", "unknown"),
                    "pid": proc.get("pid", 0),
                    "status": proc.get("pm2_env", {}).get("status", "unknown"),
                    "uptime": proc.get("pm2_env", {}).get("pm_uptime", 0),
                    "restarts": proc.get("pm2_env", {}).get("restart_time", 0)
                })
            
            return {
                "status": "success",
                "processes": process_info,
                "count": len(process_info)
            }
        else:
            return {
                "status": "error",
                "error": result.stderr
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

def check_system_resources():
    """检查系统资源使用情况"""
    
    try:
        # 检查内存使用
        memory_result = subprocess.run(
            ["free", "-m"],
            capture_output=True, text=True
        )
        
        # 检查CPU使用
        cpu_result = subprocess.run(
            ["top", "-bn1"],
            capture_output=True, text=True
        )
        
        # 检查磁盘使用
        disk_result = subprocess.run(
            ["df", "-h", "/"],
            capture_output=True, text=True
        )
        
        return {
            "memory": memory_result.stdout,
            "cpu": cpu_result.stdout[:500],  # 只取前500字符
            "disk": disk_result.stdout
        }
        
    except Exception as e:
        return {
            "error": str(e)
        }

def generate_monitoring_report():
    """生成监控报告"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 检查各项状态
    health = check_service_health()
    pm2 = check_pm2_status()
    resources = check_system_resources()
    
    report = f"""# 服务监控报告
生成时间: {timestamp}

## 服务健康状态
- **状态**: {health['status']}
- **HTTP代码**: {health.get('http_code', 'N/A')}
- **时间戳**: {health['timestamp']}

## PM2进程状态
- **状态**: {pm2['status']}
- **进程数量**: {pm2.get('count', 'N/A')}

### 进程详情
"""
    
    if pm2['status'] == 'success':
        for proc in pm2['processes']:
            report += f"- **{proc['name']}** (PID: {proc['pid']}): {proc['status']}\n"
    
    report += f"""
## 系统资源
{resources.get('error', '无错误')}

### 内存使用
```
{resources.get('memory', '无数据')}
```

### 磁盘使用
```
{resources.get('disk', '无数据')}
```

## 建议
"""
    
    if health['status'] != 'healthy':
        report += "- ⚠️ 服务不健康，建议检查日志并重启服务\n"
    
    if pm2['status'] != 'success':
        report += "- ⚠️ PM2进程异常，建议检查PM2状态\n"
    
    report += """
## 自动重启命令
如果服务异常，可以使用以下命令重启：
```bash
/home/lanxuan86/.npm-global/bin/pm2 restart x402-api-service
```
"""
    
    return report, health['status'] == 'healthy'

def main():
    """主函数"""
    
    print("生成监控报告...")
    
    report, is_healthy = generate_monitoring_report()
    
    # 保存报告
    report_path = f"/home/lanxuan86/auto-api-system/logs/monitoring-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"监控报告已保存: {report_path}")
    
    # 如果不健康，尝试重启
    if not is_healthy:
        print("⚠️ 服务不健康，尝试重启...")
        try:
            subprocess.run(
                ["/home/lanxuan86/.npm-global/bin/pm2", "restart", "x402-api-service"],
                capture_output=True
            )
            print("✅ 服务已重启")
        except Exception as e:
            print(f"❌ 重启失败: {e}")
    
    return report_path

if __name__ == "__main__":
    main()