# 数据分析功能说明

## 概述

我们在LangGraph研究代理中添加了智能数据分析功能。现在代理能够自动判断用户查询是需要网络研究还是数据分析，并相应地执行不同的处理流程。

## 新增功能

### 1. 任务类型判断
- 新增 `determine_task_type` 节点，使用LLM分析用户查询
- 自动判断是执行网络研究还是数据分析
- 支持两种任务类型：`web_research` 和 `data_analysis`

### 2. 数据分析节点
- 新增 `data_analysis` 节点，专门处理数值分析查询
- 新增 `generate_data_analysis_query` 节点，生成数据分析查询
- 新增 `continue_to_data_analysis` 节点，路由数据分析查询

### 3. 状态管理
- 在 `OverallState` 中添加 `data_analysis_result` 字段
- 新增 `DataAnalysisState` 类型定义
- 支持数据分析结果的合并和引用

### 4. 提示词优化
- 新增 `task_type_instructions`：任务类型判断提示词
- 新增 `data_analysis_instructions`：数据分析查询生成提示词
- 新增 `data_analyzer_instructions`：数据分析执行提示词

### 5. 模式定义
- 新增 `TaskType` 模式：任务类型判断结果
- 新增 `DataAnalysisQuery` 模式：数据分析查询结果

## 工作流程

### 新的工作流程
1. **任务类型判断** (`determine_task_type`)
   - 分析用户查询
   - 判断是网络研究还是数据分析

2. **查询生成**
   - 网络研究：`generate_query` → `continue_to_web_research`
   - 数据分析：`generate_data_analysis_query` → `continue_to_data_analysis`

3. **执行研究/分析**
   - 网络研究：`web_research` 节点
   - 数据分析：`data_analysis` 节点

4. **反思和迭代**
   - `reflection` 节点分析结果
   - 根据原始任务类型决定后续查询类型

5. **最终答案**
   - `finalize_answer` 节点合并所有结果

### 任务类型判断规则

**网络研究查询示例：**
- "What are the latest developments in AI technology?"
- "What are the benefits of renewable energy?"
- "How does machine learning work?"

**数据分析查询示例：**
- "What is the current stock price of Apple?"
- "Calculate the compound annual growth rate of Tesla stock over the past 5 years"
- "How has the population of New York changed in the last decade?"

## 文件修改

### 核心文件
- `backend/src/agent/graph.py`：添加数据分析节点和路由逻辑
- `backend/src/agent/state.py`：添加数据分析相关状态
- `backend/src/agent/tools_and_schemas.py`：添加数据分析相关模式
- `backend/src/agent/prompts.py`：添加数据分析相关提示词

### 示例和测试
- `backend/test_data_analysis.py`：数据分析功能测试
- `backend/examples/data_analysis_example.py`：数据分析示例
- `README.md`：更新文档说明新功能

## 使用方法

### 命令行测试
```bash
cd backend
python test_data_analysis.py
```

### 示例运行
```bash
cd backend
python examples/data_analysis_example.py
```

### 自定义查询
```bash
cd backend
python examples/cli_research.py "What is the current stock price of Apple?"
```

## 技术特点

1. **智能路由**：LLM自动判断查询类型
2. **并行处理**：支持多个查询的并行执行
3. **结果合并**：网络研究和数据分析结果统一处理
4. **引用管理**：支持数据分析结果的引用标记
5. **迭代优化**：支持多轮查询优化

## 扩展性

该架构设计支持未来添加更多任务类型：
- 图像分析
- 文档处理
- 代码分析
- 等等

只需要：
1. 添加新的任务类型判断逻辑
2. 创建对应的节点函数
3. 更新状态管理和路由逻辑
4. 添加相应的提示词和模式定义 