/*
 * MateBook 14s HKFG, i7-13700H: Darwin-only Synaptics I2C touchpad.
 * Observed hardware: I2C0 00:15.0, S9801 / 06CB:CEAD, address 0x15,
 * firmware HID descriptor register 0x20, bus frequency 400 kHz.
 *
 * Native TPD0 is a PC00 sibling of I2C0. VoodooI2C enumerates controller
 * children, so provide a Darwin-only child with the same HID protocol.
 * Preserve native TPD0 initialization; do not change global OS identification
 * or write GPIO registers. Use -vi2c-force-polling for this initial input test.
 * Expose the I2C descriptor only: upstream accepts a polled child without an
 * interrupt. A valid APIC descriptor would override force-polling, so do not
 * advertise an unverified interrupt route. Touchscreen I2C1 is outside this change.
 *
 * Requires exact DSDT-only rename of I2C0._PS3 to XPS3. The original
 * power-down method clears BAR0, while _PS0 does not restore it. Suppress
 * that method only under Darwin; retain its original behavior for other OSes.
 */
DefinitionBlock ("", "SSDT", 2, "HUAWEI", "HWINPUT", 0x00000001)
{
    External (_SB_.PC00.I2C0, DeviceObj)
    External (_SB_.PC00.I2C0._PS0, MethodObj)
    External (_SB_.PC00.I2C0.XPS3, MethodObj)
    External (_SB_.PC00.TPD0._HID, StrObj)

    Scope (_SB.PC00.I2C0)
    {
        Method (_PS3, 0, NotSerialized)
        {
            If (!_OSI ("Darwin"))
            {
                XPS3 ()
            }
        }

        Device (TPDX)
        {
            Method (_HID, 0, NotSerialized)
            {
                Return (\_SB.PC00.TPD0._HID)
            }
            Name (_CID, "PNP0C50")
            Name (_UID, One)
            Name (_S0W, 0x03)

            Method (_STA, 0, NotSerialized)
            {
                If (_OSI ("Darwin"))
                {
                    Return (0x0F)
                }
                Return (Zero)
            }

            Name (I2CR, ResourceTemplate ()
            {
                I2cSerialBusV2 (0x0015, ControllerInitiated, 0x00061A80,
                    AddressingMode7Bit, "\\_SB.PC00.I2C0",
                    0x00, ResourceConsumer, , Exclusive,)
            })

            Method (_CRS, 0, Serialized)
            {
                Return (I2CR)
            }

            Method (_DSM, 4, Serialized)
            {
                If ((Arg0 == ToUUID ("3cdff6f7-4267-4555-ad05-b30a3d8938de")))
                {
                    If ((Arg1 == One))
                    {
                        If ((Arg2 == Zero))
                        {
                            Return (Buffer (One) { 0x03 })
                        }
                        If ((Arg2 == One))
                        {
                            Return (0x20)
                        }
                    }
                }
                Return (Buffer (One) { 0x00 })
            }
        }
    }
}
