from app.core.config import get_settings
import uvicorn

s = get_settings()
uvicorn.run("app.main:app", host="0.0.0.0", port=s.port)
