from fastapi import APIRouter, status, Query
from books_db_util import get_by_book_name, get_by_book_author
import consts

books_search_router = APIRouter(prefix="/api/v1")


@books_search_router.get(path="/book/book_name/{book_name}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_book")
def get_book_by_name(book_name: str):
    """
    This endpoint returns a book by its name
    :param book_name: the book name
    :return: book's information
    """
    result = get_by_book_name(book_name=book_name, field=consts.NAME)

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
    result = get_by_book_author(author_name=author_name, field=consts.AUTHOR)

    return result
