#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from getpass import getpass
from datetime import datetime
import getpass
import time
import os
import errno
import sys
import config


print("Entrez vos informations de connexion: ")
username = input("Username: \n")
password = getpass.getpass("Password: \n")


def security():
    start_time = datetime.now()

    with open('CONFIGURATION_L2') as f:
        lines_l2 = f.read().splitlines()
    with open('switch.list') as f:
        ip_sw = f.read().splitlines()

    for ip in ip_sw:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
                }        
        net_connect = ConnectHandler(**device)  
        try:                    
            result= net_connect.send_command("show running-config | inc ip access-list standard SSH")
        except (NetMikoTimeoutException):
            print ("Délai d'attente dépassé.  " +ip)
        if "ip access-list standard SSH" in result:
            net_connect.disconnect()
        else:
            output = net_connect.send_config_set(lines_l2)
            time.sleep(5)
            net_connect.disconnect()
            print(output)


    with open('CONFIGURATION_L3') as f:
         lines = f.read().splitlines()
    with open('router.list') as f:
         ip_rtr = f.read().splitlines()

    for ip in ip_rtr:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
                }
        
        net_connect = ConnectHandler(**device) 

        try:                   
            result= net_connect.send_command("show running-config | inc ip access-list standard SSH")
        except (NetMikoTimeoutException):
            print ("Délai d'attente dépassé. " + ip)
        if "ip access-list standard SSH" in result:
            net_connect.disconnect()
        else:
            output = net_connect.send_config_set(lines)
            time.sleep(5)
            net_connect.disconnect()
            print(output)

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de la sécurisation: "+str(total_time)+"\n")


def reload():

    with open('router.list') as f:
        ip_rtr = f.read().splitlines()

    for ip in ip_rtr: 
        device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
         }                
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('reload in 5', '\n') 
        time.sleep(0.5)
        output += net_connect.send_command('no\n', expect_string='confirm')
        time.sleep(0.5)
        output += net_connect.send_command('\n')
        time.sleep(0.5)
        net_connect.disconnect()

def wipeout():
    start_time = datetime.now()

    with open('switch.list') as f:
        ip_sw = f.read().splitlines()
    
    for ip in ip_sw:
        device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
         }
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('delete vlan.dat', '\n')
        time.sleep(0.5)
        output = net_connect.send_command('vlan.dat\n', expect_string='confirm')
        time.sleep(0.5)
        output = net_connect.send_command('\n')
        time.sleep(0.5)
        output += net_connect.send_command('write erase', expect_string='confirm')
        time.sleep(0.5)
        output += net_connect.send_command('\n')
        net_connect.disconnect()

    with open('router.list') as f:
        ip_rtr = f.read().splitlines()
    
    for ip in ip_rtr:
        device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
         }                
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('write erase', expect_string='confirm')
        time.sleep(0.5)
        output += net_connect.send_command('\n')
        net_connect.disconnect()

    reload()

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de l'effacement: "+str(total_time)+"\n")

def save():
    start_time = datetime.now()

    with open('router.list') as f:
        ip_rtr = f.read().splitlines()
    with open('switch.list') as f:
        ip_sw = f.read().splitlines()

    ip_add = ip_rtr + ip_sw
  
    for ip in ip_add:        
  
        device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
         }

        net_connect = ConnectHandler(**device)        
        def hostname():            
            sh_check = net_connect.send_command("show running-config | in hostname")
            hostname = sh_check.split()
            return hostname[1]           
        try:
            os.makedirs("DIRECTORY" + hostname())
        except OSError as exc: 
            if exc.errno == errno.EEXIST and os.path.isdir("DIRECTORY" + hostname()):
                pass

        bckp = net_connect.send_command("show running-config")              
        now = datetime.now()
        date = now.strftime("%d_%m_%Y_%H:%M:%S")
        path_backup = "DIRECTORY/{0}/{1}.txt".format(hostname(),date)        
        with open(path_backup, "a") as file:
            file.write(bckp + "\n")
        net_connect.disconnect()  

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de la sauvegarde: "+str(total_time)+"\n")

def main():

    choice ='0'
    while choice =='0':
        print("Menu principal: choix disponible 1 à 4. \n")
        print("Choisir '1' pour l'amélioration de la configuration. ")
        print("Choisir '2' pour la sauvegarde intégrale. ")
        print("Choisir '3' pour l'effacement intégral. ")
        print("Choisir '4' pour quitter le script. \n")
       
        choice = input ("Faites un choix: ")

    if choice == "4":
        print("\nFin du script.")
        sys.exit()
	        
    elif choice == "3":
        print("\nEffacement intégral. ")
        wipeout()
        time.sleep(0.5)
        main()

    elif choice == "2":
        print("\nSauvegarde intégrale. ")
        save()
        time.sleep(0.5)
        main()

    elif choice == "1":
        print("\nConfiguration IOS. ")
        security()
        time.sleep(0.5)
        main()

    else:
        print("\nChoix invalide. \n")
        main()

main()
