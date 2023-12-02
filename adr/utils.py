import glob
import os
import re
import shutil
from datetime import datetime
from enum import Enum


class Status(Enum):
    Proposed = "Proposed"
    Approved = "Approved"
    Rejected = "Rejected"


def kebab_case(s: str) -> str:
    """Convert string with spaces into lower case kebab case."""
    return re.sub(r"\s+", '-', s.strip().lower())


def get_date() -> str:
    """Get the date in the format used across the project."""
    return datetime.now().strftime("%Y-%m-%d")


def get_next_adr_number() -> int:
    """Find all ADRs and determine the number the next ADR should have."""
    adr_files = glob.glob('[0-9][0-9][0-9][0-9][0-9]-*.md')
    adr_numbers = [int(s.split("-")[0]) for s in adr_files]
    higest_adr = max(adr_numbers, default=0)
    return higest_adr + 1


def backup_file(filename: str) -> None:
    """Create a copy of the current state of the file, before destructive actions."""
    now = int(datetime.now().timestamp())
    os.makedirs(".adr-backup", exist_ok=True)
    shutil.copy(filename, f".adr-backup/{filename}.{now}")
