# 数据分析功能配置指南

## 概述

本项目集成了PandasAI 3.0版本，支持对PostgreSQL数据库中的表进行智能数据分析。当用户查询涉及数值计算、统计分析或数据比较时，系统会自动选择数据分析节点进行处理。

## 环境变量配置

在`.env`文件中添加以下配置：

### OpenAI API配置
```bash
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1  # 可选，自定义API端点
```

### PostgreSQL数据库配置
```bash
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=your_database_name
POSTGRESQL_USERNAME=your_username
POSTGRESQL_PASSWORD=your_password
```

### PandasAI配置
```bash
PANDASAI_TABLES=users,orders,products  # 要分析的数据库表名，多个表用逗号分隔
PANDASAI_MODEL=gpt-4o-mini  # PandasAI使用的模型
```

### Agent配置
```bash
QUERY_GENERATOR_MODEL=gpt-4o-mini
REFLECTION_MODEL=gpt-4o
ANSWER_MODEL=gpt-4o
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2
```

## 功能特性

### 自动任务类型判断
- 系统会自动分析用户查询，判断是进行网络搜索还是数据分析
- 数据分析查询包括：计算、统计、数值比较、聚合、趋势分析、财务数据、销售数据等

### 数据库表结构获取
- 系统启动时会自动获取配置的数据库表结构信息
- 包括表名、列信息、数据类型、主键、索引、行数等
- 这些信息用于判断查询是否适合通过数据分析处理

### PandasAI集成
- 使用PandasAI 3.0版本进行智能数据分析
- 支持自然语言查询转换为SQL和数据操作
- 自动处理DataFrame结果并转换为可读格式

## 使用示例

### 数据分析查询示例
- "计算每个产品类别的总销售额"
- "显示各地区的平均客户满意度评分"
- "分析过去一年的月度收入趋势"
- "比较不同部门的绩效表现"
- "计算用户留存率"
- "分析销售数据的季节性模式"

### 网络搜索查询示例
- "AI技术的最新发展"
- "可再生能源的优势"
- "当前苹果股票价格"
- "最新科技新闻"

## 安装依赖

确保安装了所需的Python包：

```bash
pip install pandasai==3.0.0-beta.18 pandasai-litellm>=0.0.1 pandasai-sql[postgres]>=0.1.7 openpyxl>=3.1.5 psycopg2-binary>=2.9.0 pandas>=2.0.0 sqlalchemy>=2.0.0
```

## 注意事项

1. **数据库连接**：确保PostgreSQL数据库正在运行且可访问
2. **表权限**：确保配置的用户有读取指定表的权限
3. **API密钥**：确保OpenAI API密钥有效且有足够配额
4. **表名配置**：多个表名用逗号分隔，不要包含空格
5. **错误处理**：如果数据分析失败，系统会返回错误信息并继续处理

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查数据库服务是否运行
   - 验证连接参数是否正确
   - 确认网络连接正常

2. **表读取失败**
   - 检查表名是否正确
   - 确认用户有读取权限
   - 验证表是否存在

3. **PandasAI分析失败**
   - 检查OpenAI API密钥
   - 确认模型名称正确
   - 查看详细错误日志

4. **任务类型判断错误**
   - 检查查询是否包含数据分析关键词
   - 确认数据库表结构是否正确获取
   - 验证环境变量配置
