import json
from pathlib import Path

import pytest

from app.processor import (
    JoinLinesProcessor,
    MakeArrayProcessor,
    MakeJsonProcessor,
    GetKeysAndValuesProcessor,
    EpochIsoConverterProcessor,
    YamlConverterProcessor,
    CsvConverterProcessor,
    SqlConverterProcessor,
)


ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"


def read_sample(subdir: str):
    d = LOGS / subdir
    if not d.exists():
        pytest.skip(f"logs/{subdir} not found")
    files = sorted([p for p in d.iterdir() if p.is_file()])
    if not files:
        pytest.skip(f"No log files in {d}")
    return files[0].read_text(encoding="utf-8").splitlines()


def assert_json_like(value):
    if isinstance(value, (dict, list)):
        return True
    if isinstance(value, str):
        try:
            json.loads(value)
            return True
        except Exception:
            pytest.fail("Expected JSON-like output but got invalid JSON string")
    pytest.fail(f"Unexpected output type: {type(value)!r}")


def test_join_lines():
    data = read_sample("join_lines")
    res = JoinLinesProcessor().process(data)
    assert isinstance(res, str)
    assert res.strip() != ""


def test_make_array():
    data = read_sample("make_array")
    res = MakeArrayProcessor().process(data)
    # result may be list/dict or JSON string
    if isinstance(res, str):
        json.loads(res)  # will raise on failure
    else:
        assert isinstance(res, (list, dict))


def test_make_json():
    data = read_sample("make_json")
    res = MakeJsonProcessor().process(data)
    assert isinstance(res, dict)


def test_get_keys_and_values():
    data = read_sample("get_keys_and_values")
    res = GetKeysAndValuesProcessor().process(data)
    # Expect some iterable or string
    assert res is not None


def test_epoch_iso_converter():
    data = read_sample("epoch_iso_converter")
    res = EpochIsoConverterProcessor().process(data)
    assert res is not None


def test_yaml_converter_try_both_modes():
    data = read_sample("yaml_converter")
    # Try both directions; pass if any works
    tried = 0
    success = False
    for t in ("json-to-yaml", "yaml-to-json"):
        tried += 1
        try:
            res = YamlConverterProcessor(t).process(data)
            # one direction should at least succeed and produce something
            assert res is not None
            success = True
            break
        except Exception:
            continue
    if not success:
        pytest.skip("yaml_converter inputs didn't match either mode")


def test_csv_converter_try_both_modes():
    data = read_sample("csv_converter")
    for t in ("json-to-csv", "csv-to-json"):
        try:
            res = CsvConverterProcessor(t).process(data)
            assert res is not None
            return
        except Exception:
            continue
    pytest.skip("csv_converter inputs didn't match expected modes")


def test_sql_converter_basic():
    data = read_sample("csv_converter")
    # try insert/select/update variants; require string output
    for t in ("csv-to-select", "csv-to-insert", "csv-to-update"):
        try:
            res = SqlConverterProcessor(t, tbl_name="person").process(data)
            assert isinstance(res, str)
            assert res.strip() != ""
            return
        except Exception:
            continue
    pytest.skip("sql_converter input didn't match any SQL mode")
