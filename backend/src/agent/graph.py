import os

from agent.tools_and_schemas import SearchQueryList, Reflection, TaskType, DataAnalysisQuery
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
from langgraph.types import Send
from langgraph.graph import StateGraph
from langgraph.graph import START, END
from langchain_core.runnables import RunnableConfig
from openai import OpenAI
from pandasai import PandasAI
from pandasai_litellm.litellm import LiteLLM

from agent.state import (
    OverallState,
    QueryGenerationState,
    ReflectionState,
    WebSearchState,
    DataAnalysisState,
)
from agent.configuration import Configuration
from agent.prompts import (
    get_current_date,
    query_writer_instructions,
    task_type_instructions,
    data_analysis_instructions,
    web_searcher_instructions,
    data_analyzer_instructions,
    reflection_instructions,
    answer_instructions,
)
from langchain_openai import ChatOpenAI
from agent.utils import (
    get_citations,
    get_research_topic,
    insert_citation_markers,
    resolve_urls,
    get_table_schema,
    can_analyze_with_data_analysis,
)

load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY is not set")

# Used for OpenAI API
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE")  # 支持自定义base URL
)


# Nodes
def determine_task_type(state: OverallState, config: RunnableConfig) -> OverallState:
    """LangGraph node that determines whether to perform web research or data analysis.

    Uses OpenAI GPT to analyze the user's question and determine the appropriate task type.
    Also initializes database schema information for data analysis capabilities.

    Args:
        state: Current graph state containing the User's question
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update, including task_type key and database_schema
    """
    configurable = Configuration.from_runnable_config(config)

    # 获取数据库表结构信息
    database_schema = {}
    try:
        database_schema = get_table_schema(configurable)
    except Exception as e:
        print(f"获取数据库表结构失败: {str(e)}")

    # init OpenAI GPT
    llm = ChatOpenAI(
        model=configurable.query_generator_model,
        temperature=0.5,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    structured_llm = llm.with_structured_output(TaskType)

    # Format the prompt
    formatted_prompt = task_type_instructions.format(
        research_topic=get_research_topic(state["messages"]),
    )
    
    # Determine the task type
    result = structured_llm.invoke(formatted_prompt)
    
    # 如果任务类型是data_analysis，但数据库表结构为空，则改为web_research
    if result.task_type == "data_analysis" and not database_schema:
        result.task_type = "web_research"
    
    return {
        "task_type": result.task_type,
        "database_schema": database_schema
    }


def generate_query(state: OverallState, config: RunnableConfig) -> QueryGenerationState:
    """LangGraph node that generates search queries based on the User's question.

    Uses OpenAI GPT to create an optimized search queries for web research based on
    the User's question.

    Args:
        state: Current graph state containing the User's question
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update, including search_query key containing the generated queries
    """
    configurable = Configuration.from_runnable_config(config)

    # check for custom initial search query count
    if state.get("initial_search_query_count") is None:
        state["initial_search_query_count"] = configurable.number_of_initial_queries

    # init OpenAI GPT
    llm = ChatOpenAI(
        model=configurable.query_generator_model,
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    structured_llm = llm.with_structured_output(SearchQueryList)

    # Format the prompt
    current_date = get_current_date()
    formatted_prompt = query_writer_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        number_queries=state["initial_search_query_count"],
    )
    # Generate the search queries
    result = structured_llm.invoke(formatted_prompt)
    return {"search_query": result.query}


def generate_data_analysis_query(state: OverallState, config: RunnableConfig) -> OverallState:
    """LangGraph node that generates data analysis queries based on the User's question.

    Uses OpenAI GPT to create optimized data analysis queries for numerical analysis.

    Args:
        state: Current graph state containing the User's question
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update, including data_analysis_query key
    """
    configurable = Configuration.from_runnable_config(config)

    # init OpenAI GPT
    llm = ChatOpenAI(
        model=configurable.query_generator_model,
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    structured_llm = llm.with_structured_output(DataAnalysisQuery)

    # Format the prompt
    formatted_prompt = data_analysis_instructions.format(
        research_topic=get_research_topic(state["messages"]),
    )
    
    # Generate the data analysis queries
    result = structured_llm.invoke(formatted_prompt)
    return {"data_analysis_query": result.analysis_query}


def continue_to_web_research(state: QueryGenerationState):
    """LangGraph node that sends the search queries to the web research node.

    This is used to spawn n number of web research nodes, one for each search query.
    """
    return [
        Send("web_research", {"search_query": search_query, "id": int(idx)})
        for idx, search_query in enumerate(state["search_query"])
    ]


def continue_to_data_analysis(state: OverallState):
    """LangGraph node that sends the analysis queries to the data analysis node.

    This is used to spawn n number of data analysis nodes, one for each analysis query.
    """
    return [
        Send("data_analysis", {"analysis_query": analysis_query, "id": int(idx)})
        for idx, analysis_query in enumerate(state["data_analysis_query"])
    ]


def web_research(state: WebSearchState, config: RunnableConfig) -> OverallState:
    """LangGraph node that performs web research using the native Google Search API tool.

    Executes a web search using the native Google Search API tool in combination with OpenAI GPT.

    Args:
        state: Current graph state containing the search query and research loop count
        config: Configuration for the runnable, including search API settings

    Returns:
        Dictionary with state update, including sources_gathered, research_loop_count, and web_research_results
    """
    # Configure
    configurable = Configuration.from_runnable_config(config)
    formatted_prompt = web_searcher_instructions.format(
        current_date=get_current_date(),
        research_topic=state["search_query"],
    )

    # Uses the OpenAI client for web search
    # Note: This is a simplified implementation. You may need to implement
    # a proper web search tool or use a different approach for web search
    response = openai_client.chat.completions.create(
        model=configurable.query_generator_model,
        messages=[{"role": "user", "content": formatted_prompt}],
        temperature=0,
    )
    
    # For now, we'll create a simple response structure
    # In a real implementation, you'd need to integrate with a web search API
    search_result = response.choices[0].message.content or "No search results found."
    
    # Create a simple citation structure
    citations = [{
        "start_index": 0,
        "end_index": len(search_result),
        "segments": [{
            "label": "Web Search",
            "short_url": f"https://search.id/{state['id']}",
            "value": "https://example.com"
        }]
    }]
    
    modified_text = insert_citation_markers(search_result, citations)
    sources_gathered = [item for citation in citations for item in citation["segments"]]

    return {
        "sources_gathered": sources_gathered,
        "search_query": [state["search_query"]],
        "web_research_result": [modified_text],
    }


def data_analysis(state: DataAnalysisState, config: RunnableConfig) -> OverallState:
    """LangGraph node that performs data analysis using PandasAI.

    Executes data analysis using PandasAI to analyze database tables and perform calculations.

    Args:
        state: Current graph state containing the analysis query
        config: Configuration for the runnable, including analysis settings

    Returns:
        Dictionary with state update, including data_analysis_result
    """
    configurable = Configuration.from_runnable_config(config)
    
    try:
        # 初始化PandasAI
        pandasai_llm = LiteLLM(
            api_token=os.getenv("OPENAI_API_KEY"),
            model=configurable.pandasai_model,
            base_url=os.getenv("OPENAI_API_BASE")
        )
        
        pandas_ai = PandasAI(
            llm=pandasai_llm,
            verbose=True,
            enforce_privacy=True
        )
        
        # 获取要分析的表名列表
        table_names = [table.strip() for table in configurable.pandasai_tables.split(",") if table.strip()]
        
        if not table_names:
            raise Exception("没有配置要分析的数据库表")
        
        # 读取数据库表
        dataframes = {}
        for table_name in table_names:
            try:
                # 使用pandasai读取表数据
                query = f"SELECT * FROM {table_name}"
                df = pandas_ai.run(query, dataframes={})
                dataframes[table_name] = df
            except Exception as e:
                print(f"读取表 {table_name} 失败: {str(e)}")
                continue
        
        if not dataframes:
            raise Exception("无法读取任何数据库表")
        
        # 使用PandasAI分析数据
        analysis_query = state["analysis_query"]
        analysis_result = pandas_ai.run(analysis_query, dataframes=dataframes)
        
        # 如果结果是DataFrame，转换为字符串
        if hasattr(analysis_result, 'to_string'):
            analysis_result = analysis_result.to_string()
        elif hasattr(analysis_result, '__str__'):
            analysis_result = str(analysis_result)
        else:
            analysis_result = "分析完成，但结果格式不支持显示"
        
        # 创建引用结构
        citations = [{
            "start_index": 0,
            "end_index": len(analysis_result),
            "segments": [{
                "label": "Data Analysis",
                "short_url": f"https://analysis.id/{state['id']}",
                "value": f"Database: {', '.join(table_names)}"
            }]
        }]
        
        modified_text = insert_citation_markers(analysis_result, citations)
        sources_gathered = [item for citation in citations for item in citation["segments"]]

        return {
            "sources_gathered": sources_gathered,
            "data_analysis_result": [modified_text],
        }
        
    except Exception as e:
        error_message = f"数据分析失败: {str(e)}"
        print(error_message)
        
        # 返回错误信息
        citations = [{
            "start_index": 0,
            "end_index": len(error_message),
            "segments": [{
                "label": "Data Analysis Error",
                "short_url": f"https://analysis.id/{state['id']}",
                "value": "Error occurred during analysis"
            }]
        }]
        
        modified_text = insert_citation_markers(error_message, citations)
        sources_gathered = [item for citation in citations for item in citation["segments"]]

        return {
            "sources_gathered": sources_gathered,
            "data_analysis_result": [modified_text],
        }


def reflection(state: OverallState, config: RunnableConfig) -> ReflectionState:
    """LangGraph node that identifies knowledge gaps and generates potential follow-up queries.

    Analyzes the current summary to identify areas for further research and generates
    potential follow-up queries. Uses structured output to extract
    the follow-up query in JSON format.

    Args:
        state: Current graph state containing the running summary and research topic
        config: Configuration for the runnable, including LLM provider settings

    Returns:
        Dictionary with state update, including search_query key containing the generated follow-up query
    """
    configurable = Configuration.from_runnable_config(config)
    # Increment the research loop count and get the reasoning model
    state["research_loop_count"] = state.get("research_loop_count", 0) + 1
    reasoning_model = state.get("reasoning_model", configurable.reflection_model)

    # Format the prompt
    current_date = get_current_date()
    
    # Combine web research and data analysis results
    all_results = []
    if state.get("web_research_result"):
        all_results.extend(state["web_research_result"])
    if state.get("data_analysis_result"):
        all_results.extend(state["data_analysis_result"])
    
    summaries = "\n\n---\n\n".join(all_results) if all_results else "No results available."
    
    formatted_prompt = reflection_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        summaries=summaries,
    )
    # init Reasoning Model
    llm = ChatOpenAI(
        model=reasoning_model,
        temperature=1.0,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    result = llm.with_structured_output(Reflection).invoke(formatted_prompt)

    return {
        "is_sufficient": result.is_sufficient,
        "knowledge_gap": result.knowledge_gap,
        "follow_up_queries": result.follow_up_queries,
        "research_loop_count": state["research_loop_count"],
        "number_of_ran_queries": len(state.get("search_query", [])) + len(state.get("data_analysis_query", [])),
    }


def evaluate_research(
    state: ReflectionState,
    config: RunnableConfig,
) -> OverallState:
    """LangGraph routing function that determines the next step in the research flow.

    Controls the research loop by deciding whether to continue gathering information
    or to finalize the summary based on the configured maximum number of research loops.

    Args:
        state: Current graph state containing the research loop count
        config: Configuration for the runnable, including max_research_loops setting

    Returns:
        String literal indicating the next node to visit ("web_research" or "finalize_summary")
    """
    configurable = Configuration.from_runnable_config(config)
    max_research_loops = (
        state.get("max_research_loops")
        if state.get("max_research_loops") is not None
        else configurable.max_research_loops
    )
    if state["is_sufficient"] or state["research_loop_count"] >= max_research_loops:
        return "finalize_answer"
    else:
        # Determine task type for follow-up queries based on original task type
        task_type = state.get("task_type", "web_research")
        if task_type == "data_analysis":
            return [
                Send(
                    "data_analysis",
                    {
                        "analysis_query": follow_up_query,
                        "id": state["number_of_ran_queries"] + int(idx),
                    },
                )
                for idx, follow_up_query in enumerate(state["follow_up_queries"])
            ]
        else:
            return [
                Send(
                    "web_research",
                    {
                        "search_query": follow_up_query,
                        "id": state["number_of_ran_queries"] + int(idx),
                    },
                )
                for idx, follow_up_query in enumerate(state["follow_up_queries"])
            ]


def finalize_answer(state: OverallState, config: RunnableConfig):
    """LangGraph node that finalizes the research summary.

    Prepares the final output by deduplicating and formatting sources, then
    combining them with the running summary to create a well-structured
    research report with proper citations.

    Args:
        state: Current graph state containing the running summary and sources gathered

    Returns:
        Dictionary with state update, including running_summary key containing the formatted final summary with sources
    """
    configurable = Configuration.from_runnable_config(config)
    reasoning_model = state.get("reasoning_model") or configurable.answer_model

    # Format the prompt
    current_date = get_current_date()
    
    # Combine web research and data analysis results
    all_results = []
    if state.get("web_research_result"):
        all_results.extend(state["web_research_result"])
    if state.get("data_analysis_result"):
        all_results.extend(state["data_analysis_result"])
    
    summaries = "\n---\n\n".join(all_results) if all_results else "No results available."
    
    formatted_prompt = answer_instructions.format(
        current_date=current_date,
        research_topic=get_research_topic(state["messages"]),
        summaries=summaries,
    )

    # init Reasoning Model, default to OpenAI GPT
    llm = ChatOpenAI(
        model=reasoning_model,
        temperature=0,
        max_retries=2,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
    )
    result = llm.invoke(formatted_prompt)

    # Replace the short urls with the original urls and add all used urls to the sources_gathered
    unique_sources = []
    for source in state["sources_gathered"]:
        if source["short_url"] in result.content:
            result.content = result.content.replace(
                source["short_url"], source["value"]
            )
            unique_sources.append(source)

    return {
        "messages": [AIMessage(content=result.content)],
        "sources_gathered": unique_sources,
    }


def route_by_task_type(state: OverallState):
    """LangGraph routing function that determines whether to perform web research or data analysis.

    Routes to the appropriate task based on the determined task type.

    Args:
        state: Current graph state containing the task type

    Returns:
        String literal indicating the next node to visit ("generate_query" or "generate_data_analysis_query")
    """
    task_type = state.get("task_type", "web_research")
    if task_type == "data_analysis":
        return "generate_data_analysis_query"
    else:
        return "generate_query"


# Create our Agent Graph
builder = StateGraph(OverallState, config_schema=Configuration)

# Define the nodes we will cycle between
builder.add_node("determine_task_type", determine_task_type)
builder.add_node("generate_query", generate_query)
builder.add_node("generate_data_analysis_query", generate_data_analysis_query)
builder.add_node("web_research", web_research)
builder.add_node("data_analysis", data_analysis)
builder.add_node("reflection", reflection)
builder.add_node("finalize_answer", finalize_answer)

# Set the entrypoint as `determine_task_type`
builder.add_edge(START, "determine_task_type")

# Route based on task type
builder.add_conditional_edges(
    "determine_task_type", route_by_task_type, ["generate_query", "generate_data_analysis_query"]
)

# Add conditional edge to continue with search queries in a parallel branch
builder.add_conditional_edges(
    "generate_query", continue_to_web_research, ["web_research"]
)

# Add conditional edge to continue with data analysis queries in a parallel branch
builder.add_conditional_edges(
    "generate_data_analysis_query", continue_to_data_analysis, ["data_analysis"]
)

# Reflect on the research results (both web research and data analysis)
builder.add_edge("web_research", "reflection")
builder.add_edge("data_analysis", "reflection")

# Evaluate the research
builder.add_conditional_edges(
    "reflection", evaluate_research, ["web_research", "data_analysis", "finalize_answer"]
)

# Finalize the answer
builder.add_edge("finalize_answer", END)

graph = builder.compile(name="pro-search-agent")
