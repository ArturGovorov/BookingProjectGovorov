import allure
import pytest
from requests.exceptions import HTTPError


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
