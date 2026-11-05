# Next steps

[Русский](ROADMAP.md) | **English**

**November 5, 2026.** [Milestone result](devlog/2026-11-05-recovery-and-input.en.md) · [status](docs/STATUS.en.md).

- [x] Identify hardware and compare OEM ACPI with D16/X1/XPS references.
- [x] Localize TypeCBPC/EC → matching → UUID/USB waits.
- [x] Reach Recovery 15.8 [24H23] with built-in keyboard/touchpad working.
- [x] Preserve the working single-CPU EFI locally.
- [x] Remove only `cpus=1` on USB for the next all-20-thread test.
- [ ] Confirm Recovery, built-in input and all 20 logical CPUs in the new boot.
- [ ] Check repeatable cold boots and restart.
- [ ] Test gestures, Fn, touchscreen, USB ports, network, audio, battery and brightness.
- [ ] Confirm GPU/Metal, then sleep and external displays.
- [ ] With separate authorization, test installation and installed macOS.
- [ ] Prepare an EFI release after sufficient hardware tests.

The publication contains concise documentation, [essential settings](docs/recovery-settings.json) and original ACPI sources. The full archive remains local. The new 20-thread test is unconfirmed; no automatic reboot occurred.
