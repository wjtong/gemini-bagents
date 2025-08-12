import os
from pydantic import BaseModel, Field
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig


class Configuration(BaseModel):
    """The configuration for the agent."""

    query_generator_model: str = Field(
        default="gpt-4o-mini",
        metadata={
            "description": "The name of the language model to use for the agent's query generation."
        },
    )

    reflection_model: str = Field(
        default="gpt-4o",
        metadata={
            "description": "The name of the language model to use for the agent's reflection."
        },
    )

    answer_model: str = Field(
        default="gpt-4o",
        metadata={
            "description": "The name of the language model to use for the agent's answer."
        },
    )

    openai_api_base: Optional[str] = Field(
        default=None,
        metadata={
            "description": "The base URL for OpenAI API. If not set, uses the default OpenAI API endpoint."
        },
    )

    number_of_initial_queries: int = Field(
        default=3,
        metadata={"description": "The number of initial search queries to generate."},
    )

    max_research_loops: int = Field(
        default=2,
        metadata={"description": "The maximum number of research loops to perform."},
    )

    # PostgreSQL配置 (保留以备将来使用)
    postgresql_host: str = Field(
        default="localhost",
        metadata={"description": "PostgreSQL数据库主机地址"},
    )

    postgresql_port: int = Field(
        default=5432,
        metadata={"description": "PostgreSQL数据库端口"},
    )

    postgresql_database: str = Field(
        default="postgres",
        metadata={"description": "PostgreSQL数据库名称"},
    )

    postgresql_username: str = Field(
        default="postgres",
        metadata={"description": "PostgreSQL数据库用户名"},
    )

    postgresql_password: str = Field(
        default="",
        metadata={"description": "PostgreSQL数据库密码"},
    )

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )

        # Get raw values from environment or config
        raw_values: dict[str, Any] = {}
        for name in cls.model_fields.keys():
            # 特殊处理openai_api_base字段的环境变量映射
            if name == "openai_api_base":
                env_value = os.environ.get("OPENAI_API_BASE", configurable.get(name))
            else:
                env_value = os.environ.get(name.upper(), configurable.get(name))
            raw_values[name] = env_value

        # Filter out None values
        values = {k: v for k, v in raw_values.items() if v is not None}

        return cls(**values)
