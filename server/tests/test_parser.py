import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from server.services.parser import extract_text


def test_extract_txt(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("hello world")
    assert "hello" in extract_text(str(f))


def test_unsupported(tmp_path):
    f = tmp_path / "b.xyz"
    f.write_text("x")
    with pytest.raises(ValueError):
        extract_text(str(f))
