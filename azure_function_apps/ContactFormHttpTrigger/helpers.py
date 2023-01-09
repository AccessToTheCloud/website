from typing import Optional
from flanker.addresslib import address


def validate_email(email: str) -> Optional[str]:
    return address.parse(email, addr_spec_only=True)
