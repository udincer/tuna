import subprocess
import time
from pathlib import Path

import tuna  # noqa


def test_tuna():
    this_dir = Path(__file__).resolve().parent
    filename = this_dir / "foo.prof"
    cmd = ["tuna", filename, "--no-browser"]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # give server time to start up
    time.sleep(3)
    p.terminate()


def test_importprofile(tmp_path):
    content = """
import time:       3 |    22 |     c
import time:       2 |    15 |   b
import time:       1 |    12 | a
"""

    ref = {
        "text": ["main"],
        "color": 0,
        "children": [
            {
                "text": ["a"],
                "value": 1e-06,
                "color": 0,
                "children": [
                    {
                        "text": ["b"],
                        "value": 2e-06,
                        "color": 0,
                        "children": [{"text": ["c"], "value": 3e-06, "color": 0}],
                    }
                ],
            }
        ],
    }

    filepath = tmp_path / "test.log"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    out = tuna.read_import_profile(filepath)

    assert out == ref, ref


def test_importprofile_multiprocessing(tmp_path):
    # when using multiprocessing, you can have seemingly excessive indentation,
    # see <https://github.com/nschloe/tuna/issues/53>
    content = """
import time:       5 |    22 |       e
import time:       4 |    22 |   d
import time:       3 |    22 |     c
import time:       2 |    15 |   b
import time:       1 |    12 | a
"""
    ref = {
        "text": ["main"],
        "color": 0,
        "children": [
            {
                "text": ["a"],
                "value": 1e-06,
                "children": [
                    {
                        "text": ["b"],
                        "value": 2e-06,
                        "children": [
                            {
                                "text": ["c"],
                                "value": 3e-06,
                                "children": [
                                    {
                                        "text": ["e"],
                                        "value": 4.9999999999999996e-06,
                                        "color": 0,
                                    }
                                ],
                                "color": 0,
                            }
                        ],
                        "color": 0,
                    },
                    {"text": ["d"], "value": 4e-06, "color": 0},
                ],
                "color": 0,
            }
        ],
    }

    filepath = tmp_path / "test.log"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    out = tuna.read_import_profile(filepath)

    assert out == ref, ref


if __name__ == "__main__":
    test_tuna()
