from fastapi import APIRouter
from fastapi import status
from pydantic import BaseModel

import consts
from utils import db_books_util

books_search_router = APIRouter(prefix="/api/v1")


class Books(BaseModel):
    name: str
    author: str
    description: str
    isbn: str
    picture: str


@books_search_router.get(path="/book/book_name/{book_name}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_book")
def get_book_by_name(book_name: str):
    """
    This endpoint returns a book by its name
    :param book_name: the book name
    :return: book's information
    """
    result = db_books_util.get_books(field_data_=book_name, field_name_=consts.NAME)

    return result


@books_search_router.get(path="/book/author_name/{author_name}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_book_by_author")
def get_book_by_author(author_name: str):
    """
    This endpoint returns a book by its author
    :param author_name: the author name
    :return: book's information
    """
    result = db_books_util.get_books(field_data_=author_name, field_name_=consts.AUTHOR)

    return result


@books_search_router.post(path="/book/book_name/{book_name}/add",
                          status_code=status.HTTP_201_CREATED,
                          operation_id="insert_book")
def insert_book(book: Books):
    """
    This endpoint inserts a book with its properties
    :param book: the book's properties
    """

    db_books_util.insert_book(name=book.name, isbn=book.isbn, author=book.author,
                              picture=book.picture, description=book.description)
