import os
from datetime import datetime

from src.utils.utils import hash_new_password, is_correct_password, get_datetime_iso_format, get_expiration_datetime


def test_hash_new_password():
    password_hashed = hash_new_password("password")
    assert password_hashed is not None


def test_is_correct_password():
    is_correct = is_correct_password("ab".encode(), "ab".encode(), "password")
    assert is_correct is False


def test_get_datetime_iso_format():
    datetime_iso_format = get_datetime_iso_format(datetime.now())
    assert datetime_iso_format is not None


def test_get_expiration_datetime():
    datetime_expiration = get_expiration_datetime()
    assert datetime_expiration is not None
