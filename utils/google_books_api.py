import requests
import consts


def get_books_from_google_by_title(data: str, field: str) -> dict:
    """
    This function retrieve data from google API
    :param data: the data to retrieve
    :param field: the topic to retrieve
    :return: the books
    """
    if field == consts.NAME:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=intitle+{data}")
    elif field == consts.AUTHOR:
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=inauthor+{data}")

    books = {}
    for i in range(5):  # takes the first five books in the Google api response
        format_response = response.json().get('items')[i].get('volumeInfo')  # get the first item from the list
        title, author, description, isbn, picture = extract_data_from_google_dict(response=format_response)
        books[i] = {'title': title, 'author': author, 'description': description,
                    'isbn': isbn, 'picture': picture}

    return books


def extract_data_from_google_dict(response: dict):
    '''
    This function takes the output of google_api and parse it
    :param response: the original output of google_books api
    :return: the parsed data
    '''
    title = response.get('title')
    author = response.get('authors')
    description = response.get('description')
    isbn = response.get('industryIdentifiers')[0].get('identifier')
    picture = response.get('imageLinks').get('thumbnail')

    return [title, author, description, isbn, picture]
