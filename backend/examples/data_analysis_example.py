#!/usr/bin/env python3
"""Example script demonstrating the data analysis functionality."""

import os
from langchain_core.messages import HumanMessage
from src.agent.graph import graph


def main() -> None:
    """Run the research agent with data analysis examples."""
    
    # Example 1: Data Analysis Query
    print("=== Example 1: Data Analysis Query ===")
    print("Query: What is the current stock price of Apple and how has it performed this year?")
    
    state = {
        "messages": [HumanMessage(content="What is the current stock price of Apple and how has it performed this year?")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Task Type:", result.get("task_type", "unknown"))
        print("Answer:", messages[-1].content)
    else:
        print("No answer generated")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Web Research Query
    print("=== Example 2: Web Research Query ===")
    print("Query: What are the latest developments in AI technology?")
    
    state = {
        "messages": [HumanMessage(content="What are the latest developments in AI technology?")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Task Type:", result.get("task_type", "unknown"))
        print("Answer:", messages[-1].content)
    else:
        print("No answer generated")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Financial Analysis Query
    print("=== Example 3: Financial Analysis Query ===")
    print("Query: Calculate the compound annual growth rate of Tesla stock over the past 5 years")
    
    state = {
        "messages": [HumanMessage(content="Calculate the compound annual growth rate of Tesla stock over the past 5 years")],
        "initial_search_query_count": 2,
        "max_research_loops": 1,
        "reasoning_model": "gpt-4o",
    }

    result = graph.invoke(state)
    messages = result.get("messages", [])
    if messages:
        print("Task Type:", result.get("task_type", "unknown"))
        print("Answer:", messages[-1].content)
    else:
        print("No answer generated")


if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        exit(1)
    
    main() 