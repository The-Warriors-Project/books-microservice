from fastapi import APIRouter
from fastapi import status
from pydantic import BaseModel

import consts
from utils import db_books_util
from fastapi import Response

books_search_router = APIRouter(prefix="/api/v1/book")


class Books(BaseModel):
    name: str
    author: str
    description: str
    isbn: str
    picture: str


class LikesCount(BaseModel):
    offset: int
    book_ids: str


@books_search_router.get(path="/book_name/{book_name}",
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


@books_search_router.get(path="/author_name/{author_name}",
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


@books_search_router.post(path="/book_name/{book_name}/add",
                          status_code=status.HTTP_201_CREATED,
                          operation_id="insert_book")
def insert_book(book: Books):
    """
    This endpoint inserts a book with its properties
    :param book: the book's properties
    """

    db_books_util.insert_book(name=book.name, isbn=book.isbn, author=book.author,
                              picture=book.picture, description=book.description)


@books_search_router.put(path="/likes_count",
                         status_code=status.HTTP_200_OK,
                         operation_id="update_likes_count")
def update_likes_count(likes_count: LikesCount) -> None:
    """
    This endpoint update the like count for each book.
    :return: None
    """

    book_list = likes_count.book_ids.split(' ')  # split the list
    keep_track = []
    try:
        for _id in book_list:
            keep_track.append(_id)
            db_books_util.update_likes_book(book_id=_id, operator=likes_count.offset)
    except Exception:
        # revert
        for _id in keep_track:
            db_books_util.update_likes_book(book_id=_id, operator=likes_count.offset*-1)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@books_search_router.get(path="/likes_count/book_id/{book_id}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_likes_count")
def get_likes_count(book_id: str) -> int:
    """
    This endpoint returns the likes count for a book.
    :param book_id: the needed book id
    :return: an int representing the likes count
    """
    result = db_books_util.get_likes_book(book_id=book_id)
    # if _id does not exist, return 404 not found status code
    if not result:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return result
