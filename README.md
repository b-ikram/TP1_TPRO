# Shortest Cycle Finder – Graph GUI

 **Date** : 02/11/2025  
 **Module** : TPRO  
 **Auteur** : Ikram Badaoui  
 **Langage** : Python  
  

---

##  Description

Ce projet est une application graphique interactive permettant de **créer un graphe non orienté**, puis de **détecter et visualiser les cycles les plus courts** (shortest cycles) dans ce graphe.

L’utilisateur peut :
- ajouter des sommets (nœuds),
- créer ou supprimer des arêtes,
- supprimer des éléments,
- lancer un algorithme de détection des **cycles de longueur minimale**,
- visualiser **tous les cycles minimaux** trouvés avec des couleurs distinctes.

---

##  Objectifs pédagogiques

- Manipulation de graphes (représentation, parcours)
- Implémentation d’un algorithme basé sur **BFS**
- Détection de cycles dans un graphe non orienté
- Développement d’une **interface graphique (GUI)** en Python
- Visualisation algorithmique (graphes, cycles)

---

##  Fonctionnalités

###  Création du graphe
- Ajout de nœuds par clic sur le canvas
- Ajout d’arêtes en sélectionnant deux nœuds
- Suppression de nœuds ou d’arêtes

###  Analyse du graphe
- Détection du **plus court cycle**
- Recherche de **tous les cycles de longueur minimale**
- Affichage du résultat textuel
- Mise en évidence graphique des cycles (couleurs différentes)

###  Interface utilisateur
- Interface simple et intuitive
- Modes distincts :
  - Add Nodes
  - Add Edges
  - Delete
- Visualisation dynamique sur canvas

---

##  Algorithme utilisé

- **Parcours en largeur (BFS)** à partir de chaque sommet
- Calcul des distances et des parents
- Détection d’un cycle lorsqu’une arête relie deux sommets déjà visités
- Reconstruction du cycle à partir des parents
- Conservation uniquement des **cycles de longueur minimale**

Complexité approximative :
- **Temps** : \( O(V \cdot (V + E)) \)
- **Espace** : \( O(V + E) \)

---

##  Exécution du programme

### Prérequis
- Python 3.x
- Tkinter (inclus par défaut avec Python)

