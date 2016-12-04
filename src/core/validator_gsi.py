# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError


def validate_order(value):
    """**The method makes the validation of numerical field on a positive number.**

    :Arguments:
        * *value*: Input value

    """

    if value < 0:
        raise ValidationError('{0} invalid value. Order must be a positive number'.format(value))

    return value
