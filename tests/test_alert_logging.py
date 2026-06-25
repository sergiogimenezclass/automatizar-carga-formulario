import os
import tempfile
import unittest
from pathlib import Path

from main import emit_alert


class EmitAlertTests(unittest.TestCase):
    def test_emit_alert_writes_a_log_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            previous_cwd = Path.cwd()
            os.chdir(tmpdir)
            try:
                emit_alert("error de prueba")
                log_path = Path("alerts.log")
                self.assertTrue(log_path.exists())
                content = log_path.read_text(encoding="utf-8")
                self.assertIn("error de prueba", content)
            finally:
                os.chdir(previous_cwd)


if __name__ == "__main__":
    unittest.main()
