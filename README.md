# Universal CRUD API (FastAPI + MongoDB)

Author: Sam

## Requirements
- Python 3.11+
- MongoDB 6.0+

## Setup
1. Create a virtual environment and install dependencies
   - Linux/macOS:
     - python3 -m venv .venv
     - source .venv/bin/activate
     - pip install -r requirements.txt
   - Windows (PowerShell):
     - py -3 -m venv .venv
     - .venv\\Scripts\\Activate.ps1
     - pip install -r requirements.txt
2. Configure .env (only source of configuration)
   - MONGODB_URI=mongodb://localhost:27017
   - MONGODB_DB=appdb
   - PORT=8000
3. Start MongoDB
4. Run the API
   - python run.py

Base URL: http://localhost:PORT/api

## Endpoints (universal, pass any collection name)
- GET /api/{collection}
- GET /api/{collection}/{id}
- POST /api/{collection}
- PUT /api/{collection}/{id}
- PATCH /api/{collection}/{id}
- DELETE /api/{collection}/{id}

## Query Parameters (GET /api/{collection})
- limit: 1..1000, default 20
- offset: >= 0, default 0
- sort: field name to sort by
- order: asc|desc, default asc
- q: JSON-encoded filter object

Examples for q:
- q={"status":"active"}
- q={"price":{"$gte":10}}
- q={"_id":"665f7c5c3a1b8e9e4c2d1a00"}

URL-encode q when using curl or a browser.

## Response Shapes
- List: { "items": [...], "total": n, "limit": n, "offset": n }
- Single: flattened document where Mongo _id is exposed as "id"
- Errors: { "error": { "message": string, "details": any } }

## cURL Examples (collection: widgets)
Create
- curl -s -X POST http://localhost:8000/api/widgets -H "Content-Type: application/json" -d '{"name":"alpha","status":"active"}'

List with pagination and sort
- curl -s "http://localhost:8000/api/widgets?limit=10&offset=0&sort=created_at&order=desc"

Filter
- curl -s "http://localhost:8000/api/widgets?q=%7B%22status%22%3A%22active%22%7D"

Get by id
- curl -s http://localhost:8000/api/widgets/{id}

Replace
- curl -s -X PUT http://localhost:8000/api/widgets/{id} -H "Content-Type: application/json" -d '{"name":"beta","status":"inactive"}'

Patch
- curl -s -X PATCH http://localhost:8000/api/widgets/{id} -H "Content-Type: application/json" -d '{"status":"active"}'

Delete
- curl -s -X DELETE http://localhost:8000/api/widgets/{id}

## Notes
- The API is schema-agnostic; any JSON object is accepted per collection.
- "id" is a stringified ObjectId; do not send "_id" or "id" in POST/PUT/PATCH payloads.
- created_at and updated_at are managed automatically.
- Keep PORT, MONGODB_URI, and MONGODB_DB exclusively in .env.

— Sam
