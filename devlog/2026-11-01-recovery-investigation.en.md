# 2026-11-01 — Recovery testing and diagnostic data

[Русский](2026-11-01-recovery-investigation.md) | **English**

## Observations

- macOS Tahoe Recovery started the kernel, but the Recovery GUI did not appear. The last visible lines varied between `CoreAnalyticsHub start completed` and `pci (build ...)`.
- For comparison, an original macOS Sequoia **15.4.1, build 24E263** Recovery was prepared and verified against its chunklist. Sequoia also reached early kernel and ACPI output, but the Recovery GUI did not appear.
- The ACPI table load message was accompanied by `Unsupported module-level executable opcode 0x70` warnings. Some reported offsets match bytes in OEM SSDT13, but that does not establish the source of every warning or the cause of the stall.
- Linux reports ACPI `AE_ALREADY_EXISTS` for `TPL1` methods and a separate `AE_NOT_FOUND` in a Wi-Fi method; Linux works. A causal link to macOS has not been established.

## Checks

| Change / check | Result and limitation |
|---|---|
| CPUID emulation in the new EFI | A subsequent attempt passed `EXITBS` and reached the kernel. The effect of a particular spoofed field is not proven: attempts were not strictly identical. |
| A virtual EC without disabling HWEC | No visible progress was observed. |
| `cpus=1`, `npci=0x2000`, `CpuTscSync` | Individual checks did not produce an observed Recovery boot with the configurations tested; interactions remain possible. |
| Disable USBToolBox and UTBDefault; change `ReleaseUsbOwnership` | No observed Recovery boot. Access to the boot medium at the kernel stage remains unverified. |
| Diagnostic WhateverXe fork | No visible progress; Metal and acceleration were not tested. |
| `io=0x16`; allow panic on power timeout | No additional cause was obtained from the screen. |
| Whitelist runtime MMIO `0xF9D00000` | DEBUG log confirmed `skip 1`; no visible progress. This does not establish whether a particular firmware function needs this range. |
| Temporarily exclude OEM SSDT13 by signature, OEM Table ID and length | No visible progress was reported. No application log was captured, so whether the exclusion took effect is unconfirmed. The exclusion was disabled afterwards. |

The DEBUG OpenCore log showed three runtime MMIO descriptors. The previous `0xF9000000` entry did not fall within the observed `0xF9D00000–0xF9EFFFFF` descriptor. A descriptor's presence does not prove it belongs in the whitelist. A separate `0xFF000000` test was later prepared, but no confirmed boot result was recorded for it.

## Current state and next step

A working EFI, Recovery GUI and graphics acceleration are **not confirmed**. The SSDT13 exclusion is disabled in the last checked config; Tahoe Recovery 26.6.2 is on the test USB and the previously used Sequoia 15.4.1 is saved separately. ACPI changes can also affect other OSes booted through OpenCore: Using the firmware boot menu for Windows and Linux is recommended while an experiment is enabled.

The next task is to obtain information about execution **after the last visible kernel line**, or design a test with an expected result defined beforehand. The last line on screen does not identify the failing component. `ocvalidate` checks configuration structure, not hardware compatibility. A public EFI release is not ready.

## Update: graphics and USB

- The Tahoe Recovery version was identified from `SystemVersion.plist` as **26.6.2, 25G83**.
- Experimental WhateverXe 0.6.1 was tested for GPU `8086:a7a0` after disabling WhateverGreen and removing `-igfxvesa`; Recovery still stalled. The log confirms the boot arguments but does not show whether the kext loaded. This does not identify the cause: Tahoe 26.6.2 is outside the stated WhateverXe versions, and the separate graphics package was not installed.
- `UTBDefault.kext` is a generic pre-mapping configuration, not a port map for this laptop. Linux sees the boot USB at `00:14.0` over SuperSpeed; access to that port at the macOS kernel stage is unconfirmed.
- We decided to try **Sequoia 15.8**, which is listed among the compatible WhateverXe versions. A successful Recovery boot and graphics acceleration remain unconfirmed.
- Raptor Lake-H/P/U is in the [WhateverXe device list](https://github.com/b00t0x/WhateverXe/blob/main/docs/device-selection.md), but support is not validated on this laptop and internal display support is experimental.
