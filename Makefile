.PHONY: help dev-frontend dev-backend dev test-data-analysis example-data-analysis check-deps

help:
	@echo "Available commands:"
	@echo "  make dev-frontend    - Starts the frontend development server (Vite)"
	@echo "  make dev-backend     - Starts the backend development server (Uvicorn with reload)"
	@echo "  make dev             - Starts both frontend and backend development servers"
	@echo "  make test-data-analysis - Test the data analysis functionality"
	@echo "  make example-data-analysis - Run data analysis examples"
	@echo "  make check-deps      - Check dependency versions"

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server..."
	@cd backend && langgraph dev

# Run frontend and backend concurrently
dev:
	@echo "Starting both frontend and backend development servers..."
	@make dev-frontend & make dev-backend

# Test data analysis functionality
test-data-analysis:
	@echo "Testing data analysis functionality..."
	@cd backend && python examples/test_data_analysis.py

# Run data analysis examples
example-data-analysis:
	@echo "Running data analysis examples..."
	@cd backend && python examples/data_analysis_example.py

# Check dependency versions
check-deps:
	@echo "Checking dependency versions..."
	@cd backend && python check_dependencies.py 