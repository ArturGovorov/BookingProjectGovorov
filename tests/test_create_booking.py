import allure
import pytest
import requests
from requests.exceptions import HTTPError
from pydantic import ValidationError
from core.models.booking import BookingResponse
from faker import Faker

fake = Faker()


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with invalid data')
def test_create_booking_invalid_data(api_client):
    invalid_booking_data = {
        "invalid_field": "invalid_value"
    }

    with allure.step('Verify API rejects invalid data'):
        with pytest.raises(HTTPError):
            api_client.create_booking(invalid_booking_data)


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with valid data')
def test_create_booking_valid_data(api_client):
    valid_booking_data = {
        "firstname": "Arthur",
        "lastname": "Dru",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-10"
        },
        "additionalneeds": "Breakfast"
    }

    with allure.step('Create booking with valid data'):
        response = api_client.create_booking(valid_booking_data)

    with allure.step('Verify response contains booking data'):
        assert isinstance(response, dict)
        assert "bookingid" in response
        assert "booking" in response
        assert response["booking"] == valid_booking_data


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValueError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with random data')
def test_create_booking_with_random_data(generate_random_booking_data, booking_dates, api_client):
    booking_data = generate_random_booking_data
    booking_data["bookingdates"] = booking_dates
    response = api_client.create_booking(booking_data)

    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValueError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates']['checkin'] == booking_data['bookingdates']['checkin']
    assert response['booking']['bookingdates']['checkout'] == booking_data['bookingdates']['checkout']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']


@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with incorrect data')
def test_create_booking_with_incorrect_data(api_client):
    invalid_booking_data = {
        "firstname": "",
        "lastname": "",
        "totalprice": "Ivan",
        "depositpaid": None,
        "bookingdates": {
            "checkin": "Privet",
            "checkout": "Poka"
        },
        "additionalneeds": 1
    }

    with pytest.raises(requests.exceptions.HTTPError):
        api_client.create_booking(invalid_booking_data)