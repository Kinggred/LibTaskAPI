from fastapi import status


def test_create_reader(client):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": "123456",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["card_no"] == "123456"


def test_create_reader_preserves_leading_zeroes(client):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": "001234",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["card_no"] == "001234"


def test_create_reader_rejects_non_numeric_card_number(client):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": "12AB56",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json() == {"detail": "Identifier must contain digits only.", "fields": "card_no"}


def test_create_reader_rejects_short_card_number(client):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": "12345",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    body = response.json()

    assert "detail" in body
    assert isinstance(body["detail"], str)


def test_create_reader_rejects_long_card_number(client):
    response = client.post(
        "/api/v1/readers/",
        json={
            "card_no": "1234567",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    body = response.json()

    assert "detail" in body
    assert isinstance(body["detail"], str)


def test_create_reader_rejects_missing_card_number(client):
    response = client.post(
        "/api/v1/readers/",
        json={},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    body = response.json()

    assert "detail" in body
    assert isinstance(body["detail"], str)


def test_create_reader_rejects_duplicate_card_number(client):
    payload = {
        "card_no": "654321",
    }

    first_response = client.post(
        "/api/v1/readers/",
        json=payload,
    )

    assert first_response.status_code == status.HTTP_200_OK

    second_response = client.post(
        "/api/v1/readers/",
        json=payload,
    )

    assert second_response.status_code == status.HTTP_409_CONFLICT
    assert second_response.json() == {"detail": "Provided value already exists"}


def test_get_readers(client):
    client.post(
        "/api/v1/readers/",
        json={"card_no": "111111"},
    )

    client.post(
        "/api/v1/readers/",
        json={"card_no": "222222"},
    )

    response = client.get("/api/v1/readers/")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert "items" in body
    assert "total" in body

    card_numbers = {reader["card_no"] for reader in body["items"]}

    assert "111111" in card_numbers
    assert "222222" in card_numbers


def test_validation_error_has_standard_response_format(client):
    response = client.post(
        "/api/v1/readers/",
        json={"card_no": "ABCDEF"},
    )

    assert response.status_code == 422

    assert response.json() == {"detail": "Identifier must contain digits only.",  "fields": "card_no"}


def test_conflict_error_has_standard_response_format(client):
    client.post(
        "/api/v1/readers/",
        json={"card_no": "123456"},
    )

    response = client.post(
        "/api/v1/readers/",
        json={"card_no": "123456"},
    )

    assert response.status_code == 409

    assert response.json() == {"detail": "Provided value already exists"}


def test_error_response_detail_is_not_fastapi_validation_list(client):
    response = client.post(
        "/api/v1/readers/",
        json={"card_no": "invalid"},
    )

    body = response.json()

    assert isinstance(body["detail"], str)
