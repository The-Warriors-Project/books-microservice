import json
from datetime import datetime

import uvicorn
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


# For local running please uncomment the below code
#def start_books_microservice():
#    uvicorn.run(app="main:app",
#                host="0.0.0.0",
#                port=5011)
#
#
#if __name__ == "__main__":
#    start_books_microservice()
