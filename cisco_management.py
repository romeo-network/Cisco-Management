#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Version 1.1
#25/03/2020

#Importation des modules nécessaires.
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from getpass import getpass
from datetime import datetime
import getpass
import calendar
import time
import os
import errno
import sys

#Récupération des informations d'identifications 
print("Entrez vos informations de connexion: ")
username = input("Username: \n")
password = getpass.getpass("Password: \n")

#Fonction destinée à propulser un fichier de configuration vers les équipements.
def configuration():
    start_time = datetime.now()
    
    #Ouverture du fichier de configuration et du fichier contenant les IP des commutateurs.
    with open('CONFIGURATION_L2') as f:
        lines_l2 = f.read().splitlines()
    with open('switch.list') as f:
        ip_sw = f.read().splitlines()
        
    #Boucle autant de fois qu'il y a de ligne dans le fichier 'switch.list'.
    for ip in ip_sw:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
                }        
        net_connect = ConnectHandler(**device)  
        #Vérifie la présence d'une ligne de configuration issu du fichier 'CONFIGURATION_L2', si résultat positif: n'envoie rien.
        #Sauvegarde la 'running-config' dans la 'startup-config' dans les 2 cas.
        try:                    
            result= net_connect.send_command("show running-config | inc ip access-list standard SSH")
        except (NetMikoTimeoutException):
            print ("Délai d'attente dépassé.  " +ip)
        if "ip access-list standard SSH" in result:
            net_connect.save_config()
            time.sleep(0.5)
            net_connect.disconnect()
            
        #Envoie l'intégralité du contenu du fichier de configuration.
        else:
            output = net_connect.send_config_set(lines_l2)
            time.sleep(1)
            net_connect.save_config()
            time.sleep(0.5)
            net_connect.disconnect()
            print(output)

    #Ouverture du fichier de configuration et du fichier contenant les IP des routeurs.
    with open('CONFIGURATION_L3') as f:
         lines = f.read().splitlines()
    with open('router.list') as f:
         ip_rtr = f.read().splitlines()
         
         
    #Boucle autant de fois qu'il y a de ligne dans 'router.list'.
    for ip in ip_rtr:
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
                }
        
        net_connect = ConnectHandler(**device) 
        #Vérifie la présence d'une ligne de configuration issue de 'CONFIGURATION_L3', si résultat positif; n'envoie rien.
        #Sauvegarde la 'running-config' dans la 'startup-config' dans les 2 cas.
        try:                   
            result= net_connect.send_command("show running-config | inc ip access-list standard SSH")
        except (NetMikoTimeoutException):
            print ("Délai d'attente dépassé. " + ip)
        if "ip access-list standard SSH" in result:
            net_connect.save_config()
            time.sleep(0.5)
            net_connect.disconnect()
            
        #Envoie l'intégralité du contenu du fichier de configuration
        
        else:
            output = net_connect.send_config_set(lines)
            time.sleep(1)
            net_connect.save_config()
            time.sleep(0.5)
            net_connect.disconnect()
            print(output)

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de la configuration: "+str(total_time)+"\n")

#Fonction destinée à redémarrer les équipements.
def reload():

    with open('router.list') as f:
        ip_rtr = f.read().splitlines()

    with open('switch.list') as f:
        ip_sw = f.read().splitlines()
    ip_add = ip_rtr + ip_sw
    

    #Pour chaque ligne présente, boucle et envoie des instructions de redémarrage.
    for ip in ip_add: 
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

#Fonction destiné à supprimer les fichiers de configurations des équipements.
#Appelle la fonction 'reload()' une fois terminée.
def wipeout():
    start_time = datetime.now()

    with open('switch.list') as f:
        ip_sw = f.read().splitlines()
    
    #Boucle autant de fois qu'il y a de ligne, et envoie des instructions d'effacement des fichiers vlan.dat et startup-config.
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
        
    #Boucle autant de fois qu'il y a de ligne, et envoie des instructions d'effacement de la startup-config.
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
    #Appelle la fonction 'reload()'
    reload()

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de l'effacement: "+str(total_time)+"\n")
    

#Fonction destinée à sauvegarder les configurations des équipements
def save():
    start_time = datetime.now()

    with open('router.list') as f:
        ip_rtr = f.read().splitlines()
    with open('switch.list') as f:
        ip_sw = f.read().splitlines()
        
    #Addition de liste.
    ip_add = ip_rtr + ip_sw
  
    #Boucle autant de fois qu'il y a de ligne dans la liste.
    #Récupère les configurations des équipements.
    for ip in ip_add:        
  
        device = {
        'device_type': 'cisco_ios',
        'ip': ip,
        'username': username,
        'password': password,
         }

        net_connect = ConnectHandler(**device)        
        #Récupération du hostname pour nommer le dossier de sauvegarde
        def hostname():            
            sh_hstn = net_connect.send_command("show running-config | in hostname")
            hostname = sh_hstn.split()
            return hostname[1]           
            
        #Ici, on obtient l'équivalent d'un 'mkdir -p' pour l'idempotence.
        try:
            os.makedirs("/home/osboxes/Documents/cisco/" + hostname())
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir("/home/osboxes/Documents/cisco/" + hostname()):
                pass
                
        #Création des fichiers en local, et y incorpore le résultat du 'show running-config'.
        bckp = net_connect.send_command("show running-config")              
        now = datetime.now()
        date = now.strftime("%d_%m_%Y_%H:%M:%S")
        bckp_path = "/home/osboxes/Documents/cisco/{0}/{1}.txt".format(hostname(),date)        
        with open(bckp_path, "a") as file:
            file.write(bckp + "\n")
        net_connect.disconnect()  

    end_time = datetime.now()
    total_time = end_time - start_time
    print("Durée de la sauvegarde: "+str(total_time)+"\n")


#Fonction servant à obtenir un dossier, en bouclant à l'infini sur '0'.
def main():

    choice ='0'
    while choice =='0':
        print("Menu principal: choix disponible 1 à 4. \n")
        print("Choisir '1' pour la configuration avancée. ")
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
        print("\nConfiguration des IOS. ")
        configuration()
        time.sleep(0.5)
        main()

    else:
        print("\nChoix invalide. \n")
        main()

main()
