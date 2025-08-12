# OpenAI GPT Fullstack LangGraph Quickstart

This project demonstrates a fullstack application using a React frontend and a LangGraph-powered backend agent. The agent is designed to perform comprehensive research on a user's query by dynamically generating search terms, querying the web using search APIs, reflecting on the results to identify knowledge gaps, and iteratively refining its search until it can provide a well-supported answer with citations. This application serves as an example of building research-augmented conversational AI using LangGraph and OpenAI's GPT models.

<img src="./app.png" title="OpenAI GPT Fullstack LangGraph" alt="OpenAI GPT Fullstack LangGraph" width="90%">

## Features

- 💬 Fullstack application with a React frontend and LangGraph backend.
- 🧠 Powered by a LangGraph agent for advanced research and conversational AI.
- 🔍 Dynamic search query generation using OpenAI GPT models.
- 🌐 Integrated web research via search APIs.
- 📊 **NEW**: Intelligent data analysis using OpenAI GPT for numerical queries and calculations (dummy implementation).
- 🤔 Reflective reasoning to identify knowledge gaps and refine searches.
- 📄 Generates answers with citations from gathered sources.
- 🔄 Hot-reloading for both frontend and backend during development.

## Project Structure

The project is divided into two main directories:

-   `frontend/`: Contains the React application built with Vite.
-   `backend/`: Contains the LangGraph/FastAPI application, including the research agent logic.

## Getting Started: Development and Local Testing

Follow these steps to get the application running locally for development and testing.

**1. Prerequisites:**

-   Node.js and npm (or yarn/pnpm)
-   Python 3.11+
-   **`OPENAI_API_KEY`**: The backend agent requires an OpenAI API key.
-   **`OPENAI_API_BASE`** (optional): If you're using a custom OpenAI-compatible API endpoint, set this to your base URL.
    1.  Navigate to the `backend/` directory.
    2.  Create a file named `.env` by copying the `backend/.env.example` file.
    3.  Open the `.env` file and add your OpenAI API key: `OPENAI_API_KEY="YOUR_ACTUAL_API_KEY"`
    4.  If using a custom endpoint, add: `OPENAI_API_BASE="YOUR_CUSTOM_BASE_URL"`

**2. Install Dependencies:**

**Backend:**

```bash
cd backend
pip install -e .
```

For detailed installation instructions, see [INSTALL.md](backend/INSTALL.md).

**Frontend:**

```bash
cd frontend
npm install
```

**3. Configure Environment Variables:**

Create a `.env` file in the `backend/` directory with the following variables:

```bash
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1  # 可选，自定义API端点

# Agent配置
QUERY_GENERATOR_MODEL=gpt-4o-mini
REFLECTION_MODEL=gpt-4o
ANSWER_MODEL=gpt-4o
NUMBER_OF_INITIAL_QUERIES=3
MAX_RESEARCH_LOOPS=2
```

**4. Run Development Servers:**

**Backend & Frontend:**

```bash
make dev
```
This will run the backend and frontend development servers.    Open your browser and navigate to the frontend development server URL (e.g., `http://localhost:5173/app`).

_Alternatively, you can run the backend and frontend development servers separately. For the backend, open a terminal in the `backend/` directory and run `langgraph dev`. The backend API will be available at `http://127.0.0.1:2024`. It will also open a browser window to the LangGraph UI. For the frontend, open a terminal in the `frontend/` directory and run `npm run dev`. The frontend will be available at `http://localhost:5173`._

## How the Backend Agent Works (High-Level)

The core of the backend is a LangGraph agent defined in `backend/src/agent/graph.py`. It follows these steps:

<img src="./agent.png" title="Agent Flow" alt="Agent Flow" width="50%">

1.  **Task Type Determination:** The agent first analyzes the user's query to determine whether it requires web research or data analysis.
2.  **Generate Initial Queries:** Based on your input, it generates a set of initial search queries (for web research) or data analysis queries (for numerical analysis) using an OpenAI GPT model.
3.  **Web Research or Data Analysis:** 
    - For web research: Uses the GPT model with search APIs to find relevant web pages.
    - For data analysis: Performs numerical analysis, calculations, and statistical processing.
4.  **Reflection & Knowledge Gap Analysis:** The agent analyzes the results to determine if the information is sufficient or if there are knowledge gaps. It uses a GPT model for this reflection process.
5.  **Iterative Refinement:** If gaps are found or the information is insufficient, it generates follow-up queries and repeats the research/analysis steps (up to a configured maximum number of loops).
6.  **Finalize Answer:** Once the research is deemed sufficient, the agent synthesizes the gathered information into a coherent answer, including citations from the sources, using a GPT model.

### Task Type Examples

**Web Research Queries:**
- "What are the latest developments in AI technology?"
- "What are the benefits of renewable energy?"
- "How does machine learning work?"

**Data Analysis Queries:**
- "What is the current stock price of Apple?"
- "Calculate the compound annual growth rate of Tesla stock over the past 5 years"
- "How has the population of New York changed in the last decade?"

## CLI Example

For quick one-off questions you can execute the agent from the command line. The
script `backend/examples/cli_research.py` runs the LangGraph agent and prints the
final answer:

```bash
cd backend
python examples/cli_research.py "What are the latest trends in renewable energy?"
```

You can also test the data analysis functionality:

```bash
cd backend
python examples/test_data_analysis.py
```

## Deployment

In production, the backend server serves the optimized static frontend build. LangGraph requires a Redis instance and a Postgres database. Redis is used as a pub-sub broker to enable streaming real time output from background runs. Postgres is used to store assistants, threads, runs, persist thread state and long term memory, and to manage the state of the background task queue with 'exactly once' semantics. For more details on how to deploy the backend server, take a look at the [LangGraph Documentation](https://langchain-ai.github.io/langgraph/concepts/deployment_options/). Below is an example of how to build a Docker image that includes the optimized frontend build and the backend server and run it via `docker-compose`.

_Note: For the docker-compose.yml example you need a LangSmith API key, you can get one from [LangSmith](https://smith.langchain.com/settings)._

_Note: If you are not running the docker-compose.yml example or exposing the backend server to the public internet, you should update the `apiUrl` in the `frontend/src/App.tsx` file to your host. Currently the `apiUrl` is set to `http://localhost:8123` for docker-compose or `http://localhost:2024` for development._

**1. Build the Docker Image:**

   Run the following command from the **project root directory**:
   ```bash
   docker build -t openai-gpt-fullstack-langgraph -f Dockerfile .
   ```
**2. Run the Production Server:**

   ```bash
   OPENAI_API_KEY=<your_openai_api_key> OPENAI_API_BASE=<your_custom_base_url> LANGSMITH_API_KEY=<your_langsmith_api_key> docker-compose up
   ```

Open your browser and navigate to `http://localhost:8123/app/` to see the application. The API will be available at `http://localhost:8123`.

## Technologies Used

- [React](https://reactjs.org/) (with [Vite](https://vitejs.dev/)) - For the frontend user interface.
- [Tailwind CSS](https://tailwindcss.com/) - For styling.
- [Shadcn UI](https://ui.shadcn.com/) - For components.
- [LangGraph](https://github.com/langchain-ai/langgraph) - For building the backend research agent.
- [OpenAI GPT](https://openai.com/api/) - LLM for query generation, reflection, and answer synthesis.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details. 
