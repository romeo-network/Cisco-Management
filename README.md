# Cisco-Management
Cet outil a pour but la gestion d'équipement **Cisco propulsé sous IOS** (IOS 12 & 15).

## Présentation:

Cet outil, à destination d’équipement Cisco propulsé sous IOS, a pour but :
- l’automatisation d’un ensemble d’instruction destiné à améliorer la sécurité
- la récupération des "running-config"
- le "factory reset" des équipements

## Compatibilité:

- C7200
- C3745
- C2960
- IOSvL2
- IOSvL3

## Pré-requis:

Afin d’utiliser cet outil, il sera nécessaire d’installer les bons paquets:

#### Sous Ubuntu:

<code>sudo apt install -y python3-pip </code>

<code>sudo apt install -y build-essential libssl-dev libffi-dev </code>

<code>sudo apt install -y python3-dev </code>

<code>python3 -m pip install cryptography</code>

<code>python3 -m pip install netmiko</code>

## Installation:
<code>chmod +x cisco_management.py</code>

## Configuration:

### Configuration SSH:

Afin de pouvoir utiliser ce script, il est nécessaire de configurer le SSH sur les équipements et d'avoir initié une première connexion sur ces derniers.

### Préparation 'router.list' et 'switch.list':

Vous devrez renseigner dans les fichiers ‘switch.list’ et ‘router.list’, toutes les adresses IP de vos commutateurs sous forme X.X.X.X.

Exemple:

![IP2](https://user-images.githubusercontent.com/55896009/77539246-57336f00-6ea1-11ea-826e-a7fd5d39ff82.JPG)

### Préparation des fichiers 'CONFIGURATION_L2' et 'CONFIGURATION_L3:

Dans les fichiers ‘configuration_l3’ et ‘configuration_l2’, se trouvent les instructions qui seront envoyées aux équipements.
Avant d’ajouter des instructions dans ces fichiers, il est vivement conseillé de les tester directement sur au moins un équipement, afin de s'assurer du comportement en résultant.
De plus, si vous utilisez les fichiers fournis ici, adapter la 'range' des 'line vty' selon vos besoins. 

Le fichier 'CONFIGURATION_COMMENTED' explique brièvement l'usage des commandes, **ne pas l'utiliser avec ce script.**

### Préparation de la fonction 'save()':

Il faudra définir la destination de la sauvegarde, via la variable 'bckp_path'.

### Préparation de la fonction 'reload()':

La fonction 'reload' permet de planifier le redémarrage des équipements au bout de 2min, par défaut.
Valeur minimum 1min, le programme ne pourra pas se terminer correctement si l'équipement redémarre pendant l'envoie d'instruction.

#### Point particulier concernant GNS3:
Si vous utilisez ce script avec GNS3, sur un IOSvL2, la valeur 'config-register' est à 0x0. Le mode ROMMON n'étant pas supporté pour la changer, l'envoie d'un 'reload' via SSH, sera impossible. Pensez donc, dans ce cas, à modifier la fonction comme suit:

![reload](https://user-images.githubusercontent.com/55896009/77462156-00c42300-6e04-11ea-92ef-d671cf7c090b.jpg)

De plus, certains IOS (c7200, c3745, c3725) figent lors d'un 'reload'. Privilégier l'utilisation d'IOSvL3 dans ce cas. ([En savoir plus](https://gns3.com/community/discussion/problem-with-reload-c3725-3745))

Enfin, suite à un 'write erase', il se peut que l'équipement émulé ne fasse pas apparaître un prompt de type:

'System configuration has been modified. Save? [yes/no]'

Auquel cas, modifier la fonction 'reload' comme suit:

![RELOAD_NO](https://user-images.githubusercontent.com/55896009/77533876-fd7a7700-6e97-11ea-92ae-b91ac88b856a.jpg)

## Utilisation:

<code>python3 cisco_management.py</code>

### Menu avec 3 actions possibles:

#### Configuration avancée:
Cette fonctionnalité permet d’envoyer une liste d’instruction visant à:
- Vérifier si l'équipement a déjà été configuré par ce script
- Désactiver les services non utilisés
- Amélioration de la sécurité

#### Sauvegarde:
Cette fonctionnalité permet de récupérer les 'running-config' sous forme de fichier '.txt', et de le sauvegarder dans le repértoire définit dans la variable 'path_backup', se trouvant dans la fonction 'save'. Le dossier aura pour nom, le 'hostname'.

#### Effacement intégral:
Cette foncionnalité permet de faire un effacement:
- de la ‘startup-config’
- du fichier ‘vlan.dat’ pour les commutateurs

Et, de planifier un redémarrage des équipements.

## Licence
![IP](https://img.shields.io/badge/Licence-GPL--3.0-red)                                  

##
###### Ajouté le 24/03/2020
###### Dernière mise à jour le 31/03/2020
