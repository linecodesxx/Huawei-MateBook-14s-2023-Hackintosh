# Huawei MateBook 14s 2023 — Hackintosh

[Русский](README.md) | **English**

**i7-13700H · Iris Xe A7A0 · OpenCore · updated November 5, 2026**

The Huawei MateBook 14s 2023 (HKFG-XX) reached **macOS Sequoia Recovery 15.8 [24H23] Disk Utility**. The user confirmed its built-in keyboard and touchpad work. The working EFI is preserved locally; no ready-to-boot EFI release is provided here yet.

| Feature | Status |
|---|---|
| Recovery and Disk Utility | Working |
| Built-in keyboard and touchpad | Working; touchpad uses polling |
| All 20 logical CPUs | Enabled in the USB configuration; new boot unconfirmed |
| GPU/Metal, network, installed macOS | Untested |

The observer localized a blocked `TypeCBPC::probe`: firmware exposed `HWEC`, while the driver waited for literal `EC`. A named Darwin-only EC addressed this barrier, and the temporary UUID-wait bypass was disabled. PS/2 keyboard and I2C touchpad support followed. After success, only `cpus=1` was removed for the next 20-thread test. The working single-CPU baseline is preserved; the USB was verified and unmounted without automatically rebooting the laptop.

## Essential materials

- [Concise result and negative-test summary](devlog/2026-11-05-recovery-and-input.en.md)
- [Current status](docs/STATUS.en.md) and [next steps](ROADMAP.en.md)
- [Essential settings, versions and checksums](docs/recovery-settings.json)
- ACPI: [CPU20](patches/SSDT-CPU20-ALT.dsl), [named EC](patches/SSDT-EC-HUAWEI.dsl), [built-in input](patches/SSDT-HW-INPUT.dsl)
- [Hardware](docs/HARDWARE.en.md), [references](docs/REFERENCES.en.md), [historical devlog](devlog/README.en.md)
- [Privacy](PRIVACY.en.md) and [contributing](CONTRIBUTING.en.md)

Publication contains a research digest and original text patches. The full archive, native EFI, binary drivers, private configurations, raw logs and photos remain local. No formatting or installation was performed. Other models' results do not establish support for this laptop.

Before committing:

```sh
python3 scripts/check_publication.py
python3 -m unittest discover -s tests -v
```

This repository is not affiliated with Apple, Huawei or Intel.
