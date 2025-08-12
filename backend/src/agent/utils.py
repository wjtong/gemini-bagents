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
    """获取数据库表结构信息 (保留以备将来使用)"""
    # 暂时返回空字典，因为pandasai功能已被移除
    return {}


def get_table_row_count(engine, table_name: str) -> int:
    """获取表的行数 (保留以备将来使用)"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            return result.scalar()
    except Exception:
        return 0


def can_analyze_with_data_analysis(query: str, database_schema: Dict[str, Any]) -> bool:
    """判断查询是否适合通过数据分析节点处理 (保留以备将来使用)"""
    # 暂时返回False，因为pandasai功能已被移除
    return False
