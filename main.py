import uvicorn


def start_books_microservice():
    uvicorn.run(app="app:app",
                host="localhost",
                port=8000)


if __name__ == "__main__":
    start_books_microservice()
