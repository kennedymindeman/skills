import contextlib
import io
import sys
import tempfile
import unittest
from unittest import mock
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import log  # noqa: E402

NOW = datetime(2026, 5, 24, 9, 2, tzinfo=timezone.utc)


class DecisionLogTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.path = Path(tmp.name) / "nested" / "decisions.tsv"

    def rows(self):
        return self.path.read_bytes().decode("utf-8").split("\n")

    def test_first_use_writes_header_then_row(self):
        log.append(self.path, ["frame", "counted", "size first", "commit 3a9f", "ok"], NOW)
        self.assertEqual(
            self.rows(),
            [log.HEADER.rstrip("\n"), "2026-05-24T09:02:00Z\tframe\tcounted\tsize first\tcommit 3a9f\tok", ""],
        )

    def test_appends_without_rewriting(self):
        log.append(self.path, ["a", "b", "c", "d", "e"], NOW)
        before = self.path.read_bytes()
        log.append(self.path, ["f", "g", "h", "i", "j"], NOW)
        after = self.path.read_bytes()
        self.assertTrue(after.startswith(before))
        self.assertEqual(after.count(b"ts\tphase"), 1)
        self.assertEqual(len(self.rows()), 4)

    def test_strips_tabs_and_newlines(self):
        log.append(self.path, ["p\th", "line1\nline2\r\nline3", "w", "e", "r"], NOW)
        cells = self.rows()[1].split("\t")
        self.assertEqual(len(cells), 6)
        self.assertEqual(cells[1:3], ["p h", "line1 line2  line3"])

    def test_guards_formula_cells(self):
        log.append(self.path, ["=1+1", "+cmd", "-2", "@SUM(A1)", "plain"], NOW)
        self.assertEqual(self.rows()[1].split("\t")[1:], ["'=1+1", "'+cmd", "'-2", "'@SUM(A1)", "plain"])

    def test_guard_applies_after_stripping(self):
        self.assertEqual(log.clean("\n=1"), " =1")
        self.assertEqual(log.clean(""), "")

    def test_timestamp_is_utc_iso(self):
        # A clock whose local time is five hours off UTC, so a local-time
        # stamp with a Z suffix fails on any machine.
        class Clock(datetime):
            @classmethod
            def now(cls, tz=None):
                return NOW.astimezone(tz) if tz else datetime(2026, 5, 24, 4, 2)

        with mock.patch.object(log, "datetime", Clock):
            log.append(self.path, ["a", "b", "c", "d", "e"])
        self.assertEqual(self.rows()[1].split("\t")[0], "2026-05-24T09:02:00Z")

    def test_main_rejects_wrong_arg_count(self):
        with contextlib.redirect_stderr(io.StringIO()) as err:
            self.assertEqual(log.main(["log.py", str(self.path), "only"]), 1)
        self.assertIn("usage", err.getvalue())
        self.assertFalse(self.path.exists())

    def test_main_appends(self):
        self.assertEqual(log.main(["log.py", str(self.path), "p", "d", "w", "e", "r"]), 0)
        self.assertEqual(self.rows()[1].split("\t")[1:], ["p", "d", "w", "e", "r"])


if __name__ == "__main__":
    unittest.main()
