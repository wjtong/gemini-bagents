# 从Gemini到OpenAI GPT的迁移总结

## 概述
本项目已成功从Google Gemini模型迁移到OpenAI GPT模型。以下是所做的主要更改：

## 主要更改

### 1. 依赖项更新 (`backend/pyproject.toml`)
- 移除了 `langchain-google-genai` 和 `google-genai`
- 添加了 `langchain-openai` 和 `openai`

### 2. 配置文件更新 (`backend/src/agent/configuration.py`)
- `query_generator_model`: `gemini-2.0-flash` → `gpt-4o-mini`
- `reflection_model`: `gemini-2.5-flash` → `gpt-4o`
- `answer_model`: `gemini-2.5-pro` → `gpt-4o`
- 新增 `openai_api_base`: 支持自定义OpenAI兼容API端点

### 3. 核心代码更新 (`backend/src/agent/graph.py`)
- 导入更改：`from google.genai import Client` → `from openai import OpenAI`
- 导入更改：`from langchain_google_genai import ChatGoogleGenerativeAI` → `from langchain_openai import ChatOpenAI`
- API密钥环境变量：`GEMINI_API_KEY` → `OPENAI_API_KEY`
- 新增base URL支持：所有LLM实例都支持`base_url`参数，使用`OPENAI_API_BASE`环境变量
- 更新了所有LLM实例化代码
- 简化了web_research函数（移除了Google Search API的特定实现）

### 4. 工具函数更新 (`backend/src/agent/utils.py`)
- 更新了 `get_citations` 函数以适配OpenAI API结构
- 更新了 `resolve_urls` 函数的URL前缀

### 5. 前端更新
- `frontend/src/components/WelcomeScreen.tsx`: 更新了Powered by描述
- `frontend/src/components/InputForm.tsx`: 更新了模型选项
  - `gemini-2.0-flash` → `gpt-4o-mini`
  - `gemini-2.5-flash-preview-04-17` → `gpt-4o`
  - `gemini-2.5-pro-preview-05-06` → `gpt-4-turbo`

### 6. 配置文件更新
- `docker-compose.yml`: 更新环境变量和镜像名称，新增`OPENAI_API_BASE`支持
- `README.md`: 更新了所有Gemini相关的描述和说明，添加base URL配置说明
- `backend/examples/cli_research.py`: 更新默认模型，新增`--openai-api-base`参数

### 7. 文档更新
- 更新了项目标题和描述
- 更新了技术栈说明
- 更新了部署说明

## 注意事项

### Web搜索功能
由于OpenAI的API结构与Gemini不同，web搜索功能已被简化。在当前的实现中：
- 移除了Google Search API的特定集成
- 使用简化的搜索响应结构
- 可能需要进一步集成其他搜索API

### 环境变量
用户需要将环境变量从 `GEMINI_API_KEY` 更改为 `OPENAI_API_KEY`
可选设置 `OPENAI_API_BASE` 用于自定义OpenAI兼容的API端点

### 模型选择
前端现在提供以下OpenAI模型选项：
- GPT-4o Mini (快速、经济)
- GPT-4o (平衡性能和成本)
- GPT-4 Turbo (最高性能)

### Base URL配置
- 支持通过环境变量 `OPENAI_API_BASE` 设置自定义API端点
- 支持通过CLI参数 `--openai-api-base` 设置自定义API端点
- 支持通过配置类设置自定义API端点

## 测试建议

1. 确保设置了正确的 `OPENAI_API_KEY` 环境变量
2. 测试前端模型选择功能
3. 验证后端API调用是否正常工作
4. 测试Docker部署流程
5. 测试自定义base URL配置

## 后续工作

1. 集成适当的web搜索API
2. 优化citation处理逻辑
3. 添加更多OpenAI模型选项
4. 性能测试和优化