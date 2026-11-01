#!/usr/bin/env python3
"""Check Git index contents for common identifiers; never print matched values."""
from __future__ import annotations
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
IDENTIFIER_ASSIGNMENT = re.compile(
    r'(?im)\b(?:SystemSerialNumber|SystemUUID|MLB|ROM|SerialNumber|'
    r'SSID|BSSID|IOPlatformSerialNumber)\b["\x27]?\s*[:=]\s*'
    r'["\x27]?([^\s"\x27,;<>]+)'
)
PLACEHOLDERS = {"redacted", "removed", "placeholder", "none", "null", "empty", "-", "xxx"}

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
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            problems.append(label)
    for match in IDENTIFIER_ASSIGNMENT.finditer(text):
        if match.group(1).lower() not in PLACEHOLDERS:
            problems.append("identifier assignment")
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

