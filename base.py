import sqlite3
import pytest
import os

books = [
        ('How to create Blog', 'Ivanov', 1984),
        ('How to fix PC', 'Petrov', 1981),
        ('How to fix lighter', 'Sidorov', 2001)
    ]


def creating_and_filling_db():
    bd_name = 'books.db'
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                             id integer PRIMARY KEY,
                                             title text,
                                             author text,
                                             year integer
                                         ); ''')
    cursor.executemany("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", books)
    conn.commit()
    conn.close()


@pytest.fixture()
def copy_and_fill_db():
    bd_name = 'test_books.db'
    conn = sqlite3.connect(bd_name)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS test_books (
                                            id integer PRIMARY KEY,
                                            title text,
                                            author text,
                                            year integer
                                        ); ''')
    cursor.executemany("INSERT INTO test_books (title, author, year) VALUES (?, ?, ?)", books)
    conn.commit()
    yield conn
    conn.close()
    os.remove(bd_name)
