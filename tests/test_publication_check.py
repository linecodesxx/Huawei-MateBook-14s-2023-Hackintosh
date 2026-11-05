import importlib.util
import json
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

    def test_reviewed_protocol_guids_are_allowed_case_insensitively(self):
        guids = [
            "7C436110-AB2A-4BBB-A880-FE41995C9F82",
            "4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14",
            "4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102",
            "8BE4DF61-93CA-11D2-AA0D-00E098032B8C",
            "3CDFF6F7-4267-4555-AD05-B30A3D8938DE",
            "4C616265-6C00-11AA-AA11-00306543ECAC",
            "0516B563-B15B-11DA-96EB-0014519758EF",
            "00000000-0000-0000-0000-000000000000",
        ]
        for guid in guids:
            for spelling in (guid, guid.lower()):
                with self.subTest(guid=guid, spelling=spelling):
                    self.assertEqual(module.inspect_blob("protocols.md", spelling.encode()), [])

    def test_unknown_uuid_remains_blocked_beside_protocol_guid(self):
        unknown = "-".join(["00112233", "4455", "6677", "8899", "aabbccddeeff"])
        text = "7C436110-AB2A-4BBB-A880-FE41995C9F82 " + unknown
        self.assertIn("UUID", module.inspect_blob("protocols.md", text.encode()))

    def test_empty_quoted_text_assignments_are_allowed(self):
        for quote in ('"', "'"):
            text = "SystemSerialNumber" + "=" + quote * 2 + "\nMLB" + "=" + quote * 2
            self.assertEqual(module.inspect_blob("notes.md", text.encode()), [])

    def test_nonempty_quoted_text_assignments_remain_blocked(self):
        for quote in ('"', "'"):
            text = "SystemSerialNumber" + "=" + quote + "SYNTHETIC VALUE" + quote
            self.assertIn("identifier assignment", module.inspect_blob("notes.md", text.encode()))

    def test_sanitized_config_json_accepts_only_empty_identity_values(self):
        name = "archive/2026-11-02_05/config.sanitized.json"
        key = "SystemSerialNumber"
        for value in ("", None, [], {}):
            text = json.dumps({"PlatformInfo": {"Generic": {key: value, "MLB": "", "ROM": "", "SystemUUID": ""}}})
            with self.subTest(empty_type=type(value).__name__):
                self.assertEqual(module.inspect_blob(name, text.encode()), [])
        for value in ("SYNTHETICVALUE", "REDACTED", 0, False, ["SYNTHETICVALUE"], {"data": "SYNTHETICVALUE"}):
            text = json.dumps({"PlatformInfo": {"Generic": {key: value}}})
            with self.subTest(nonempty_type=type(value).__name__):
                self.assertIn("identifier assignment", module.inspect_blob(name, text.encode()))

    def test_json_identity_checks_include_escaped_and_duplicate_keys(self):
        key = "SystemSerial" + "Number"
        text = json.dumps({key: "SYNTHETICVALUE"}).replace("Number", r"\u004eumber")
        self.assertIn("identifier assignment", module.inspect_blob("config.json", text.encode()))
        text = '{"' + key + '":"SYNTHETICVALUE","' + key + '":""}'
        self.assertIn("identifier assignment", module.inspect_blob("config.json", text.encode()))

    def test_json_notes_and_escaped_secrets_are_still_checked(self):
        text = json.dumps({"notes": "MLB" + "=SYNTHETICVALUE"})
        self.assertIn("identifier assignment", module.inspect_blob("report.json", text.encode()))
        token = "gh" + "p_" + "x" * 24
        text = json.dumps({"note": token}).replace("gh", r"\u0067h")
        self.assertIn("GitHub token", module.inspect_blob("report.json", text.encode()))

    def test_tokens_and_private_key_headers_remain_blocked(self):
        cases = [
            ("GitHub token", "gh" + "p_" + "x" * 24),
            ("private key", "-----BEGIN " + "PRIVATE KEY-----"),
            ("Windows product key", "-".join(["A1B2C"] * 5)),
        ]
        for label, value in cases:
            with self.subTest(label=label):
                self.assertIn(label, module.inspect_blob("notes.md", value.encode()))

    def test_invalid_json_is_blocked(self):
        self.assertIn("invalid JSON", module.inspect_blob("config.json", b'{"MLB":'))

    def test_raw_files_are_blocked_even_without_secrets(self):
        for name in ["EFI/OC/config.plist", "dump.aml", "raw/report.txt", "photo.jpeg", "history/EFI/config.sanitized.json", "history/backup.tar.gz", "report.log"]:
            with self.subTest(name=name):
                self.assertTrue(module.inspect_blob(name, b"public words"))

    def test_binary_is_blocked(self):
        self.assertTrue(module.inspect_blob("notes.md", b"\xff\x00"))
        self.assertIn("binary content", module.inspect_blob("observer.cpp", b"public\x00text"))

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

