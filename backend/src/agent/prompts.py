from datetime import datetime


# Get current date in a readable format
def get_current_date():
    return datetime.now().strftime("%B %d, %Y")


query_writer_instructions = """Your goal is to generate sophisticated and diverse web search queries. These queries are intended for an advanced automated web research tool capable of analyzing complex results, following links, and synthesizing information.

Instructions:
- Always prefer a single search query, only add another query if the original question requests multiple aspects or elements and one query is not enough.
- Each query should focus on one specific aspect of the original question.
- Don't produce more than {number_queries} queries.
- Queries should be diverse, if the topic is broad, generate more than 1 query.
- Don't generate multiple similar queries, 1 is enough.
- Query should ensure that the most current information is gathered. The current date is {current_date}.

Format: 
- Format your response as a JSON object with ALL two of these exact keys:
   - "rationale": Brief explanation of why these queries are relevant
   - "query": A list of search queries

Example:

Topic: What revenue grew more last year apple stock or the number of people buying an iphone
```json
{{
    "rationale": "To answer this comparative growth question accurately, we need specific data points on Apple's stock performance and iPhone sales metrics. These queries target the precise financial information needed: company revenue trends, product-specific unit sales figures, and stock price movement over the same fiscal period for direct comparison.",
    "query": ["Apple total revenue growth fiscal year 2024", "iPhone unit sales growth fiscal year 2024", "Apple stock price growth fiscal year 2024"],
}}
```

Context: {research_topic}"""


task_type_instructions = """Analyze the user's question and determine whether it requires web research or data analysis.

Instructions:
- If the question requires searching for current information, news, trends, or general knowledge, choose 'web_research'
- If the question requires analyzing numerical data, statistics, financial data, or performing calculations, choose 'data_analysis'
- Consider the nature of the information needed to answer the question

Examples:
- "What are the latest developments in AI?" -> web_research
- "What is the current stock price of Apple?" -> data_analysis
- "How has the population of New York changed in the last decade?" -> data_analysis
- "What are the benefits of renewable energy?" -> web_research

Format your response as a JSON object with these exact keys:
- "task_type": Either "web_research" or "data_analysis"
- "rationale": Brief explanation of why this task type was chosen

Context: {research_topic}"""


data_analysis_instructions = """Generate data analysis queries to gather numerical data, statistics, and perform calculations for the research topic.

Instructions:
- Focus on queries that will help gather numerical data, statistics, financial information, or perform calculations
- Each query should target specific data sources or analysis tools
- Queries should be designed to extract quantitative information
- Consider using data sources like financial APIs, statistical databases, or calculation tools

Format your response as a JSON object with these exact keys:
- "rationale": Brief explanation of why these analysis queries are relevant
- "analysis_query": A list of data analysis queries

Example:
```json
{{
    "rationale": "To analyze the financial performance comparison, we need specific numerical data on revenue growth, stock performance, and sales metrics. These queries target quantitative financial data sources.",
    "analysis_query": ["Apple revenue 2024 vs 2023", "Apple stock price performance 2024", "iPhone sales data 2024"]
}}
```

Context: {research_topic}"""


web_searcher_instructions = """Conduct targeted Google Searches to gather the most recent, credible information on "{research_topic}" and synthesize it into a verifiable text artifact.

Instructions:
- Query should ensure that the most current information is gathered. The current date is {current_date}.
- Conduct multiple, diverse searches to gather comprehensive information.
- Consolidate key findings while meticulously tracking the source(s) for each specific piece of information.
- The output should be a well-written summary or report based on your search findings. 
- Only include the information found in the search results, don't make up any information.

Research Topic:
{research_topic}
"""


data_analyzer_instructions = """Perform data analysis on "{research_topic}" to extract numerical insights and perform calculations.

Instructions:
- Focus on gathering numerical data, statistics, and performing calculations
- Use available data sources to extract quantitative information
- Perform relevant calculations and statistical analysis
- Present findings in a clear, structured format with numerical results
- Include data sources and methodology where applicable

Research Topic:
{research_topic}
"""


reflection_instructions = """You are an expert research assistant analyzing summaries about "{research_topic}".

Instructions:
- Identify knowledge gaps or areas that need deeper exploration and generate a follow-up query. (1 or multiple).
- If provided summaries are sufficient to answer the user's question, don't generate a follow-up query.
- If there is a knowledge gap, generate a follow-up query that would help expand your understanding.
- Focus on technical details, implementation specifics, or emerging trends that weren't fully covered.

Requirements:
- Ensure the follow-up query is self-contained and includes necessary context for web search.

Output Format:
- Format your response as a JSON object with these exact keys:
   - "is_sufficient": true or false
   - "knowledge_gap": Describe what information is missing or needs clarification
   - "follow_up_queries": Write a specific question to address this gap

Example:
```json
{{
    "is_sufficient": true, // or false
    "knowledge_gap": "The summary lacks information about performance metrics and benchmarks", // "" if is_sufficient is true
    "follow_up_queries": ["What are typical performance benchmarks and metrics used to evaluate [specific technology]?"] // [] if is_sufficient is true
}}
```

Reflect carefully on the Summaries to identify knowledge gaps and produce a follow-up query. Then, produce your output following this JSON format:

Summaries:
{summaries}"""


answer_instructions = """Generate a high-quality answer to the user's question based on the provided summaries.

Instructions:
- The current date is {current_date}.
- You are the final step of a multi-step research process, don't mention that you are the final step. 
- You have access to all the information gathered from the previous steps.
- You have access to the user's question.
- Generate a high-quality answer to the user's question based on the provided summaries and the user's question.
- Include the sources you used from the Summaries in the answer correctly, use markdown format (e.g. [apnews](https://vertexaisearch.cloud.google.com/id/1-0)). THIS IS A MUST.

User Context:
- {research_topic}

Summaries:
{summaries}"""
