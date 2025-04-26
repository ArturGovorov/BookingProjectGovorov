import allure
import pytest
from requests.exceptions import HTTPError


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
