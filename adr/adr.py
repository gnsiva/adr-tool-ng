import os

import typer

from adr.markdown_editing import (
    update_status,
    insert_adr_number,
)
from adr.utils import (
    Status,
    backup_file,
    get_date,
    get_next_adr_number,
    kebab_case,
)

template = """\
# No. XXXXX: {title}

## Status timeline

* {date} - Proposed

## Context

## Decision

## Consequences

"""

app = typer.Typer()


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


# def update_status(filename: str, status: Status) -> None:
#     """Read the file in, update the status including the current date.
#
#     The logic for updating is that
#     1. It finds the "Status timeline" subheading
#     2. It finds the first bulleted list
#     3. It appends to the end of the bulleted list
#     """
#     # read in adr
#     with open(filename, "r") as f:
#         lines = f.readlines()
#
#     # find where to insert the status update
#     i = 0
#     status_block_found = False
#     last_bullet_i = None
#     while i < len(lines):
#         if lines[i].startswith("## Status"):
#             # you have found the status subheading
#             status_block_found = True
#         elif status_block_found:
#             # you are within the status subheading, and trying to find the last bullet
#             if lines[i].startswith("*"):
#                 last_bullet_i = i
#             elif lines[i].startswith("## "):
#                 # reached the next section
#                 break
#         i += 1
#
#     if last_bullet_i is None:
#         typer.echo("Status list not found!")
#         typer.Exit(42)
#
#     # insert the new status and write the file
#     lines.insert(i - 1, f"* {get_date()} - {status.value.capitalize()}\n")
#     with open(filename, "w") as f:
#         f.writelines(lines)
#
#
# def insert_adr_number(filename: str, adr_number: int) -> None:
#     with open(filename, "r") as f:
#         lines = f.readlines()
#
#     for i, line in enumerate(lines):
#         if line.startswith("# No. XXXXX: "):
#             lines[i] = line.replace("XXXXX", f"{adr_number:05}")
#             break
#     else:
#         typer.echo("Proposed ADR number entry template not found, check your title.")
#         typer.Exit(42)
#
#     with open(filename, "w") as f:
#         f.writelines(lines)
#

@app.command()
def approve(filename: str) -> None:
    """Confirms the ADR by setting the decision number and updating the status."""
    adr_number = get_next_adr_number()

    backup_file(filename=filename)

    # read in file
    with open(filename, "r") as f:
        lines = f.readlines()

    # update the status
    lines = update_status(lines=lines, status=Status.Approved)

    # TODO - update ADR number in the file itself
    lines = insert_adr_number(lines=lines, adr_number=adr_number)

    with open(filename, "w") as f:
        f.writelines(lines)

    # rename the file with number
    new_filename = filename.replace("XXXXX", f"{adr_number:05}")
    os.rename(filename, new_filename)


if __name__ == "__main__":
    app()
