#!/usr/bin/env python3
"""Check Git index contents for common identifiers; never print matched values."""
from __future__ import annotations
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

BLOCKED_SUFFIXES = (
    ".plist", ".aml", ".bin", ".rom", ".dmp", ".log", ".ioreg",
    ".tar", ".tar.gz", ".zip", ".7z", ".png", ".jpg", ".jpeg",
    ".webp", ".heic", ".mp4", ".pem", ".key", ".p12", ".pfx",
)
BLOCKED_PARTS = {"private", "raw", "downloads", "efi", "sysreport"}
# Shared protocol/type constants, never device, volume or attachment identities.
# Sources and purposes are documented in PRIVACY.md / PRIVACY.en.md.
PUBLIC_GUIDS = {
    "7C436110-AB2A-4BBB-A880-FE41995C9F82",  # Apple boot NVRAM namespace.
    "4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14",  # Apple vendor NVRAM namespace.
    "4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102",  # OpenCore vendor NVRAM namespace.
    "8BE4DF61-93CA-11D2-AA0D-00E098032B8C",  # UEFI global-variable namespace.
    "3CDFF6F7-4267-4555-AD05-B30A3D8938DE",  # HID-over-I2C ACPI _DSM interface.
    "4C616265-6C00-11AA-AA11-00306543ECAC",  # Apple Label partition type.
    "0516B563-B15B-11DA-96EB-0014519758EF",  # AppleMultitouch IOCFPlugInTypes interface.
    "00000000-0000-0000-0000-000000000000",  # Nil UUID: absence of an identifier.
}
PATTERNS = {
    "UUID": re.compile(r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"),
    "MAC address": re.compile(r"(?i)(?<![0-9a-f])(?:[0-9a-f]{2}[:-]){5}[0-9a-f]{2}(?![0-9a-f])"),
    "IPv4 address": re.compile(r"(?<![\w.])(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?![\w.])"),
    "email address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "personal home path": re.compile(r"(?:/home/|/Users/)[A-Za-z0-9_.-]+"),
    "Windows product key": re.compile(r"(?i)\b[A-Z0-9]{5}(?:-[A-Z0-9]{5}){4}\b"),
    "GitHub token": re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    "private key": re.compile(r"-----BEGIN (?:[A-Z0-9]+ )?PRIVATE KEY-----"),
    "SSH public key identifier": re.compile(r"\bssh-(?:ed25519|rsa)\s+[A-Za-z0-9+/]{30,}"),
}
IDENTIFIER_FIELDS = {
    "SystemSerialNumber", "SystemUUID", "MLB", "ROM", "SerialNumber",
    "SSID", "BSSID", "IOPlatformSerialNumber", "IOPlatformUUID",
    "HardwareUUID", "BoardSerialNumber", "ChassisSerialNumber",
}
_IDENTIFIER_NAMES = "|".join(sorted(IDENTIFIER_FIELDS))
IDENTIFIER_ASSIGNMENT = re.compile(
    r'(?im)\b(?:' + _IDENTIFIER_NAMES + r')\b["\x27]?\s*[:=]\s*'
    r'(?:"(?P<double>(?:\\.|[^"\\])*)"|'
    r"'(?P<single>(?:\\.|[^'\\])*)'|"
    r'(?P<bare>[^\s"\x27,;<>]+))'
)
PLACEHOLDERS = {"redacted", "removed", "placeholder", "none", "null", "empty", "-", "xxx"}

def inspect_json(text: str) -> tuple[bool, set[str]]:
    """Inspect parsed values, including escapes and duplicate assignments."""
    found = False
    fields = {name.casefold() for name in IDENTIFIER_FIELDS}
    strings = set()

    def collect_strings(value: object) -> None:
        if isinstance(value, str):
            strings.add(value)
        elif isinstance(value, dict):
            for key, item in value.items():
                collect_strings(key)
                collect_strings(item)
        elif isinstance(value, list):
            for item in value:
                collect_strings(item)

    def inspect_object(pairs: list[tuple[str, object]]) -> dict:
        nonlocal found
        for key, value in pairs:
            if key.casefold() in fields and value not in ("", None, [], {}):
                found = True
            collect_strings(key)
            collect_strings(value)
        return dict(pairs)

    collect_strings(json.loads(text, object_pairs_hook=inspect_object))
    return found, strings

def inspect_blob(name: str, data: bytes) -> list[str]:
    path = PurePosixPath(name)
    problems = []
    if (name.lower().endswith(BLOCKED_SUFFIXES)
            or any(p.lower() in BLOCKED_PARTS for p in path.parts)
            or path.name.startswith(".env")):
        problems.append("blocked raw/private file type or location")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return problems + ["non-UTF-8/binary file"]
    if "\x00" in text:
        problems.append("binary content")
    scan_texts = [text]
    assignment_texts = [text]
    if path.suffix.lower() == ".json":
        try:
            has_identifier, decoded_strings = inspect_json(text)
            if has_identifier:
                problems.append("identifier assignment")
            scan_texts.extend(decoded_strings)
            assignment_texts = decoded_strings
        except (ValueError, RecursionError):
            problems.append("invalid JSON")
    for label, pattern in PATTERNS.items():
        if any(label != "UUID" or match.group().upper() not in PUBLIC_GUIDS
               for item in scan_texts for match in pattern.finditer(item)):
            problems.append(label)
    if "identifier assignment" not in problems:
        for item in assignment_texts:
            for match in IDENTIFIER_ASSIGNMENT.finditer(item):
                value = next(group for group in match.groups() if group is not None)
                if value and value.lower() not in PLACEHOLDERS:
                    problems.append("identifier assignment")
                    break
            if "identifier assignment" in problems:
                break
    return problems

def indexed_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "-z"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return [p.decode("utf-8") for p in result.stdout.split(b"\0") if p]

def main() -> int:
    try:
        names = indexed_files()
        failures = []
        for name in names:
            result = subprocess.run(
                ["git", "show", ":" + name],
                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
            problems = inspect_blob(name, result.stdout)
            if problems:
                failures.append((name, problems))
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        print("FAIL: cannot safely inspect the Git index.", file=sys.stderr)
        return 2
    for name, problems in failures:
        print("FAIL: " + name + ": " + ", ".join(problems), file=sys.stderr)
    if failures:
        print("Matched values were not printed. Review locally before publishing.", file=sys.stderr)
        return 1
    print("PASS: checked " + str(len(names)) + " indexed UTF-8 files.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

