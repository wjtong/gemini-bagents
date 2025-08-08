# 依赖安装说明

## 概述

本项目使用PandasAI 3.0进行数据分析功能。以下是详细的安装和配置说明。

## 核心依赖

### 基础依赖
```bash
pip install -e .
```

### 手动安装依赖（如果需要）
```bash
# LangGraph和LangChain
pip install langgraph>=0.2.6 langchain>=0.3.19 langchain-openai

# PandasAI相关
pip install pandasai==3.0.0-beta.18
pip install pandasai-litellm>=0.0.1
pip install "pandasai-sql[postgres]>=0.1.7"
pip install openpyxl>=3.1.5

# 数据库相关
pip install psycopg2-binary>=2.9.0
pip install pandas>=2.0.0
pip install sqlalchemy>=2.0.0

# 其他依赖
pip install python-dotenv>=1.0.1
pip install fastapi
pip install openai
```

## 版本兼容性

### PandasAI 3.0.0-beta.18
- 使用PandasAI 3.0.0-beta.18版本（Beta版本）
- 支持PostgreSQL数据库连接
- 支持自然语言查询转换
- 支持Excel文件处理

### 数据库支持
- PostgreSQL (主要支持)
- MySQL (通过pandasai-sql扩展)
- SQLite (基础支持)

### Python版本
- Python 3.11+
- 推荐使用Python 3.11或3.12

## 环境配置

### 必需的环境变量
```bash
# OpenAI API
OPENAI_API_KEY=your_api_key_here

# PostgreSQL数据库
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5432
POSTGRESQL_DATABASE=your_database
POSTGRESQL_USERNAME=your_username
POSTGRESQL_PASSWORD=your_password

# PandasAI配置
PANDASAI_TABLES=table1,table2,table3
PANDASAI_MODEL=gpt-4o-mini
```

### 可选的环境变量
```bash
# 自定义OpenAI API端点
OPENAI_API_BASE=https://api.openai.com/v1

# Agent配置
QUERY_GENERATOR_MODEL=gpt-4o-mini
REFLECTION_MODEL=gpt-4o
ANSWER_MODEL=gpt-4o
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2
```

## 测试安装

### 1. 基础功能测试
```bash
cd backend
python examples/test_data_analysis.py
```

### 2. 数据分析示例
```bash
cd backend
python examples/data_analysis_example.py
```

### 3. 使用Makefile
```bash
# 测试数据分析功能
make test-data-analysis

# 运行数据分析示例
make example-data-analysis
```

## 故障排除

### 常见问题

1. **PandasAI导入错误**
   ```bash
   # 确保安装了正确的版本
   pip install pandasai>=3.0.0
   ```

2. **数据库连接失败**
   - 检查PostgreSQL服务是否运行
   - 验证连接参数是否正确
   - 确认用户权限

3. **OpenAI API错误**
   - 检查API密钥是否正确
   - 确认API配额是否充足
   - 验证网络连接

4. **依赖冲突**
   ```bash
   # 清理并重新安装
   pip uninstall pandasai pandasai-litellm pandasai-sql
   pip install -e .
   ```

### 调试模式

启用详细日志：
```bash
export PANDASAI_VERBOSE=true
python examples/test_data_analysis.py
```

## 开发环境

### 开发依赖
```bash
pip install -e ".[dev]"
```

### 代码格式化
```bash
# 使用ruff格式化
ruff format .

# 使用ruff检查
ruff check .
```

## 生产部署

### Docker部署
```bash
# 构建镜像
docker build -t agent-backend .

# 运行容器
docker run -p 2024:2024 agent-backend
```

### 环境变量管理
```bash
# 使用.env文件
cp .env.example .env
# 编辑.env文件配置环境变量
```

## 更新依赖

### 更新PandasAI
```bash
pip install pandasai==3.0.0-beta.18
pip install --upgrade pandasai-litellm
pip install --upgrade "pandasai-sql[postgres]"
```

### 更新所有依赖
```bash
pip install --upgrade -e .
```

## 支持

如果遇到问题，请：

1. 检查环境变量配置
2. 运行测试脚本验证功能
3. 查看详细错误日志
4. 参考[DATA_ANALYSIS_SETUP.md](DATA_ANALYSIS_SETUP.md)文档
