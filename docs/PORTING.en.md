# Porting plan: D16 → MateBook 14s 2023

[Русский](PORTING.md) | **English**

## Decision

Build an EFI for this laptop using the D16 Huawei layer and a consistent X1/NootedGreen base. Do not copy the entire donor configuration.

Start with the installer without acceleration, then address the graphics stack, peripherals and stability.

## Porting matrix

| Component | Match / difference | Action |
|---|---|---|
| Fn keys | EC/PS2K paths and _Q0A/_Q0B/_Q0D/_Q0E/_Q0F assignments match | SSDT-HWFN is a candidate; verify renames and actual behavior |
| Backlight | GFX0 path and the PNLF field conflict have the same structure | Place a PNLF device under the GPU; measure this panel's PWM/brightness limit |
| Audio | Same SN6140 14F1:1F87 | Compare pins, then use AppleALC/SimpleHDA/XE-HPFIX from a consistent version |
| Touchpad | D16 uses BLTP7840; this laptop uses S9801 | Adapt HID, address, descriptor register, power and IRQ |
| GPU | D16 has A7A8/48 EU; this laptop has A7A0/96 EU | Do not copy the D16 48 EU/6 L3 profile or frequencies |
| Graphics memory | A 14s-specific GMS issue has not yet been confirmed | Check GGC/GMS before concluding that XE-GMS4 is needed |
| USB | Different motherboard model | Create a port map for this laptop |
| HDMI | The D16 experimental mode hangs with a monitor connected | Defer until the internal panel is stable |
| MMIO/Booter | Examined snapshots match X1/the current EFI | Justify settings using this laptop's memory map |
| Sleep | Unconfirmed on the 14s | Test separately at a later stage |

## Reproducible base

The D16 patch targets dssoftx commit:

`c4cc862a8959741f360044a60a6022508a983511`

SHA256 of the examined patches/nootedgreen-huawei.diff:

`a93efbb93352e3f50c6a0bc9493407f6faae0bf56bcbee4edfe8281b93dcfb77`

The D16 repository contains a configuration, individual SSDTs, a patch and tools, rather than a complete ready-to-use EFI folder with all dependencies. Its documentation ties the stack to Tahoe 26.7.1 (25G241); the actual target system version still needs to be established.

## Sequence

1. Compare newer local changes and results, preserving the stage already reached.
2. Prepare a separate USB test build without changing the main disk's bootloaders or partition layout.
3. Prepare ACPI using this laptop's OEM AML.
4. Validate the configuration structure and paths.
5. Run one boot experiment that distinguishes between hypotheses and record the observation.
6. Once boot is reproducible, build and install a consistent NootedGreen/TGL stack.
7. Add audio, input, Fn and brightness support incrementally.
8. Test restart, load, sleep and external display outputs separately.

## Boundaries

- A successful build does not establish a successful boot.
- Metal working on an XPS does not establish that it works on the 14s.
- Do not arbitrarily mix WhateverXe with the chosen NootedGreen stack.
- Do not copy CPUFriendDataProvider, the USB map or panel constants from the older Tiger Lake 14s.
- Unresolved external methods in DSL are a reason to use OEM AML as source material, rather than replace the entire DSDT.
- If further progress requires an unknown kernel driver fix, assess the cost of that research separately.
