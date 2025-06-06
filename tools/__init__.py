from __future__ import annotations

from datetime import datetime, timedelta
import random


def utc_to_pacific(utc_dt: datetime) -> datetime:
    """Convert UTC datetime to Pacific Time by subtracting 3 hours."""
    return utc_dt - timedelta(hours=3)


def format_pacific_time() -> str:
    """Return the current time formatted in Pacific Time."""
    pacific = utc_to_pacific(datetime.utcnow())
    return pacific.strftime('%Y-%m-%d %H:%M:%S PT')


NYC_PLACES = ["Brooklyn", "Dumbo", "Queens"]


def random_nyc_location() -> str:
    """Return a random NYC location from the predefined list."""
    return random.choice(NYC_PLACES)
