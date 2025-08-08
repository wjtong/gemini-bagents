#!/usr/bin/env python3
"""
依赖版本检查脚本

这个脚本用于检查项目依赖的版本是否正确安装。
"""

import sys
import importlib
from typing import Dict, List, Tuple

def check_package_version(package_name: str, min_version: str = None) -> Tuple[bool, str]:
    """检查包的版本"""
    try:
        module = importlib.import_module(package_name)
        version = getattr(module, '__version__', 'unknown')
        
        if min_version:
            # 处理beta版本的特殊情况
            if 'b' in min_version or 'beta' in min_version:
                # 对于beta版本，检查是否完全匹配
                if version != min_version:
                    return False, f"版本不匹配: {version} (需要 == {min_version})"
            else:
                # 简单的版本比较（仅支持主版本号）
                try:
                    current_major = int(version.split('.')[0])
                    required_major = int(min_version.split('.')[0])
                    if current_major < required_major:
                        return False, f"版本过低: {version} (需要 >= {min_version})"
                except (ValueError, IndexError):
                    pass
        
        return True, version
    except ImportError:
        return False, "未安装"

def check_dependencies() -> Dict[str, Tuple[bool, str]]:
    """检查所有依赖"""
    dependencies = {
        # 核心依赖
        "langgraph": ("langgraph", "0.2.6"),
        "langchain": ("langchain", "0.3.19"),
        "langchain_openai": ("langchain_openai", None),
        
        # PandasAI相关
        "pandasai": ("pandasai", "3.0.0-beta.18"),
        "pandasai_litellm": ("pandasai_litellm", "0.0.1"),
        "pandasai_sql": ("pandasai_sql", "0.1.7"),
        
        # 数据库相关
        "psycopg2": ("psycopg2", None),
        "pandas": ("pandas", "2.0.0"),
        "sqlalchemy": ("sqlalchemy", "2.0.0"),
        
        # 其他依赖
        "openpyxl": ("openpyxl", "3.1.5"),
        "python_dotenv": ("dotenv", "1.0.1"),
        "fastapi": ("fastapi", None),
        "openai": ("openai", None),
    }
    
    results = {}
    for name, (package, min_version) in dependencies.items():
        success, version = check_package_version(package, min_version)
        results[name] = (success, version)
    
    return results

def print_results(results: Dict[str, Tuple[bool, str]]):
    """打印检查结果"""
    print("🔍 依赖版本检查结果")
    print("=" * 50)
    
    all_passed = True
    
    for package_name, (success, version) in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {package_name}: {version}")
        if not success:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 所有依赖检查通过！")
    else:
        print("⚠️  部分依赖有问题，请检查安装。")
        print("\n建议操作：")
        print("1. 运行: pip install -e .")
        print("2. 检查: pip list | grep pandasai")
        print("3. 参考: backend/INSTALL.md")
    
    return all_passed

def check_optional_dependencies() -> Dict[str, Tuple[bool, str]]:
    """检查可选依赖"""
    optional_deps = {
        "mypy": ("mypy", "1.11.1"),
        "ruff": ("ruff", "0.6.1"),
        "pytest": ("pytest", "8.3.5"),
    }
    
    results = {}
    for name, (package, min_version) in optional_deps.items():
        success, version = check_package_version(package, min_version)
        results[name] = (success, version)
    
    return results

def print_optional_results(results: Dict[str, Tuple[bool, str]]):
    """打印可选依赖检查结果"""
    print("\n🔍 可选依赖检查结果")
    print("=" * 50)
    
    for package_name, (success, version) in results.items():
        status = "✅" if success else "⚠️"
        print(f"{status} {package_name}: {version}")
    
    print("=" * 50)

def main():
    """主函数"""
    print("🚀 开始依赖版本检查...\n")
    
    # 检查核心依赖
    results = check_dependencies()
    core_passed = print_results(results)
    
    # 检查可选依赖
    optional_results = check_optional_dependencies()
    print_optional_results(optional_results)
    
    # 返回状态码
    sys.exit(0 if core_passed else 1)

if __name__ == "__main__":
    main()
