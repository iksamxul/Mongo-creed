Universal CRUD API Core
The core FastAPI CRUD service for MongoDB. This repository contains only the production-ready application code for the universal API.

Python 3.11+ FastAPI License: MIT

About
Universal CRUD API Core provides a dynamic, schema-agnostic REST interface for any MongoDB collection. It delivers clean, optimized application code without scaffolding, examples, or containerization.

Quick Overview
- Universal routing: Operates on any collection via path parameter
- Async I/O: Motor-based non-blocking MongoDB access
- Efficient reads: Pagination, optional sorting, JSON filter (q)
- Strict config: .env-only configuration for URI, DB, and Port
- Consistent errors: Centralized error handling with structured payloads
- High throughput: ORJSON responses, FastAPI on Uvicorn

File Structure
├── app/
│   ├── main.py                  # FastAPI app and lifespan
│   ├── api/
│   │   ├── routes.py            # Universal CRUD endpoints
│   ├── core/
│   │   ├── config.py            # .env configuration loader
│   │   └── db.py                # Mongo connection lifecycle
│   │   └── errors.py            # Centralized error handling
│   ├── repositories/
│   │   └── universal_repository.py  # Generic Mongo repository
│   ├── controllers/
│   │   └── universal_controller.py  # Request validation and orchestration
│   └── utils/
│       └── bson.py              # ObjectId conversion and serialization
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore patterns
└── run.py                       # Starts server using .env PORT

Core Dependencies
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
motor>=3.3.2
pymongo>=4.7.0
python-dotenv>=1.0.1
orjson>=3.10.7
pydantic>=2.7.0

API Endpoints
All endpoints use the /api prefix.

Method  Endpoint                      Purpose
GET     /api/{collection}             List documents with pagination, sort, filter
GET     /api/{collection}/{id}        Fetch a single document by id
POST    /api/{collection}             Create a document
PUT     /api/{collection}/{id}        Replace a document
PATCH   /api/{collection}/{id}        Partially update fields
DELETE  /api/{collection}/{id}        Delete a document

Configuration
Use a .env file as the single source of truth:

MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=appdb
PORT=8000

Installation
# Create venv and install
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

Running
# Start MongoDB separately
# Launch API
python run.py

Development
- main.py: App factory and lifespan hooks (connect/disconnect)
- core/config.py: Loads required settings from .env
- core/db.py: Motor client and database handle
- core/errors.py: AppError and exception handlers
- repositories/universal_repository.py: Generic data access
- controllers/universal_controller.py: Validation, id handling, orchestration
- api/routes.py: HTTP endpoints (universal CRUD)

Code Standards
- Python 3.11+
- Type hints
- Async-first I/O
- DRY, modular structure

Integration
Use as a standalone service via HTTP, or mount the router in another FastAPI app:

from fastapi import FastAPI
from app.api.routes import api_router
from app.core.db import connect, disconnect

app = FastAPI()
app.include_router(api_router, prefix="/api")

Performance Characteristics
Metric                 Value
List latency           Depends on filter/index; paginated
Single-item read       ~1 network round trip
Serialization          ORJSON
Max page size          1000 (configurable via query)

License
© 2026 Sam
