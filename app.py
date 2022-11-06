import json
from datetime import datetime

from fastapi import FastAPI, Response, status

from endpoints import books_search_router

app = FastAPI()

app.include_router(books_search_router)


@app.get("/api/health")
def get_health():
    current_time = str(datetime.now())
    msg = {"name": "Books-Microservice",
            "health": "Good",
            "at time": current_time}
    result = Response(json.dumps(msg), status_code=status.HTTP_200_OK)

    return result
