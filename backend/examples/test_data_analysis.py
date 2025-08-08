#!/usr/bin/env python3
"""
数据分析功能测试脚本

这个脚本用于测试PandasAI数据分析功能是否正常工作。
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent.configuration import Configuration
from src.agent.utils import get_table_schema, get_database_connection
from pandasai import PandasAI
from pandasai.llm.litellm import LiteLLM

def test_database_connection():
    """测试数据库连接"""
    print("🔍 测试数据库连接...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        connection = get_database_connection(config)
        print("✅ 数据库连接成功")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

def test_table_schema():
    """测试表结构获取"""
    print("\n🔍 测试表结构获取...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        schema = get_table_schema(config)
        if schema:
            print("✅ 表结构获取成功")
            for table_name, table_info in schema.items():
                print(f"   📊 表: {table_name}")
                print(f"     列数: {len(table_info['columns'])}")
                print(f"     行数: {table_info['row_count']}")
                print(f"     主键: {table_info['primary_keys']}")
        else:
            print("⚠️  没有找到可用的表")
        return True
    except Exception as e:
        print(f"❌ 表结构获取失败: {str(e)}")
        return False

def test_pandasai():
    """测试PandasAI功能"""
    print("\n🔍 测试PandasAI功能...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        # 初始化PandasAI
        pandasai_llm = LiteLLM(
            api_token=os.getenv("OPENAI_API_KEY"),
            model=config.pandasai_model,
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        pandas_ai = PandasAI(
            llm=pandasai_llm,
            verbose=True,
            enforce_privacy=True
        )
        
        print("✅ PandasAI初始化成功")
        
        # 获取表名列表
        table_names = [table.strip() for table in config.pandasai_tables.split(",") if table.strip()]
        
        if not table_names:
            print("⚠️  没有配置要分析的数据库表")
            return False
        
        print(f"📋 配置的表: {', '.join(table_names)}")
        
        # 测试读取第一个表
        if table_names:
            test_table = table_names[0]
            print(f"🔍 测试读取表: {test_table}")
            
            try:
                # 使用pandasai读取表数据
                query = f"SELECT * FROM {test_table} LIMIT 5"
                df = pandas_ai.run(query, dataframes={})
                print(f"✅ 成功读取表 {test_table}")
                print(f"   数据形状: {df.shape if hasattr(df, 'shape') else 'N/A'}")
            except Exception as e:
                print(f"❌ 读取表 {test_table} 失败: {str(e)}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ PandasAI测试失败: {str(e)}")
        return False

def test_simple_analysis():
    """测试简单数据分析"""
    print("\n🔍 测试简单数据分析...")
    
    load_dotenv()
    config = Configuration()
    
    try:
        # 初始化PandasAI
        pandasai_llm = LiteLLM(
            api_token=os.getenv("OPENAI_API_KEY"),
            model=config.pandasai_model,
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        pandas_ai = PandasAI(
            llm=pandasai_llm,
            verbose=True,
            enforce_privacy=True
        )
        
        # 获取表名列表
        table_names = [table.strip() for table in config.pandasai_tables.split(",") if table.strip()]
        
        if not table_names:
            print("⚠️  没有配置要分析的数据库表")
            return False
        
        # 读取所有表
        dataframes = {}
        for table_name in table_names:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pandas_ai.run(query, dataframes={})
                dataframes[table_name] = df
                print(f"✅ 成功读取表: {table_name}")
            except Exception as e:
                print(f"❌ 读取表 {table_name} 失败: {str(e)}")
                continue
        
        if not dataframes:
            print("❌ 没有成功读取任何表")
            return False
        
        # 测试简单分析
        test_query = "显示每个表的基本信息"
        print(f"🔍 执行分析查询: {test_query}")
        
        try:
            result = pandas_ai.run(test_query, dataframes=dataframes)
            print("✅ 数据分析成功")
            print(f"   结果类型: {type(result)}")
            if hasattr(result, 'to_string'):
                print("   结果预览:")
                print(result.to_string()[:500] + "..." if len(result.to_string()) > 500 else result.to_string())
            else:
                print(f"   结果: {str(result)[:500]}...")
        except Exception as e:
            print(f"❌ 数据分析失败: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 简单分析测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 开始数据分析功能测试\n")
    
    # 检查环境变量
    load_dotenv()
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
    
    print("✅ 环境变量检查通过")
    
    # 运行测试
    tests = [
        test_database_connection,
        test_table_schema,
        test_pandasai,
        test_simple_analysis
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
