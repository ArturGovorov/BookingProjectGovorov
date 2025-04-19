from enum import Enum


class Users(Enum):
    USERNAME = "admin"
    PASSWORD = "password123"


class Timeouts(Enum):
    TIMEOUT = 5


class TestBookingData:
    BOOKING_ID = 1
    EXPECTED_BOOKING_DATA = {
        "firstname": "Sally",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2013-02-23",
            "checkout": "2014-10-23"
        },
        "additionalneeds": "Breakfast"
    }
