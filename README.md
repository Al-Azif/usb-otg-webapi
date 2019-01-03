USB OTG via WebAPI
==================

## Purpose
Cheap (<$50) remote viewing/control of devices on which you cannot install remote control software but can use a USB keyboard.

## My Primary Setup
- PS4
- Raspberry Pi Zero W connected via USB and UART
- Official Raspberry Pi 8MP camera pointed at the screen

## But you can just run your own software controls on the system...
There is currently no public coldboot available to run your own code, meaning there is no screen streaming/control on boot

## Roadmap
- [ ] Camera Stream (Find a better method/Tweak existing method)
- [ ] Macro Support (Multiple commands contained in one neat command)
- [ ] "On Boot" Support (Run a macro when power is detected on the system, or other external trigger)
- [ ] UART Support
- [ ] Power/Eject API (Control physical buttons)
- [ ] Secure login vs static auth-key
- [ ] Single script setup
- [ ] Documentation
