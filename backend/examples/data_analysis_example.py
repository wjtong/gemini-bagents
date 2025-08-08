#!/usr/bin/env python3
"""
数据分析功能使用示例

这个脚本展示了如何使用PandasAI进行数据分析。
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.graph import graph
from langchain_core.messages import HumanMessage

def run_data_analysis_example():
    """运行数据分析示例"""
    
    # 加载环境变量
    load_dotenv()
    
    # 检查必要的环境变量
    required_vars = [
        "OPENAI_API_KEY",
        "POSTGRESQL_HOST",
        "POSTGRESQL_DATABASE",
        "POSTGRESQL_USERNAME",
        "POSTGRESQL_PASSWORD",
        "PANDASAI_TABLES"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请参考 DATA_ANALYSIS_SETUP.md 文件进行配置")
        return
    
    # 示例查询
    example_queries = [
        "计算每个产品类别的总销售额",
        "显示各地区的平均客户满意度评分",
        "分析过去一年的月度收入趋势",
        "比较不同部门的绩效表现",
        "计算用户留存率",
        "分析销售数据的季节性模式"
    ]
    
    print("🚀 数据分析功能示例")
    print("=" * 50)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📊 示例 {i}: {query}")
        print("-" * 30)
        
        try:
            # 创建消息
            messages = [HumanMessage(content=query)]
            
            # 运行图
            result = graph.invoke({"messages": messages})
            
            # 获取结果
            if result.get("messages"):
                answer = result["messages"][-1].content
                print(f"✅ 回答: {answer}")
            else:
                print("❌ 没有获得回答")
                
        except Exception as e:
            print(f"❌ 执行失败: {str(e)}")
        
        print()

def main():
    """主函数"""
    print("数据分析功能使用示例")
    print("请确保已正确配置PostgreSQL数据库和PandasAI")
    print("参考 DATA_ANALYSIS_SETUP.md 进行配置\n")
    
    run_data_analysis_example()

if __name__ == "__main__":
    main() 