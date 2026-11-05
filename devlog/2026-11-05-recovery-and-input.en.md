# 2026-11-05 — Recovery and built-in input: digest

[Русский](2026-11-05-recovery-and-input.md) | **English**

**Confirmed:** the Huawei MateBook 14s 2023 reached **macOS Sequoia Recovery 15.8 [24H23] Disk Utility**. The user confirmed its built-in keyboard and touchpad work. The working `cpus=1` EFI is preserved locally. That limit was subsequently removed on USB; the new 20-thread boot remains unconfirmed.

## What unsuccessful tests established

CPU/CPUID, CpuTscSync, MMIO, SSDT13/TPL1, USBToolBox, SetupVirtualMap, ExtraMsrs, DebugEnhancer and graphics variants were tested. Individual changes did not reach Recovery in those configurations; interactions remain possible. A single-CPU repeat did not advance the earlier stall. The final PCI/NVMe line did not identify the cause, and `ocvalidate` checked configuration rather than hardware compatibility.

The full chronology, raw logs and negative results remain local. This digest retains the causal chain, essential changes and evidence limits. November 1 entries are historical snapshots.

## Cause: literal EC versus HWEC

BSDSnapshot first confirmed a bootstrap UUID wait. A narrow temporary bypass reached BSD, then exposed `IOResources::waitQuiet` before Recovery root-image submission. No quiet-wait bypass was added.

Version 0.4.0 captured three IOConfig workers: one waited in `TypeCBPC::probe` for an ACPI device literally named `EC`; two waited for `AppleUSBHostResources`. Firmware exposed the enabled real controller as `HWEC` with `PNP0C09`. Exact Recovery kernel-collection inspection showed that the blocked probe held up IOResources matching, delaying UUID/USB readiness and root-image preparation.

Darwin-only [SSDT-EC-HUAWEI](../patches/SSDT-EC-HUAWEI.dsl) supplied a named EC without ports or Apple methods, preserving real HWEC. The temporary UUID bypass was disabled and native waiting restored. The next boot reached graphical input setup. No custom Kernel/Patch is enabled in the successful baseline.

Earlier interpretations were corrected: a UUID property did not prove matching completion; startup DONE did not establish completion of all memory protection; no busy descendants did not exclude the resource's own matching job.

## Built-in devices

The PS/2 keyboard uses VoodooPS2Controller/Keyboard from official [release 2.3.7](https://github.com/acidanthera/VoodooPS2/releases/tag/2.3.7). Synaptics S9801 is on I2C0 `8086:51e8`, address `0x15`, 400 kHz, HID descriptor `0x20`.

[SSDT-HW-INPUT](../patches/SSDT-HW-INPUT.dsl) adds Darwin-only TPDX under I2C0 while preserving OEM TPD0 initialization. An exact DSDT-only `_PS3` rename and Darwin wrapper prevent the D3hot transition from clearing BAR0. No global OSI override or GPIO writes were added.

VoodooI2C main was built from unchanged upstream commit [`6be653a2d2234ac1f7464ebf12716314975c3920`](https://github.com/VoodooI2C/VoodooI2C/tree/6be653a2d2234ac1f7464ebf12716314975c3920), containing the needed `51e8`/timing support; its personality was narrowed to the actual ID. Services/GPIO/HID came from official package 2.9.1, with one VoodooInput 1.1.6 copy. Dependency compatibility and imports were checked separately; the selection is not claimed as one official release. Polling uses `-vi2c-force-polling`; gestures and interrupts remain untested.

Disk Utility then opened and the user confirmed both devices. EFI backups preceded changes; the successful 117-file EFI was separately preserved and byte-verified.

## Next boot

At the user's request, **only `cpus=1` was removed**. [CPU20 ACPI](../patches/SSDT-CPU20-ALT.dsl), input, CPUID and other settings remain unchanged. The USB passed `ocvalidate` and verification of all 117 files, then was unmounted. No automatic reboot occurred. **All 20 logical CPUs are enabled in configuration; successful Recovery after this change remains unobserved.** The single-CPU baseline remains available for rollback.

On SMP, BSDSnapshot skips saved stacks with `status=-2`; their lifetime protection requires one CPU. Resource snapshots remain non-atomic. Earlier logical=20/20 counters do not replace this test; physical=20 did not mean 20 physical cores.

[Essential settings, versions and checksums](../docs/recovery-settings.json) accompany the original text ACPI patches. Full archives, EFI, binary dependencies and photos stay local. GPU/Metal, network, sleep and installed macOS remain untested; no formatting or installation was performed.
