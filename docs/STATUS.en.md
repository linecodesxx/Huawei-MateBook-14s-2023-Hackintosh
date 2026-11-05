# Current status

[Русский](STATUS.md) | **English**

**November 5, 2026 · Huawei MateBook 14s 2023 · Sequoia 15.8 [24H23]**

| Check | Result |
|---|---|
| Graphical Recovery / Disk Utility | Confirmed on the laptop |
| Built-in keyboard | Works, confirmed by the user |
| Synaptics S9801 | Works with polling; gestures not separately tested |
| Working `cpus=1` baseline | Preserved locally and byte-verified |
| All 20 logical CPUs | Only `cpus=1` removed on USB; new hardware boot result pending |
| GPU/Metal and network | Untested |
| Audio, Fn/brightness, battery, sleep, camera, touchscreen | Untested |
| Installation / installed macOS | Not performed / untested |

The repair uses a named Darwin-only `EC` while preserving `HWEC`, native UUID waiting, a PS/2 keyboard and an I2C touchpad. The temporary UUID bypass is disabled; no custom Kernel/Patch entry is enabled. A graphical interface does not establish hardware acceleration.

The current USB configuration passed checks, all 117 files were verified, and the USB was unmounted. No automatic reboot occurred. Earlier logical=20/20 counters do not replace testing Recovery after the latest change; the old physical=20 field does not mean 20 physical cores.

[Research digest](../devlog/2026-11-05-recovery-and-input.en.md) · [essential settings](recovery-settings.json) · [roadmap](../ROADMAP.en.md). The full archive and boot EFI remain local.
