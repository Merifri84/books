from random import randint
import random
import string
from base import copy_and_fill_db
import pytest

random_book_id = randint(1, 3)
random_non_existing_book_id = randint(4, 100)
random_non_existing_book_year = randint(1, 1000)
random_string = ''.join(random.choice(string.ascii_letters) for i in range(10))


def test_positive_add_book(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute("INSERT INTO test_books (title, author, year) VALUES ('Cookbook', 'Connor', 2024)")
    copy_and_fill_db.commit()
    cursor.execute("SELECT * FROM test_books WHERE title='Cookbook'")
    book = cursor.fetchone()
    assert book
    assert book[1] == 'Cookbook'


def test_positive_all_books(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute("SELECT * FROM test_books")
    rows = cursor.fetchall()
    num_rows = len(rows)
    if num_rows == 3:
        assert True
    else:
        assert False, f"Number of books are not equal 3, it's {num_rows}"


def test_positive_get_info_by_id(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute(f"SELECT * FROM test_books WHERE id = {random_book_id}")
    book = cursor.fetchone()
    assert book
    print(f'"\n"Id = {book[0]}, title = {book[1]}, author = {book[2]}, year = {book[3]}')


def test_positive_update_book(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    copy_and_fill_db.commit()
    cursor.execute("UPDATE test_books SET title=?, author=?, year=? WHERE id=?",
                   ('Handbook', 'Mikhailov', 2011, 1))
    copy_and_fill_db.commit()
    cursor.execute("SELECT * FROM test_books WHERE id = 1")
    book = cursor.fetchone()
    assert book
    assert book[1] == 'Handbook'
    assert book[2] == 'Mikhailov'
    assert book[3] == 2011


def test_positive_delete_book(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute("DELETE FROM test_books WHERE id = 2")
    copy_and_fill_db.commit()
    cursor.execute("SELECT * FROM test_books WHERE id = 2")
    book = cursor.fetchone()
    assert book is None
    print('"\n"Book with id = 2 deleted successfully')


def test_negative_get_book_by_non_existing_id(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute(f"SELECT * FROM test_books WHERE id = {random_non_existing_book_id}")
    book = cursor.fetchone()
    assert book is None
    print(f'"\n"Book with id - {random_non_existing_book_id} is not exist')


def test_negative_get_book_by_non_existing_title(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute(f"SELECT * FROM test_books WHERE title like ('{random_string}')")
    book = cursor.fetchone()
    assert book is None
    print(f'"\n"Book with title - {random_string} is not exist')


def test_negative_get_book_by_non_existing_author(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute(f"SELECT * FROM test_books WHERE author like ('{random_string}')")
    book = cursor.fetchone()
    assert book is None
    print(f'"\n"Book with author - {random_string} is not exist')


def test_negative_get_book_by_non_existing_year(copy_and_fill_db):
    cursor = copy_and_fill_db.cursor()
    cursor.execute(f"SELECT * FROM test_books WHERE year = {random_non_existing_book_year}")
    book = cursor.fetchone()
    assert book is None
    print(f'"\n"Book with year - {random_non_existing_book_year} is not exist')
