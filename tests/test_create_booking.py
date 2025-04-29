import allure
import pytest
from requests.exceptions import HTTPError


@allure.feature('Test Booking')
@allure.story('Test invalid booking creation')
def test_create_booking_unsuccessful(api_client):
    invalid_booking_data = {
        "firstname": "Arthur",
        "lastname": "Dru",
        "totalprice": -100,
        "depositpaid": "not_boolean",
        "bookingdates": {
            "checkin": "2025-04-01",
            "checkout": "2025-04-10"
        },
        "additionalneeds": "Breakfast"
    }

    with allure.step('Send invalid booking request'):
        with pytest.raises(HTTPError) as exc_info:
            api_client.create_booking(invalid_booking_data)
        assert "418" in str(exc_info.value), "Expected 418 I'm a Teapot error"


@allure.feature('Test Booking')
@allure.story('Test creating booking with invalid data')
def test_create_booking_invalid_data(api_client):
    invalid_booking_data = {
        "invalid_field": "invalid_value"
    }

    with allure.step('Verify API rejects invalid data'):
        with pytest.raises(HTTPError):
            api_client.create_booking(invalid_booking_data)


@allure.feature('Test Booking')
@allure.story('Test creating booking with valid data')
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