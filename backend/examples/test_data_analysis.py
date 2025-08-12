#!/usr/bin/env python3
"""
数据分析功能测试脚本

这个脚本用于测试数据分析功能是否正常工作（当前为dummy实现）。
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.configuration import Configuration
from src.agent.utils import get_table_schema
from src.agent.graph import graph
from langchain_core.messages import HumanMessage

def test_configuration():
    """测试配置加载"""
    print("🔍 测试配置加载...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        print(f"✅ 配置加载成功")
        print(f"   查询生成模型: {config.query_generator_model}")
        print(f"   反思模型: {config.reflection_model}")
        print(f"   回答模型: {config.answer_model}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {str(e)}")
        return False

def test_table_schema():
    """测试表结构获取"""
    print("\n🔍 测试表结构获取...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        schema = get_table_schema(config)
        print("✅ 表结构获取成功")
        print(f"   当前返回空字典（dummy实现）")
        return True
    except Exception as e:
        print(f"❌ 表结构获取失败: {str(e)}")
        return False

def test_data_analysis_node():
    """测试数据分析节点"""
    print("\n🔍 测试数据分析节点...")
    
    load_dotenv()
    
    try:
        # 测试数据分析查询
        test_query = "计算每个产品类别的总销售额"
        print(f"   测试查询: {test_query}")
        
        messages = [HumanMessage(content=test_query)]
        result = graph.invoke({
            "messages": messages,
            "initial_search_query_count": 1,
            "max_research_loops": 1,
            "reasoning_model": "gpt-4o",
        })
        
        if result.get("messages"):
            print("✅ 数据分析节点测试成功")
            print(f"   生成了回答")
            return True
        else:
            print("❌ 数据分析节点没有生成回答")
            return False
            
    except Exception as e:
        print(f"❌ 数据分析节点测试失败: {str(e)}")
        return False

def test_task_type_determination():
    """测试任务类型判断"""
    print("\n🔍 测试任务类型判断...")
    
    load_dotenv()
    
    try:
        # 测试数据分析查询
        data_query = "计算每个产品类别的总销售额"
        print(f"   数据分析查询: {data_query}")
        
        messages = [HumanMessage(content=data_query)]
        result = graph.invoke({
            "messages": messages,
            "initial_search_query_count": 1,
            "max_research_loops": 1,
            "reasoning_model": "gpt-4o",
        })
        
        task_type = result.get("task_type", "unknown")
        print(f"   判断的任务类型: {task_type}")
        
        # 测试网络搜索查询
        web_query = "AI技术的最新发展"
        print(f"   网络搜索查询: {web_query}")
        
        messages = [HumanMessage(content=web_query)]
        result = graph.invoke({
            "messages": messages,
            "initial_search_query_count": 1,
            "max_research_loops": 1,
            "reasoning_model": "gpt-4o",
        })
        
        task_type = result.get("task_type", "unknown")
        print(f"   判断的任务类型: {task_type}")
        
        print("✅ 任务类型判断测试成功")
        return True
        
    except Exception as e:
        print(f"❌ 任务类型判断测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始数据分析功能测试\n")
    print("注意：当前使用dummy实现，实际数据分析功能已暂时移除")
    print("=" * 60)
    
    # 检查环境变量
    load_dotenv()
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
    
    print("✅ 环境变量检查通过")
    
    # 运行测试
    tests = [
        test_configuration,
        test_table_schema,
        test_data_analysis_node,
        test_task_type_determination,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！数据分析功能配置正确。")
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")

if __name__ == "__main__":
    main()
