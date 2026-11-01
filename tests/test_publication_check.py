import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "check_publication.py"
spec = importlib.util.spec_from_file_location("publication_check", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PublicationCheckTests(unittest.TestCase):
    def test_public_hardware_and_revision_are_allowed(self):
        text = b"HKFG-XX i7-13700H PCI 8086:A7A0 rev 04 OpenCore 1.0.8"
        self.assertEqual(module.inspect_blob("docs/hardware.md", text), [])

    def test_sensitive_values_are_detected(self):
        # Deliberately synthetic identifiers, never copied from a machine.
        cases = [
            b"-".join([b"00112233", b"4455", b"6677", b"8899", b"aabbccddeeff"]),
            b":".join([b"aa", b"bb", b"cc", b"dd", b"ee", b"ff"]),
            b"someone" + b"@" + b"example.invalid",
            b"/home" + b"/example/private",
            b"SystemSerialNumber" + b"=EXAMPLEVALUE",
            b"MLB" + b"=EXAMPLEVALUE",
            b"SSID" + b"=ExampleNetwork",
            b".".join([b"192", b"0", b"2", b"10"]),
        ]
        for value in cases:
            with self.subTest(value=value):
                self.assertTrue(module.inspect_blob("notes.md", value))

    def test_placeholders_are_allowed(self):
        self.assertEqual(module.inspect_blob("notes.md", b"SystemSerialNumber=REDACTED"), [])

    def test_raw_files_are_blocked_even_without_secrets(self):
        for name in ["EFI/OC/config.plist", "dump.aml", "raw/report.txt", "photo.jpeg"]:
            with self.subTest(name=name):
                self.assertTrue(module.inspect_blob(name, b"public words"))

    def test_binary_is_blocked(self):
        self.assertTrue(module.inspect_blob("notes.md", b"\xff\x00"))

    def test_index_is_checked_instead_of_cleaned_worktree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            note = root / "note.md"
            note.write_bytes(b"MLB" + b"=SYNTHETICVALUE")
            subprocess.run(["git", "add", "note.md"], cwd=root, check=True)
            note.write_text("Public text after working-tree cleanup")
            result = subprocess.run(
                [sys.executable, str(path)], cwd=root,
                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("identifier assignment", result.stderr)
            self.assertNotIn("SYNTHETICVALUE", result.stderr)

if __name__ == "__main__":
    unittest.main()

