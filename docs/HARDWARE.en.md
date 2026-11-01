# Hardware

[Русский](HARDWARE.md) | **English**

Sources: the owner's local hardware report and analysis of OEM ACPI. Only model specifications and standard device identifiers are included here.

| Component | Confirmed information |
|---|---|
| Laptop / motherboard | Huawei MateBook 14s 2023, HKFG-XX / HKFG-XX-PCB |
| CPU | Intel Core i7-13700H; 6P + 8E; 14 cores / 20 threads |
| iGPU | Intel Iris Xe, PCI 8086:A7A0, revision 04 |
| EU | 96 according to Intel specifications; the full resource profile must be checked against this GPU's registers |
| Host bridge | 8086:A706 |
| Wi-Fi | Intel CNVi 8086:51F1 |
| Bluetooth | Intel AX211, USB 8087:0033 |
| Audio controller | Intel cAVS 8086:51CA |
| Audio codec | Conexant SN6140, 14F1:1F87 |
| NVMe controller | Phison PS5021-E21, 1987:5021 |
| Main USB controller | 8086:51ED |
| Keyboard | PS/2 |
| Touchpad | Synaptics S9801, 06CB:CEAD, I2C0 |
| Touchscreen | FTSC1000, 2808:5946, I2C1 |
| Camera | USB UVC, 3408:C200 |

## Confirmed ACPI nodes

- GPU: `\_SB.PC00.GFX0`.
- EC: `\_SB.PC00.LPCB.HWEC`.
- Keyboard: `\_SB.PC00.LPCB.PS2K`.
- Touchpad: `\_SB.PC00.TPD0`, connected to I2C0.
- S9801 branch: address 0x15, HID descriptor register 0x20, firmware bus speed 400 kHz.
- The STAS field controls the availability of AWAC and the legacy RTC.
- The DSDT root contains a 16-bit PNLF field. Do not blindly rename it as though it were a backlight device.
- The factory DSDT declares 64 CPU devices. This does not mean there are 64 physical processors and does not, by itself, prove an error.

## Measurements still needed

- Enabled APIC IDs and their correspondence to CPU objects.
- UEFI memory map and justification for MMIO exceptions.
- GPU GGC/GMS, L3/topology and frequencies.
- eDP lane count/link rate, PWM and the backlight control method.
- A USB port map for this laptop and the complete audio pin configuration.

These measurements do not require publishing any serial numbers or other unique identifiers.
