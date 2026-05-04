#!/usr/bin/env python3
"""
主控制脚本
整合市场需求分析和项目生成的完整流程
"""

import sys
import os
from datetime import datetime

# 添加脚本路径
sys.path.insert(0, '/home/lanxuan86/auto-api-system/scripts')

from market_analysis import main as analyze_market
from project_generator import main as generate_project

def run_full_cycle():
    """运行完整的自动化周期"""
    
    print("=" * 60)
    print(f"自动化API服务管理系统 - 完整周期")
    print(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 第一步：市场需求分析
        print("\n[1/2] 执行市场需求分析...")
        report_path = analyze_market()
        print(f"✅ 市场分析完成，报告: {report_path}")
        
        # 第二步：生成并部署新项目
        print("\n[2/2] 生成并部署新项目...")
        project_path = generate_project()
        print(f"✅ 项目部署完成: {project_path}")
        
        print("\n" + "=" * 60)
        print("✅ 完整周期执行成功！")
        print("=" * 60)
        
        # 验证服务
        print("\n验证服务状态...")
        import subprocess
        result = subprocess.run(
            ["curl", "-s", "http://localhost:3000/health"],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"✅ 服务正常运行: {result.stdout}")
        else:
            print("⚠️ 服务可能未正常启动，请检查日志")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_full_cycle()
    sys.exit(0 if success else 1)