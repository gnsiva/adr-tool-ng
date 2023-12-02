import os

import typer

from adr.markdown_editing import (
    insert_adr_number,
    update_status,
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
