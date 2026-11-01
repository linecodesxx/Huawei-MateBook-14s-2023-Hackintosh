# Status: facts and hypotheses

[Русский](STATUS.md) | **English**

Snapshot as of November 1, 2026. Later tests and their limitations are documented in the [Recovery investigation](../devlog/2026-11-01-recovery-investigation.en.md).

## Observed on this laptop

- The macOS kernel prints AppleKeyStore/CoreAnalyticsHub messages.
- A list of ACPI tables is printed.
- Warnings report Unsupported module-level executable opcode 0x70.
- A subsequent message reports successful loading of the ACPI AML tables.
- The last visible line is pci (build ...), flags ...
- No explicit kernel panic or stack trace is visible in the latest photo.

The installer, desktop and Metal have not been confirmed on this laptop. Output stopping does not prove that the system has completely stopped executing.

## Static checks completed

- The files referenced by all enabled ACPI/UEFI/Kernel entries in the archived EFI were found.
- GPU properties were removed from the archived configuration; Wi-Fi/PS2 were disabled; VESA and safe mode were added.
- Booter/Kernel settings match the corresponding sections of the examined D16 configuration.
- Both SSDTs in the archived EFI match the X1 files byte for byte.
- The D16 NootedGreen patch matched the current public version at the time of checking.
- git apply --check passed against the sources from the X1 archive. Only file permission warnings caused by archive extraction were reported.

These are not hardware test results. A saved config.before-* variant also does not establish that it was booted or what its result was.

## Working hypotheses

1. The stall is related to early platform/device initialization through ACPI/IOKit.
2. Firmware settings carried over from another model need verification on this Huawei.
3. Further screen output may have been lost.

No particular ACPI method, PCI component, CPU topology issue or iGPU fault has been established as the cause. The 0x70 warnings cannot automatically be classified as either the cause of the hang or entirely harmless.

## Unresolved questions

- Exact version of the original Tahoe Recovery; Sequoia Recovery 15.4.1 (24E263) was also used for comparison.
- Whether the SSDT13 exclusion took effect during the test: no application log was captured. It is disabled in the last checked config.
- How to obtain the next diagnostically useful result.
- Hardware compatibility of the chosen graphics stack with the 14s panel.
