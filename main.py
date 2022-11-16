import json
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response, status

from endpoints import books_search_router
from utils.database import check_db_connection

app = FastAPI(openapi_url='/openapi.json')

app.include_router(books_search_router)


@app.get("/api/health")
def get_health():
    """
    The health check verify the app is up and that it is connected to the RDS instance
    :return:
    """
    current_time = str(datetime.now())
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    db_connection = check_db_connection()
    health = "Not good"
    if db_connection:
        db_connection = True
        status_code = status.HTTP_200_OK
        health = "Good"

    msg = {"name": "Books-Microservice",
           "health": health,
           "DB connection": db_connection,
           "at time": current_time}
    result = Response(json.dumps(msg), status_code=status_code)

    return result


# For local running please uncomment the below code
def start_books_microservice():
    uvicorn.run(app="main:app",
                host="0.0.0.0",
                port=5011)


if __name__ == "__main__":
    start_books_microservice()
