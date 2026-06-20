#!/usr/bin/env python3
# ponytail: validation only; the "ok" branch touches the real Recents list, not tested here
import tempfile, pathlib
from touch_for_recents import add_to_recents


def test_validation():
    assert add_to_recents("/no/such/xyz.txt") is False    # does not exist
    with tempfile.TemporaryDirectory() as d:
        assert add_to_recents(d) is False                 # not a regular file
        f = pathlib.Path(d) / "ok.txt"
        f.write_text("x")
        assert add_to_recents(str(f)) is True             # valid file -> added


if __name__ == "__main__":
    test_validation()
    print("OK")
