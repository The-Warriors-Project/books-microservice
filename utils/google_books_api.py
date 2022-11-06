import requests
import consts


def get_book_from_google_by_title(data: str, field: str):
    """
    This function retrieve data from google API
    :param data: the data to retrieve
    :param field: the topic to retrieve
    :return:
    """
    if field == consts.NAME:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle+{data}")
    elif field == consts.AUTHOR:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=inauthor+{data}")
    format_response = response.json().get('items')[0].get('volumeInfo')  # get the first item from the list

    title = format_response.get('title')
    author = format_response.get('authors')
    description = format_response.get('description')
    isbn = format_response.get('industryIdentifiers')[0].get('identifier')
    picture = format_response.get('imageLinks').get('thumbnail')
    return [title, author, description, isbn, picture]


