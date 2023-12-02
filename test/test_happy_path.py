import os
from datetime import datetime
from pathlib import Path
from typing import Generator
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from adr.adr import app


@pytest.fixture
def change_dir(tmp_path: Path) -> Generator[None, None, None]:
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    yield
    # go back to original directory
    os.chdir(original_dir)


@pytest.fixture
def test_data_dir() -> Path:
    current_dir = Path(__file__).parent
    return current_dir / "resources" / "happy-path"


@pytest.fixture
def mock_datetime_utcnow() -> Generator[Mock, None, None]:
    """Set the date for when the test runs."""
    with patch("adr.adr.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2013, 12, 1, 12)
        yield mock_datetime


def read_file_contents(file_path: Path) -> str:
    with open(file_path, "r") as f:
        return f.read()


def test_creating_and_approving(
        change_dir: None,
        mock_datetime_utcnow: Mock,
        tmp_path: Path,
        test_data_dir: Path,
) -> None:
    """Basic happy path test to help stop regressions during early development."""
    title = "My Important Decision"
    expected_proposed_filename = "XXXXX-my-important-decision.md"
    expected_approved_filename = "00001-my-important-decision.md"

    runner = CliRunner()

    # ========
    # creating the proposed file test
    create_result = runner.invoke(app, ["create", title])
    assert create_result.exit_code == 0
    proposed_file = tmp_path / expected_proposed_filename
    assert proposed_file.exists()

    assert read_file_contents(test_data_dir / expected_proposed_filename) \
        == read_file_contents(proposed_file)

    # ========
    # approving the file test
    approve_result = runner.invoke(app, ["approve", expected_proposed_filename])
    assert approve_result.exit_code == 0

    # the original approved file shouldn't be there
    assert not proposed_file.exists()

    # it should have been renamed
    approved_file = tmp_path / expected_approved_filename
    assert approved_file.exists()

    # check contents as expected
    assert read_file_contents(test_data_dir / expected_approved_filename) \
        == read_file_contents(approved_file)
