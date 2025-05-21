# Vector DB

This module contains setup and configuration for local vector databases (e.g., Qdrant) used for semantic search and RAG applications.

## Qdrant Setup

1. Ensure Docker is installed.
2. Start Qdrant:
   ```sh
   docker-compose up -d
   ```
   Qdrant will be available at http://localhost:6333

## Python Utilities

- `qdrant_utils.py`: Utility functions for connecting, inserting, and searching vectors in Qdrant.
- `example_usage.py`: Example script for basic Qdrant operations.

### Install dependencies
```sh
pip install -r requirements.txt
```

### Run the example
```sh
python example_usage.py 