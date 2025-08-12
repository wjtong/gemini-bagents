#!/usr/bin/env python3
"""
数据分析功能使用示例

这个脚本展示了如何使用数据分析功能（当前为dummy实现）。
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
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请参考 README.md 文件进行配置")
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
    print("注意：当前使用dummy实现，实际数据分析功能已暂时移除")
    print("=" * 50)
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📊 示例 {i}: {query}")
        print("-" * 30)
        
        try:
            # 创建消息
            messages = [HumanMessage(content=query)]
            
            # 运行分析
            result = graph.invoke({
                "messages": messages,
                "initial_search_query_count": 2,
                "max_research_loops": 1,
                "reasoning_model": "gpt-4o",
            })
            
            # 显示结果
            if result.get("messages"):
                answer = result["messages"][-1].content
                print(f"✅ 分析结果:")
                print(answer[:500] + "..." if len(answer) > 500 else answer)
            else:
                print("❌ 没有生成分析结果")
                
        except Exception as e:
            print(f"❌ 分析失败: {str(e)}")
    
    print("\n🎉 数据分析示例完成！")

if __name__ == "__main__":
    run_data_analysis_example() 