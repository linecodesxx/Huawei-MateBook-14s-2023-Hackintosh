# Roadmap

[Русский](ROADMAP.md) | **English**

Only mark confirmed results as complete.

## Completed

- [x] Identified the HKFG-XX/i7-13700H/A7A0 hardware.
- [x] Located and examined OEM ACPI and the archived EFI.
- [x] Selected D16 as the main donor for Huawei patches.
- [x] Compared Fn/EC/PS2K/GFX0 paths and touchpad parameters.
- [x] Compared archived configurations.
- [x] Checked that the D16 patch applies to the selected X1 sources.

## Stage 1 — reproducible early boot

- [ ] Record the current local configuration and latest Codex results.
- [ ] Establish the target macOS version.
- [ ] Check MADT/APIC and the UEFI memory map.
- [ ] Prepare ACPI for this laptop, justifying each change.
- [ ] Localize the stall after ACPI loading.
- [ ] Achieve reproducible installer/system boot without acceleration.

## Stage 2 — internal display and Metal

- [ ] Measure the GPU resource profile, GMS and eDP parameters.
- [ ] Build a consistent NootedGreen version with the D16 layer.
- [ ] Confirm Metal on this laptop.
- [ ] Test sustained load, restart and boot repeatability.

## Stage 3 — peripherals

- [ ] Keyboard and Fn keys.
- [ ] Synaptics S9801 and touchscreen.
- [ ] SN6140 audio: speakers, headphones and microphones.
- [ ] Wi-Fi/Bluetooth.
- [ ] USB and camera.
- [ ] Brightness and battery.

## Stage 4 — separate complex tasks

- [ ] Sleep and wake.
- [ ] HDMI and USB-C display output.
- [ ] Publish tested adaptation sources.
- [ ] Prepare a sanitized EFI release only after hardware confirmation.
