#!/usr/bin/env python3
"""Test script for the data analysis functionality."""

import os
from langchain_core.messages import HumanMessage
from src.agent.graph import graph


def test_web_research_query():
    """Test a web research query."""
    print("=== Testing Web Research Query ===")
    
    state = {
        "messages": [HumanMessage(content="What are the latest developments in AI technology?")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Answer:", messages[-1].content)
        print("Task Type:", result.get("task_type", "unknown"))
    else:
        print("No answer generated")


def test_data_analysis_query():
    """Test a data analysis query."""
    print("\n=== Testing Data Analysis Query ===")
    
    state = {
        "messages": [HumanMessage(content="What is the current stock price of Apple and how has it performed this year?")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Answer:", messages[-1].content)
        print("Task Type:", result.get("task_type", "unknown"))
    else:
        print("No answer generated")


def test_financial_analysis_query():
    """Test a financial analysis query."""
    print("\n=== Testing Financial Analysis Query ===")
    
    state = {
        "messages": [HumanMessage(content="Calculate the compound annual growth rate of Tesla stock over the past 5 years")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Answer:", messages[-1].content)
        print("Task Type:", result.get("task_type", "unknown"))
    else:
        print("No answer generated")


if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        exit(1)
    
    test_web_research_query()
    test_data_analysis_query()
    test_financial_analysis_query() 