import click
import pytest

from adr.markdown_editing import insert_adr_number, update_status
from adr.utils import Status


def test_adr_number__works_under_normal_conditions() -> None:
    lines = [
        "# No. XXXXX: Some title",
        "",
        "## Subheading",
    ]
    output = insert_adr_number(lines=lines, adr_number=42)
    assert len(output) == len(lines)
    assert output[0] == "# No. 00042: Some title"
    assert lines[1:] == output[1:]


def test_adr_number__missing_title() -> None:
    lines = [
        "## Subheading",
    ]
    with pytest.raises(click.exceptions.Exit) as e:
        insert_adr_number(lines=lines, adr_number=42)
    assert e.value.exit_code == 42


def test_adr_number__already_filled_in() -> None:
    lines = [
        "# No. 00042: Some title",
        "## Subheading",
    ]
    with pytest.raises(click.exceptions.Exit) as e:
        insert_adr_number(lines=lines, adr_number=42)
    assert e.value.exit_code == 42


def test_update_status__works_under_normal_conditions() -> None:
    lines = [
        "# Heading",
        "",
        "## Status",
        "",
        "* 2023-12-1 - Proposed",
        "",
        "## Subheading",
        "Some more data",
    ]

    output = update_status(lines=lines, status=Status.Proposed)
    assert len(output) == (len(lines) + 1)

    # chop off the first couple of lines and check it still passes
    output_short = update_status(lines=lines[2:], status=Status.Proposed)
    assert len(output_short) == (len(lines[2:]) + 1)


def test_update_status__status_subheading_missing() -> None:
    lines = [
        "# Heading",
        "",
        "## Not Status",
        "",
        "* 2023-12-1 - Proposed",
        "",
        "## Subheading",
        "Some more data",
    ]

    with pytest.raises(click.exceptions.Exit) as e:
        update_status(lines=lines, status=Status.Proposed)
    assert e.value.exit_code == 42

    with pytest.raises(click.exceptions.Exit) as e:
        update_status(lines=lines, status=Status.Approved)
    assert e.value.exit_code == 42


def test_update_status__bullet_list_statuses_missing() -> None:
    lines = [
        "# Heading",
        "",
        "## Status",
        "",
        "## Subheading",
        "Some more data",
    ]

    with pytest.raises(click.exceptions.Exit) as e:
        update_status(lines=lines, status=Status.Proposed)
    assert e.value.exit_code == 42


