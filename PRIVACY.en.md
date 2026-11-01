# Publishing without unique identifiers

[Русский](PRIVACY.md) | **English**

## What may be published

Laptop/motherboard and CPU models, standard PCI/USB IDs, anonymized ACPI paths, verified conclusions, links to public projects and our own minimal patches after review.

## What stays local

- Actual SystemSerialNumber, MLB, ROM, SystemUUID and other PlatformInfo identifiers.
- Serial numbers of the laptop, motherboard, drives and USB devices.
- MAC addresses, Bluetooth addresses, SSIDs and IP addresses.
- Personal usernames, home directory paths and personal email addresses.
- Windows OEM keys and the MSDM table.
- Tokens, passwords, private keys and VPN configurations.
- Complete EFI folders, NVRAM/IORegistry/SysReport data and memory/firmware dumps.
- Raw hardware reports and screenshots.

## Before committing

1. Stage only specific reviewed files; do not copy an entire diagnostics directory.
2. Review the staged diff and file list.
3. Run python3 scripts/check_publication.py.
4. Ensure commit messages and author metadata use public information; a GitHub noreply address is suitable for the author email.
5. Review previous history before the first push.

The checker reads staged/index contents rather than only the current files on disk. Otherwise, a secret left in staging could be missed after editing the working copy.

.gitignore does not remove already tracked files or clean history. The checker is a precaution, not a guarantee that all personal data is absent. It does not check images, EXIF, issue attachments or files behind external links. The initial publication therefore contains only text and our own checking tool.

## Public configurations in the future

Only publish a separately reviewed copy with empty identifiers and mandatory manual review. Do not upload the working config.plist directly. Supporting that format will require an intentional change to the publication rules.

If a leak occurs, removing the line in a subsequent commit is insufficient: account for history, accessible copies and rotation of exposed secrets.
