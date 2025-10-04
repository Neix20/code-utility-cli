
import pytest
from app.processor.processor import JoinLinesProcessor


@pytest.fixture
def processor():
    """Fixture to initialize the processor once per test."""
    return JoinLinesProcessor()


def test_join_multiple_lines(processor):
    data = ["Hello", "world", "from", "pytest"]
    result = processor.process(data)
    assert result == "Hello world from pytest"


def test_join_single_line(processor):
    data = ["Hello"]
    result = processor.process(data)
    assert result == "Hello"


def test_join_empty_list(processor):
    data = []
    result = processor.process(data)
    assert result == ""  # join() on empty list should return empty string


def test_join_with_whitespace(processor):
    data = ["  leading", "and", "trailing  "]
    result = processor.process(data)
    # Expect spaces preserved, only joined with single space
    assert result == "  leading and trailing  ".strip()


def test_output_type_is_str(processor):
    data = ["one", "two", "three"]
    result = processor.process(data)
    assert isinstance(result, str)
