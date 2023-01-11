# Projet-Poker

Le but du projet est de créer un jeu de Poker Texas Hold'Em faisant intervenir joueurs humains et intelligences artificielles en mettant en oeuvre les algorithmes de la théorie des jeux et de l'apprentissage statistique.

Le jeu permettra à des humains de s'affronter et d'affronter des IA, le tout en réseau.

Le jeu de Poker comportera plusieurs modules :
- Un serveur, hébergé sur une machine en réseau local
- Un logiciel client humain avec une interface graphique
- Un logiciel client IA, avec possiblement plusieurs variantes d'IA. (Jeu au hasard, jeu agressif, par auto-apprentissage)
- Un protocole de communication entre clients et serveur

Pour que le projet puisse fonctionner sur Linux, Windows et Mac, le langage et les bibliothèques utilisés seront (à peu près) libres.

# Comment jouer 

- Lancer le serveur dans `src/rules/` : 
```{bash}
python server.py
```
- Lancer le client dans `src/poker/` : 
```{bash}
python main.py
```

# Ressources 
Le dossier de stockage des fichiers annexes (Cahier des charges, planning & ressources éducatives) est accessibles à l'aide du lien suivant (https://drive.google.com/drive/folders/1wyqECV4-QQn1gJoVZwRgfn_wUfKAfKLP?usp=sharing).
