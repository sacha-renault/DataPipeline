class ValidationError(Exception):
    """
    Exception raised for errors in data validation.

    This exception is used to indicate that data has failed a validation check. It is 
    typically raised by validator classes when the data does not meet specified criteria.

    Inherits from:
        Exception: Base class for all built-in exceptions.

    Examples:
        >>> if not some_validation_check(data):
        >>>     raise ValidationError("The data did not meet the validation criteria.")
    """
    pass