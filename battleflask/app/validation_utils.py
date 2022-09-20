import battleflask.app.exceptions as ex


def validate_is_not_empty_string(value: str | None) -> None:
    if is_empty_string(value):
        raise ex.IsEmptyStringException(f'Passed value "{value}" is not valid')


def is_empty_string(value: str | None) -> bool:
    return value is None or not isinstance(value, str) or len(value.strip()) == 0
