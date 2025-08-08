# 版本说明

## PandasAI 3.0.0-beta.18

### 版本信息
- **版本**: 3.0.0-beta.18 (Beta版本)
- **发布日期**: 2024年
- **状态**: Beta测试版本

### 主要特性
1. **PostgreSQL支持**: 完整的PostgreSQL数据库连接和分析支持
2. **LiteLLM集成**: 使用LiteLLM作为LLM后端，支持多种模型
3. **自然语言查询**: 支持自然语言转换为SQL查询
4. **多表分析**: 支持同时分析多个数据库表
5. **Excel支持**: 支持Excel文件读取和处理
6. **隐私保护**: 内置数据隐私保护机制

### 兼容性
- **Python**: 3.11+
- **数据库**: PostgreSQL (主要), MySQL, SQLite
- **文件格式**: Excel (.xlsx, .xls), CSV, JSON

### 已知问题
1. **Beta版本**: 这是Beta版本，可能存在一些不稳定性
2. **API变化**: Beta版本中API可能发生变化
3. **功能限制**: 某些高级功能可能尚未完全实现

### 安装说明
```bash
# 安装特定版本
pip install pandasai==3.0.0-beta.18

# 安装相关依赖
pip install pandasai-litellm>=0.0.1
pip install "pandasai-sql[postgres]>=0.1.7"
pip install openpyxl>=3.1.5
```

### 使用示例
```python
from pandasai import PandasAI
from pandasai.llm.litellm import LiteLLM

# 初始化
llm = LiteLLM(api_token="your_openai_api_key")
pandas_ai = PandasAI(llm=llm)

# 分析数据
result = pandas_ai.run("计算销售总额", dataframes=[df])
```

### 更新日志
- 修复了PostgreSQL连接问题
- 改进了自然语言查询处理
- 增强了错误处理机制
- 优化了性能表现

### 注意事项
1. **生产环境**: 建议在生产环境中使用稳定版本
2. **测试**: 充分测试所有功能后再部署
3. **备份**: 重要数据请做好备份
4. **监控**: 密切关注系统性能和错误日志

### 支持
- 官方文档: https://docs.pandas-ai.com/
- GitHub: https://github.com/Sinaptik-AI/pandas-ai
- 问题反馈: GitHub Issues

### 升级建议
- 定期检查新版本发布
- 关注官方更新公告
- 在测试环境中验证新功能
- 制定升级计划和时间表
