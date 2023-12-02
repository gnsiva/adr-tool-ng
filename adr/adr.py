import glob
import os
import re
import shutil
from datetime import datetime
from enum import Enum

import typer

template = """\
# No. XXXXX: {title}

## Status timeline

* {date} - Proposed

## Context

## Decision

## Consequences

"""

app = typer.Typer()


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
    now = int(datetime.utcnow().timestamp())
    os.makedirs(".adr-backup", exist_ok=True)
    shutil.copy(filename, f".adr-backup/{filename}.{now}")


@app.command()
def create(title: str) -> None:
    """Creates a new ADR file with the provided title."""
    filename = f"XXXXX-{kebab_case(title)}.md"
    content = template.format(
        date=get_date(),
        title=title,
    )
    with open(filename, 'w') as file:
        file.write(content)
    typer.echo(f"ADR created: {filename}")


def update_status(filename: str, status: Status) -> None:
    """Read the file in, update the status including the current date.

    The logic for updating is that
    1. It finds the "Status timeline" subheading
    2. It finds the first bulleted list
    3. It appends to the end of the bulleted list
    """
    # read in adr
    with open(filename, "r") as f:
        lines = f.readlines()

    # find where to insert the status update
    i = 0
    status_block_found = False
    last_bullet_i = None
    while i < len(lines):
        if lines[i].startswith("## Status"):
            # you have found the status subheading
            status_block_found = True
        elif status_block_found:
            # you are within the status subheading, and trying to find the last bullet
            if lines[i].startswith("*"):
                last_bullet_i = i
            elif lines[i].startswith("## "):
                # reached the next section
                break
        i += 1

    if last_bullet_i is None:
        typer.echo("Status list not found!")
        typer.Exit(42)

    # insert the new status and write the file
    lines.insert(i - 1, f"* {get_date()} - {status.value.capitalize()}\n")
    with open(filename, "w") as f:
        f.writelines(lines)


def insert_adr_number(filename: str, adr_number: int) -> None:
    with open(filename, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith("# No. XXXXX: "):
            lines[i] = line.replace("XXXXX", f"{adr_number:05}")
            break
    else:
        typer.echo("Proposed ADR number entry template not found, check your title.")
        typer.Exit(42)

    with open(filename, "w") as f:
        f.writelines(lines)


@app.command()
def approve(filename: str) -> None:
    """Confirms the ADR by setting the decision number and updating the status."""
    adr_number = get_next_adr_number()

    backup_file(filename=filename)

    # update the status
    update_status(filename=filename, status=Status.Approved)

    # TODO - update ADR number in the file itself
    insert_adr_number(filename=filename, adr_number=adr_number)

    # rename the file with number
    new_filename = filename.replace("XXXXX", f"{adr_number:05}")
    os.rename(filename, new_filename)


if __name__ == "__main__":
    app()
