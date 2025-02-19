#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Version 2.0
# Updated: 19/02/2025
# License: GPL-3.0
# Author: romeo-network

import argparse
import logging
import os
import sys
import time
from datetime import datetime
from getpass import getpass
from typing import List

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to read IP addresses from a file
def read_ip_addresses(file_path: str) -> List[str]:
    with open(file_path) as file:
        return file.read().splitlines()

# Function to read configuration lines from a file
def read_configuration(file_path: str) -> List[str]:
    with open(file_path) as file:
        return file.read().splitlines()

# Function to configure devices
def configure_devices(ip_addresses: List[str], config_lines: List[str], username: str, password: str):
    for ip in ip_addresses:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        try:
            with ConnectHandler(**device) as net_connect:
                result = net_connect.send_command("show running-config | inc ip access-list standard SSH")
                if "ip access-list standard SSH" in result:
                    net_connect.save_config()
                else:
                    output = net_connect.send_config_set(config_lines)
                    net_connect.save_config()
                    logging.info(f"Configured {ip}: {output}")
        except NetMikoTimeoutException:
            logging.error(f"Timeout error for {ip}")

# Function to reload devices
def reload_devices(ip_addresses: List[str], username: str, password: str):
    for ip in ip_addresses:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        try:
            with ConnectHandler(**device) as net_connect:
                net_connect.send_command('reload in 5', expect_string=r'confirm')
                net_connect.send_command('no')
                logging.info(f"Reload scheduled for {ip}")
        except NetMikoTimeoutException:
            logging.error(f"Timeout error for {ip}")

# Function to wipe out configurations
def wipeout_configurations(ip_addresses: List[str], username: str, password: str):
    for ip in ip_addresses:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        try:
            with ConnectHandler(**device) as net_connect:
                net_connect.send_command('delete vlan.dat', expect_string=r'confirm')
                net_connect.send_command('write erase', expect_string=r'confirm')
                logging.info(f"Wiped configuration for {ip}")
        except NetMikoTimeoutException:
            logging.error(f"Timeout error for {ip}")

# Function to save configurations
def save_configurations(ip_addresses: List[str], username: str, password: str):
    for ip in ip_addresses:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        try:
            with ConnectHandler(**device) as net_connect:
                hostname = net_connect.send_command("show running-config | in hostname").split()[1]
                backup_dir = f"/home/cisco/{hostname}"
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = f"{backup_dir}/{datetime.now().strftime('%d_%m_%Y_%H:%M:%S')}.txt"
                with open(backup_path, "w") as file:
                    file.write(net_connect.send_command("show running-config"))
                logging.info(f"Saved configuration for {ip} to {backup_path}")
        except NetMikoTimeoutException:
            logging.error(f"Timeout error for {ip}")

# Main function to handle command-line arguments
def main():
    parser = argparse.ArgumentParser(description="Network Device Management Script")
    parser.add_argument("--config", action="store_true", help="Configure devices")
    parser.add_argument("--reload", action="store_true", help="Reload devices")
    parser.add_argument("--wipeout", action="store_true", help="Wipe out configurations")
    parser.add_argument("--save", action="store_true", help="Save configurations")
    parser.add_argument("--username", required=True, help="Username for device login")
    parser.add_argument("--password", help="Password for device login (will prompt if not provided)")

    args = parser.parse_args()

    if not args.password:
        args.password = getpass("Password: ")

    switch_ips = read_ip_addresses('switch.list')
    router_ips = read_ip_addresses('router.list')
    config_l2 = read_configuration('CONFIGURATION_L2')
    config_l3 = read_configuration('CONFIGURATION_L3')

    if args.config:
        configure_devices(switch_ips, config_l2, args.username, args.password)
        configure_devices(router_ips, config_l3, args.username, args.password)
    elif args.reload:
        reload_devices(switch_ips + router_ips, args.username, args.password)
    elif args.wipeout:
        wipeout_configurations(switch_ips + router_ips, args.username, args.password)
        reload_devices(switch_ips + router_ips, args.username, args.password)
    elif args.save:
        save_configurations(switch_ips + router_ips, args.username, args.password)
    else:
        logging.error("No valid action specified. Use --config, --reload, --wipeout, or --save.")

if __name__ == "__main__":
    main()
