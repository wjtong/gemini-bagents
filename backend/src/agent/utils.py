import re
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text, MetaData, inspect
from agent.configuration import Configuration


def get_citations(response):
    """Extract citations from the response."""
    citations = []
    if hasattr(response, "citations"):
        citations = response.citations
    return citations


def get_research_topic(messages):
    """Extract the research topic from the messages."""
    if not messages:
        return ""
    return messages[-1].content


def insert_citation_markers(text, citations):
    """Insert citation markers into the text."""
    if not citations:
        return text
    
    # Sort citations by start_index in reverse order to avoid index shifting
    sorted_citations = sorted(citations, key=lambda x: x["start_index"], reverse=True)
    
    for citation in sorted_citations:
        start = citation["start_index"]
        end = citation["end_index"]
        
        # Get the text segment
        segment = text[start:end]
        
        # Create citation markers for each segment
        citation_markers = []
        for seg in citation["segments"]:
            marker = f"[{seg['label']}]({seg['short_url']})"
            citation_markers.append(marker)
        
        # Replace the segment with citation markers
        if citation_markers:
            replacement = f"{segment} {' '.join(citation_markers)}"
            text = text[:start] + replacement + text[end:]
    
    return text


def resolve_urls(text, sources_gathered):
    """Replace short URLs with original URLs in the text."""
    for source in sources_gathered:
        if source["short_url"] in text:
            text = text.replace(source["short_url"], source["value"])
    return text


def get_database_connection(config: Configuration):
    """获取PostgreSQL数据库连接"""
    try:
        connection = psycopg2.connect(
            host=config.postgresql_host,
            port=config.postgresql_port,
            database=config.postgresql_database,
            user=config.postgresql_username,
            password=config.postgresql_password
        )
        return connection
    except Exception as e:
        raise Exception(f"数据库连接失败: {str(e)}")


def get_table_schema(config: Configuration) -> Dict[str, Any]:
    """获取数据库表结构信息"""
    try:
        # 创建SQLAlchemy引擎
        connection_string = f"postgresql://{config.postgresql_username}:{config.postgresql_password}@{config.postgresql_host}:{config.postgresql_port}/{config.postgresql_database}"
        engine = create_engine(connection_string)
        
        # 获取表名列表
        table_names = [table.strip() for table in config.pandasai_tables.split(",") if table.strip()]
        
        if not table_names:
            return {}
        
        # 获取表结构信息
        inspector = inspect(engine)
        schema_info = {}
        
        for table_name in table_names:
            try:
                # 获取列信息
                columns = inspector.get_columns(table_name)
                column_info = []
                
                for column in columns:
                    column_info.append({
                        "name": column["name"],
                        "type": str(column["type"]),
                        "nullable": column["nullable"],
                        "default": column["default"]
                    })
                
                # 获取主键信息
                primary_keys = inspector.get_pk_constraint(table_name)
                
                # 获取索引信息
                indexes = inspector.get_indexes(table_name)
                
                schema_info[table_name] = {
                    "columns": column_info,
                    "primary_keys": primary_keys.get("constrained_columns", []),
                    "indexes": [idx["name"] for idx in indexes],
                    "row_count": get_table_row_count(engine, table_name)
                }
                
            except Exception as e:
                print(f"获取表 {table_name} 结构失败: {str(e)}")
                continue
        
        return schema_info
        
    except Exception as e:
        raise Exception(f"获取数据库表结构失败: {str(e)}")


def get_table_row_count(engine, table_name: str) -> int:
    """获取表的行数"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()
    except Exception:
        return 0


def can_analyze_with_data_analysis(query: str, database_schema: Dict[str, Any]) -> bool:
    """判断查询是否适合通过数据分析节点处理"""
    if not database_schema:
        return False
    
    # 检查查询是否包含数据分析相关的关键词
    data_analysis_keywords = [
        "数据", "统计", "分析", "计算", "数值", "金额", "价格", "销量", "收入", "利润",
        "数据", "统计", "分析", "计算", "数值", "金额", "价格", "销量", "收入", "利润",
        "data", "statistics", "analysis", "calculate", "numeric", "amount", "price", "sales", "revenue", "profit",
        "sum", "average", "count", "max", "min", "total", "percentage", "ratio"
    ]
    
    query_lower = query.lower()
    has_data_keywords = any(keyword in query_lower for keyword in data_analysis_keywords)
    
    # 检查是否有可用的数据库表
    has_available_tables = len(database_schema) > 0
    
    return has_data_keywords and has_available_tables
