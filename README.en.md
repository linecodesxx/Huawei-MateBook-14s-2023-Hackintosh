# Huawei MateBook 14s 2023 — Hackintosh research log

[Русский](README.md) | **English**

**i7-13700H · Intel Iris Xe A7A0 · OpenCore · work in progress**

An experimental, public research journal for bringing macOS to the Huawei MateBook 14s 2023 (HKFG-XX). Hardware notes, a D16-based porting plan and reproducible boot experiments. **No working EFI release or graphics acceleration on this machine has been demonstrated.**

## About this project

This project investigates booting macOS on a MateBook 14s 2023 with an Intel Core i7-13700H. It records verified observations, adaptation plans, individual boot results and unsuccessful attempts.

The goal is to progress from kernel startup to the installer, then test Metal, peripherals and stability. An EFI will only be described as working after it has been tested on this laptop.

**Last updated: November 1, 2026.**

## Current status

| Stage | Status | Evidence |
|---|---|---|
| OpenCore hands control to macOS | Observed | Kernel messages are visible in the latest boot photo |
| Kernel starts early services | Observed | AppleKeyStore, CoreAnalyticsHub |
| ACPI table loading | Success reported | Warnings are followed by ACPI AML tables successfully acquired and loaded |
| Further boot progress | Output stops; cause unknown | Last visible line: pci (build ...), flags ... |
| Installer / desktop | Unconfirmed | No successful boot has been recorded |
| Metal on this 14s | Untested | Results from other laptops are not results for this project |
| Audio, touchpad, brightness, sleep | Untested in macOS | Early boot must be resolved first |

The latest attempt has already passed EXITBS. The PCI banner alone does not prove a PCI problem; the last log line does not necessarily identify the cause.

## Why use the D16 as a donor?

The Huawei MateBook D16 2024 uses the same SN6140 audio codec. The EC/keyboard paths and Fn method assignments confirmed in our 14s DSDT also match the D16 approach. However, the GPU, display panel and touchpad differ.

The D16 configuration builds on the X1 Carbon Gen 11 project. In the snapshots examined, its Booter settings, CPUID configuration and main Kernel Quirks match the archived 14s configuration. Simply replacing the configuration is therefore not an established fix for the current stall.

## Documentation

Russian is the primary documentation language. Every document and template has an English version; use the language links at the top to switch.

- [Hardware](docs/HARDWARE.en.md)
- [Facts, hypotheses and unknowns](docs/STATUS.en.md)
- [Porting plan](docs/PORTING.en.md)
- [Roadmap](ROADMAP.en.md)
- [First devlog: what we know so far](devlog/2026-11-01-start.en.md)
- [Boot experiment template](experiments/TEMPLATE.en.md)
- [References and acknowledgements](docs/REFERENCES.en.md)
- [Publication rules and identifier protection](PRIVACY.en.md)
- [How to maintain the journal](CONTRIBUTING.en.md)

- [Devlog index](devlog/README.en.md)
- [Issue templates](.github/ISSUE_TEMPLATE/)

## Published materials and privacy

The initial publication contains documentation and a publication checker. Original EFI configurations, PlatformInfo/SMBIOS data, firmware dumps, hardware reports, screen photos and raw logs are excluded.

Before each commit:

```sh
python3 scripts/check_publication.py
python3 -m unittest discover -s tests -v
```

To enable the local pre-commit hook:

```sh
git config core.hooksPath .githooks
```

The checker reduces the risk of leaks but does not replace reviewing the diff and history. It does not scan issue attachments, external links or photo metadata. Web and API edits bypass the local hook and require separate review.

## Contributing

Reproducible reports for the HKFG-XX/i7-13700H, ACPI analysis and hardware comparisons are welcome. Remove unique identifiers before publishing. Do not attach complete dumps or configurations.

This repository is not affiliated with Apple, Huawei or Intel. The initial publication includes no third-party code or binary drivers; their rights remain with their respective authors.
