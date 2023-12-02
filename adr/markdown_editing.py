
import typer

from adr.utils import (
    Status,
    get_date,
)


def update_status(lines: list[str], status: Status) -> list[str]:
    """Add a status entry line to the status subsection.

    The logic for updating is that
    1. It finds the "Status timeline" subheading
    2. It finds the first bulleted list
    3. It appends to the end of the bulleted list
    """
    lines = lines[:]

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
        raise typer.Exit(42)

    # insert the new status and write the file
    lines.insert(i - 1, f"* {get_date()} - {status.value.capitalize()}\n")

    return lines


def insert_adr_number(lines: list[str], adr_number: int) -> list[str]:
    """Fill in the ADR number within the markdown text (passed hear after reading)."""
    lines = lines[:]

    for i, line in enumerate(lines):
        if line.startswith("# No. XXXXX: "):
            lines[i] = line.replace("XXXXX", f"{adr_number:05}")
            break
    else:
        typer.echo("Proposed ADR number entry template not found, check your title.")
        raise typer.Exit(42)

    return lines

