from fastapi import APIRouter
from fastapi import status, Response
from pydantic import BaseModel

import consts
from utils import db_books_util

books_search_router = APIRouter(prefix="/api/v1/book")


class Books(BaseModel):
    title: str
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
    """
    result = db_books_util.get_books(field_data_=book_name, field_name_=consts.TITLE)

    return result


@books_search_router.get(path="/author_name/{author_name}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_book_by_author")
def get_book_by_author(author_name: str):
    """
    This endpoint returns a book by its author
    """
    result = db_books_util.get_books(field_data_=author_name, field_name_=consts.AUTHOR)

    return result


@books_search_router.get(path="/book_ids/{book_ids}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_book_by_id")
def get_book_by_id(book_ids: str):
    """
    This function get book information from the DB by a book id.
    A list of books must be in the pattern of '+' seperated. Example: "1+2+3"
    """
    books_to_return = {}
    book_ids_list = book_ids.split('+')  # split the str if there are multiple ids
    i = 0
    for _id in book_ids_list:
        books_to_return[i] = db_books_util.get_book_by_id(_id=_id)
        i += 1

    return books_to_return


@books_search_router.post(path="/book_name/{book_name}/add",
                          status_code=status.HTTP_201_CREATED,
                          operation_id="insert_book")
def insert_book(book: Books):
    """
    This endpoint inserts a book with its properties
    """
    db_books_util.insert_book(title=book.title, isbn=book.isbn, author=book.author,
                              picture=book.picture, description=book.description)


@books_search_router.put(path="/likes_count",
                         status_code=status.HTTP_200_OK,
                         operation_id="update_likes_count")
def update_likes_count(likes_count: LikesCount):
    """
    This endpoint update the like count for each book.
    """

    payload = {}
    book_list = likes_count.book_ids.split('')  # split the list
    keep_track = []
    try:
        for _id in book_list:
            keep_track.append(_id)
            db_books_util.update_likes_book(book_id=_id, operator=likes_count.offset)
            book_likes_count = db_books_util.get_likes_book(book_id=_id)
            if book_likes_count:
                payload[_id] = book_likes_count.get('likes_count')
    except Exception:
        # revert
        for _id in keep_track:
            db_books_util.update_likes_book(book_id=_id, operator=likes_count.offset*-1)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return {'success': True, 'payload': payload}


@books_search_router.get(path="/likes_count/book_id/{book_id}",
                         status_code=status.HTTP_200_OK,
                         operation_id="get_likes_count")
def get_likes_count(book_id: str):
    """
    This endpoint returns the likes count for a book.
    """
    result = db_books_util.get_likes_book(book_id=book_id)
    # if _id does not exist, return 404 not found status code
    if not result:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return {'success': True, 'payload': result}
