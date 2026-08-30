from fastapi import status


def create_reader(client, card_no: str = "123456"):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": card_no,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    return response.json()


def create_book(
    client,
    serial: str = "654321",
    title: str = "The Hobbit",
    author: str = "J.R.R. Tolkien",
):
    response = client.post(
        "/api/v1/books/",
        json={
            "serial": serial,
            "title": title,
            "author": author,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    return response.json()

def test_borrow_book(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="654321",
    )

    response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["serial"] == "654321"
    assert body["state"] == "borrowed"

def test_borrowed_book_is_returned_with_borrow_record(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="654321",
    )

    response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    response = client.get(
        "/api/v1/books/",
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    book = next(
        item
        for item in body["items"]
        if item["serial"] == "654321"
    )

    assert book["state"] == "borrowed"

    assert book["borrow_record"] is not None
    assert book["borrow_record"]["reader_card_no"] == "123456"
    assert book["borrow_record"]["borrowed_at"] is not None

def test_available_book_has_no_borrow_record(client):
    create_book(
        client,
        serial="654321",
    )

    response = client.get(
        "/api/v1/books/",
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    book = next(
        item
        for item in body["items"]
        if item["serial"] == "654321"
    )

    assert book["state"] == "available"
    assert book["borrow_record"] is None

def test_return_book(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="654321",
    )

    borrow_response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert borrow_response.status_code == status.HTTP_200_OK

    response = client.delete(
        "/api/v1/books/654321/borrow",
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["serial"] == "654321"
    assert body["state"] == "available"

def test_returned_book_has_no_active_borrow_record(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="654321",
    )

    client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    return_response = client.delete(
        "/api/v1/books/654321/borrow",
    )

    assert return_response.status_code == status.HTTP_200_OK

    response = client.get(
        "/api/v1/books/",
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    book = next(
        item
        for item in body["items"]
        if item["serial"] == "654321"
    )

    assert book["state"] == "available"
    assert book["borrow_record"] is None

def test_borrow_nonexistent_book(client):
    create_reader(
        client,
        card_no="123456",
    )

    response = client.post(
        "/api/v1/books/999999/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {
        "detail": "Book not found"
    }

def test_borrow_with_nonexistent_reader(client):
    create_book(
        client,
        serial="654321",
    )

    response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "999999",
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {
        "detail": "Reader not found"
    }

def test_borrow_already_borrowed_book(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="654321",
    )

    first_response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert first_response.status_code == status.HTTP_200_OK

    second_response = client.post(
        "/api/v1/books/654321/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert second_response.status_code == status.HTTP_409_CONFLICT

    assert second_response.json() == {
        "detail": "Book not available"
    }

def test_borrow_book_rejects_invalid_serial(client):
    response = client.post(
        "/api/v1/books/123/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    body = response.json()

    assert body["fields"] == "serial"
    assert isinstance(body["detail"], str)

def test_get_books_pagination(client):
    create_book(
        client,
        serial="100001",
    )

    create_book(
        client,
        serial="100002",
    )

    create_book(
        client,
        serial="100003",
    )

    response = client.get(
        "/api/v1/books/",
        params={
            "page": 1,
            "size": 2,
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["page"] == 1
    assert body["size"] == 2
    assert len(body["items"]) == 2
    assert body["total"] >= 3

def test_book_pagination_contains_one_entry_per_book(client):
    create_reader(
        client,
        card_no="123456",
    )

    create_book(
        client,
        serial="100001",
    )

    create_book(
        client,
        serial="100002",
    )

    client.post(
        "/api/v1/books/100001/borrow",
        json={
            "reader_card_no": "123456",
        },
    )

    response = client.get(
        "/api/v1/books/",
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    serials = [
        item["serial"]
        for item in body["items"]
    ]

    assert serials.count("100001") == 1
    assert serials.count("100002") == 1