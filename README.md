# Cisco Management Tool

This tool automates the management of Cisco devices running IOS (versions 12 & 15).

## Overview

The Cisco Management Tool is designed to:
- Automate security-enhancing configurations.
- Retrieve and save "running-config" files.
- Perform factory resets on devices.

## Compatibility

- C7200
- C3745
- C2960
- IOSvL2
- IOSvL3

## Prerequisites

To use this tool, you need to install the following packages:

### On Ubuntu:

```bash
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install -y python3-dev
python3 -m pip install cryptography
python3 -m pip install netmiko
```

## Installation

Make the script executable:

```bash
chmod +x cisco_management.py
```

## Configuration

### SSH Configuration

Ensure SSH is configured on your devices and that you have established an initial connection.

### IP Lists

Populate the `router.list` and `switch.list` files with the IP addresses of your devices in the format X.X.X.X.

### Configuration Files

The `CONFIGURATION_L2` and `CONFIGURATION_L3` files contain the commands to be sent to the devices. Test these commands on at least one device before adding them to the files. Adjust the `line vty` range as needed.

### Backup Path

Define the backup destination in the `save()` function using the `bckp_path` variable.

### Reload Function

The `reload()` function schedules a device reboot after 2 minutes by default. Ensure the device does not reboot during command execution.

## Usage

Run the script:

```bash
python3 cisco_management.py
```

### Menu Options

1. **Advanced Configuration**:
   - Checks if the device has been configured by this script.
   - Disables unused services.
   - Enhances security settings.

2. **Backup**:
   - Retrieves the "running-config" and saves it as a `.txt` file in the specified backup directory, named after the device's hostname.

3. **Full Erase**:
   - Erases the `startup-config` and `vlan.dat` file for switches.
   - Schedules a device reboot.

## License

![License](https://img.shields.io/badge/License-GPL--3.0-red)
