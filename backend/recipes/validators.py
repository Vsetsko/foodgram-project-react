from django.core.validators import RegexValidator


ENTER_HEX_MESSAGE = 'Введите корректный HEX-код цвета.'


def validate_hex(value):
    hex_regex = r'^#(?:[0-9a-fA-F]{3}){1,2}$'
    hex_validator = RegexValidator(
        hex_regex, message=ENTER_HEX_MESSAGE, code='invalid_hex'
    )
    hex_validator(value)
