# Publishing without unique identifiers

[Русский](PRIVACY.md) | **English**

## What may be published

Laptop/motherboard and CPU models, standard PCI/USB IDs, anonymized ACPI paths, verified conclusions, links to public projects and our own minimal patches after review.

The repository retains the reviewed [results summary](devlog/2026-11-05-recovery-and-input.en.md), [essential settings](docs/recovery-settings.json) and our own ACPI patch DSL sources. The complete experiment archive and historical configurations stay local. Passing the publication check does not establish a successful boot or suitability for another device.

## What stays local

- Actual SystemSerialNumber, MLB, ROM, SystemUUID and other PlatformInfo identifiers.
- Serial numbers of the laptop, motherboard, drives and USB devices.
- MAC addresses, Bluetooth addresses, SSIDs and IP addresses.
- Personal usernames, home directory paths and personal email addresses.
- Windows OEM keys and the MSDM table.
- Tokens, passwords, private keys and VPN configurations.
- Complete EFI folders and their archives, original NVRAM/IORegistry/SysReport data and memory/firmware dumps.
- Raw hardware reports, complete native DSDT/ACPI tables, binaries, photographs and screenshots.

## Before committing

1. Stage only specific reviewed files; do not copy an entire diagnostics directory.
2. Review the staged diff and file list.
3. Run python3 scripts/check_publication.py.
4. Ensure commit messages and author metadata use public information; a GitHub noreply address is suitable for the author email.
5. Review previous history before the first push.

The checker reads staged/index contents rather than only the current files on disk. Otherwise, a secret left in staging could be missed after editing the working copy.

.gitignore does not remove already tracked files or clean history. The checker is a precaution, not a guarantee that all personal data is absent. It blocks original private formats and binaries, but does not inspect EXIF, issue attachments or files behind external links. Published materials therefore remain textual and require manual review.

## Sanitized JSON configurations

Publish only a reviewed, concise JSON settings summary with unique identifiers emptied. For identity fields in JSON, the checker allows only an empty string, null, empty array or empty object; a nonempty placeholder is also rejected. Remove identifiers from nested structures, text comments and encoded forms as well. Keep the original config.plist and complete historical copies local; renaming a file does not sanitize it. Original plist, AML, logs, EFI directories, archives and images remain blocked.

## Shared protocol and type GUIDs

Exceptions are limited to these shared constants; device, volume and attachment UUIDs are excluded:

- 7C436110-AB2A-4BBB-A880-FE41995C9F82 — Apple boot NVRAM namespace.
- 4D1EDE05-38C7-4A6A-9CC6-4BCCA8B38C14 — Apple vendor NVRAM namespace.
- 4D1FDA02-38C7-4A6A-9CC6-4BCCA8B30102 — OpenCore vendor NVRAM namespace.
- 8BE4DF61-93CA-11D2-AA0D-00E098032B8C — UEFI global-variable namespace.
- 3CDFF6F7-4267-4555-AD05-B30A3D8938DE — HID-over-I2C ACPI _DSM interface.
- 4C616265-6C00-11AA-AA11-00306543ECAC — Apple Label partition type.
- 0516B563-B15B-11DA-96EB-0014519758EF — AppleMultitouch IOCFPlugInTypes interface.
- 00000000-0000-0000-0000-000000000000 — Nil UUID denoting absence; this does not permit a nonempty JSON identity field.

Purposes are established by the [OpenCore Reference Manual, §9.1](https://raw.githubusercontent.com/acidanthera/OpenCorePkg/master/Docs/Configuration.pdf), [Microsoft HID-over-I2C documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/bringup/hidi2c-device-specific-method---dsm-), [Apple IOStorageFamily](https://github.com/apple-oss-distributions/IOStorageFamily/blob/main/Info.plist), [VoodooI2C metadata](https://github.com/VoodooI2C/VoodooI2C/blob/6be653a2d2234ac1f7464ebf12716314975c3920/VoodooI2C/VoodooI2C/Info.plist) and [RFC 9562, §5.9](https://www.rfc-editor.org/rfc/rfc9562.html#name-nil-uuid). Any new exception requires a primary-source check and a test; UUID syntax alone grants no exception.

If a leak occurs, removing the line in a subsequent commit is insufficient: account for history, accessible copies and rotation of exposed secrets.
