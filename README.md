# Energy or Carbon footprint from HPC



## Getting started

Comment calculer sa consommation énergétique et carbone à partir de sorties HPC ?

Nous allons voir deux méthodes :
- Avec GreenAlgorithm : permet une estimation grâce aux paramètres du HPC
- A la main, en additionnant la consommation de chacun des jobs (mesure logicielle)

## GreenAlgorithm

GreenAlgorithm (Lannelongue et al. (2021)) est un outil permettant le calcul de la consommation électrique et de son équivalent carbone d'une simulation numérique.

- Suivre l'installation depuis GIT : https://www.green-algorithms.org/GA4HPC/install
  
    → Si cela ne fonctionne pas : télécharger en local et transférer sur belenos.
  
- Télécharger le fichier des paramètres de Belenos (n'hésitez pas à en prendre connaissance) : cluster_info.yaml
  
    → Si votre version de python < 3.7 (python --version) : creer un environnement virtuel avec conda.

- Lancer l'outil :
```sh
   myCarbonFootprint.sh
```

→ Si cela ne fonctionne pas, lancer directement GreenAlgorithms_global.py.


Remarques :

- Les données sont calculées sur les simulations réalisées depuis le début de l'année calendaire.
- L'outil vous informe du TEI consommé (en jours) → Consommation énergétique (kWh) → Empreinte carbone (gCO2eq).
- Il est très important d'aller vérifier l'ordre de grandeur obtenu. Une possibilité :  obtenir le TEI de l'année par une commande de SLURM (/opt/softs/bin/sccompta -p USER). Faire la somme des TEI (Kh) et ramener en jours. Comparer.


## A la main : Récupérer le temps de calcul et la consommation de ses jobs

1) Préparation :

- Ajouter à son ~/.bashrc : PATH=$PATH:$HOME/bin
- Télécharger et placer le script : grep_tei_kwh.sh dans l'espace ~/bin/
- Créer le dossier ~/EcoStats
- Télécharger et placer le script : tei_kwh_prepare.sh dans l'espace ~/EcoStats/


2) Concaténer les temps de calcul et consommations :
```sh
   cd ~/Path/to/NameXP
   ./grep_tei_kwh.sh NameXP
```
→ Les résultats se situent dans le dossier ~/EcoStats


3) Au besoin, on peut concaténer les sorties 
 ```sh
   cd ~/EcoStats
   python3 tei_kwh_prepare.py NameXP_tei.txt; python3 tei_kwh_prepare.py NameXP_kwh.txt
 ```
NB : pour lire des fichiers ".pkl" sous python, on peut utiliser pandas :
 ```py
   df = pd.read_pickle('main_kwh_NameXP_kwh.pkl')
 ```


## Remerciements
Les codes de récupération ont été développés par Ghislain Faure.
