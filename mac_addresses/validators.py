import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from netaddr import EUI, AddrFormatError


def validate_mac_address(value: str) -> None:
    """
    Validates MAC Address that [EUI(48): Extended Unique Identifier]
    """

    default_error_messages = {
        "invalid": _("Invalid MAC Address."),
        "format_error": _("Format must be XX-XX-XX-XX-XX-XX"),
        "type_error": _("value must be string"),
    }

    if not isinstance(value, str):
        raise ValidationError(default_error_messages["type_error"], "type_error")
    try:
        EUI(value, version=48)
    except AddrFormatError:
        raise ValidationError(default_error_messages["invalid"])

    # version == 48
    if not re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
        raise ValidationError(default_error_messages["format_error"])
