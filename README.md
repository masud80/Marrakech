# Marrakech

This project is a local-first, modular data and analytics platform for Ash Investments. It supports data ingestion, inventory administration, machine learning/NLP services, and an admin UI.

## Project Structure

- `data_ingestion/` - ETL/ELT pipelines, Airflow DAGs, Spark jobs, custom scripts
- `backend/` - Inventory admin API (FastAPI), DB models, business logic
- `ml_service/` - ML/NLP model training, serving, and utilities
- `vector_db/` - Vector database setup (Qdrant, FAISS)
- `admin_ui/` - React admin dashboard
- `data/` - Local data storage (raw, processed, models, etc.)

## Local Development

1. Install Docker and Docker Compose.
2. Copy `.env.example` to `.env` and fill in environment variables as needed.
3. Run `docker-compose up --build` to start all services.
4. Access the admin UI at `http://localhost:3000` (default).

See individual module READMEs for more details. 
