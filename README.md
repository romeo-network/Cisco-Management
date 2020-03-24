# Cisco-Management
Cet outil a pour but la gestion d'équipement **Cisco propulsé sous IOS**.

## Présentation:

Cet outil, à destination d’équipement Cisco propulsé sous IOS, a pour but :
- l’automatisation d’un ensemble d’instruction destiné à améliorer la sécurité
- la récupération des "running-config"
- le "factory reset" des équipements

## Compatibilité:

- C7200
- C3745
- C2960

## Pré-requis:

Afin d’utiliser cet outil, il sera nécessaire d’installer les bons paquets:

#### Sous Ubuntu:

sudo apt install -y python3-pip

python3 -m pip install netmiko

## Installation:
chmod +x cisco_management.py

## Configuration:

### Préparation 'router.list' et 'switch.list':

Vous devrez renseigner dans les fichiers ‘switch.list’ et ‘router.list’, toutes les adresses IP de vos commutateurs sous forme X.X.X.X

Exemple:

![IP](https://user-images.githubusercontent.com/55896009/77462720-cc9d3200-6e04-11ea-9684-c545b4ab7d2a.JPG)

Dans les fichiers ‘configuration_l3’ et ‘configuration_l2’, se trouvent les instructions qui seront envoyés aux équipements.
Avant d’ajouter des instructions dans ces fichiers, il est vivement conseillé de les tester directement sur au moins un équipement, afin de s'assurer du comportement en résultant.

### Préparation de la fonction 'save':

Il faudra définir la destination de la sauvegarde, via la variable 'bckp_path'.

### Préparation de la fonction 'reload':

La fonction 'reload' permet de planifier le redémarrage des équipements au bout de 2min, par défaut.
Valeur minimum 1min, le programme ne pourra pas se terminer correctement si l'équipement redémarre pendant l'envoie d'instruction.

#### Point particulier concernant GNS3:
Si vous utilisez ce script avec GNS3, sur un IOSvL2, la valeur 'config-register' est à 0x0. Le mode ROMMON n'étant pas supporté pour la changer, l'envoie d'un 'reload' via SSH, sera impossible. Pensez donc, dans ce cas, à modifier la fonction comme suit:

![reload](https://user-images.githubusercontent.com/55896009/77462156-00c42300-6e04-11ea-92ef-d671cf7c090b.jpg)

De plus, certains IOS (c7200, c3745, c3725) figent lors d'un 'reload'. Les redémarrer manuellement via un clic droit et 'reload' directement avec GNS3.

## Utilisation:

python3 cisco_management.py

### Menu avec 3 actions possibles:

#### Sécurisation:
Cette fonctionnalité permet d’envoyer une liste d’instruction visant à:
- Vérifier si l'équipement a déjà été configuré par ce script
- Désactiver les services non utilisés
- Amélioration de la sécurité

#### Sauvegarde:
Cette fonctionnalité permet de récupérer les 'running-config' sous forme de fichier '.txt', et de le sauvegarder dans le repértoire définit dans la variable 'path_backup', se trouvant dans la fonction 'save'. Le dossier aura pour nom, le 'hostname'.

#### Factory reset:
Cette foncionnalité permet de faire un effacement:
- de la ‘startup-config’
- du fichier ‘vlan.dat’ pour les commutateurs

Et, de planifier un redémarrage des équipements.
