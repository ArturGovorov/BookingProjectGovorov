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
def test_create_booking_invalid_data(api_client, mocker):
    invalid_booking_data = {
        "invalid_field": "invalid_value"
    }
    mock_response = mocker.Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = HTTPError("400 Client Error")
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)

    with allure.step('Verify HTTPError is raised for invalid data'):
        with pytest.raises(HTTPError, match="400 Client Error"):
            api_client.create_booking(invalid_booking_data)

    with allure.step('Verify status code check fails for non-200 response'):
        mock_response.raise_for_status.side_effect = None
        with pytest.raises(AssertionError, match="Expected status 200 but got 400"):
            api_client.create_booking(invalid_booking_data)


@allure.feature('Test Booking')
@allure.story('Test creating booking with valid data')
def test_create_booking_valid_data(api_client, mocker):
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
    expected_response = {"bookingid": 111, "booking": valid_booking_data}

    mock_success_response = mocker.Mock()
    mock_success_response.status_code = 200
    mock_success_response.json.return_value = expected_response
    mocker.patch.object(api_client.session, 'post', return_value=mock_success_response)

    result = api_client.create_booking(valid_booking_data)

    if isinstance(result, dict):
        assert result == expected_response
    else:
        assert result.status_code == 200
        assert result.json() == expected_response