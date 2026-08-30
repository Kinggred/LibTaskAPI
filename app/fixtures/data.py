from app.models.common import BookState

BOOKS = [
    {
        "serial": "100001",
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100002",
        "title": "1984",
        "author": "George Orwell",
        "state": BookState.BORROWED,
    },
    {
        "serial": "100003",
        "title": "Brave New World",
        "author": "Aldous Huxley",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100004",
        "title": "Dune",
        "author": "Frank Herbert",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100005",
        "title": "Fahrenheit 451",
        "author": "Ray Bradbury",
        "state": BookState.BORROWED,
    },
    {
        "serial": "100006",
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100007",
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100008",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100009",
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100010",
        "title": "Animal Farm",
        "author": "George Orwell",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100011",
        "title": "The Trial",
        "author": "Franz Kafka",
        "state": BookState.AVAILABLE,
    },
    {
        "serial": "100012",
        "title": "Solaris",
        "author": "Stanisław Lem",
        "state": BookState.BORROWED,
    },
]


READERS = [
    {"card_no": "200001"},
    {"card_no": "200002"},
    {"card_no": "200003"},
    {"card_no": "200004"},
]


BORROWS = [
    {
        "book_serial": "100002",
        "reader_card_no": "200001",
    },
    {
        "book_serial": "100005",
        "reader_card_no": "200002",
    },
    {
        "book_serial": "100012",
        "reader_card_no": "200003",
    },
]
