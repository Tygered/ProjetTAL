Avant d'exécuter ce projet, vérifier que le dossier data/generated est vide.
Ce répertoire accueillera les fichiers générés par le script.

Exécuter le fichier scripts.py répond au différentes questions du sujet de projet
et génère les différents fichiers demandés (traduction aux formats universitaires/CoNLL).

Il n'est pas nécessaire de relancer les analyses POS/NE.
Des fichiers résultats sont déjà placés dans le dossier data/taggings.

Afin de lancer le projet, se placer dans le dossier src, et executer la commande suivante: 

python scripts.py



Executer ensuite à part les commandes d'évaluation :

python evaluate.py ../data/generated/pos_test.txt.pos.lima.univ ../data/pos_reference.txt.univ

python evaluate.py ../data/generated/pos_test.txt.pos.stanford.univ ../data/pos_reference.txt.univ

python evaluate.py ../data/generated/pos_test.txt.pos.nltk.univ ../data/pos_reference.txt.univ



python evaluate.py ../data/generated/ne_test.txt.ne.lima.conll ../data/ne_reference.txt.conll

python evaluate.py ../data/generated/ne_test.txt.ne.stanford.conll ../data/ne_reference.txt.conll

python evaluate.py ../data/generated/ne_test.txt.ne.nltk.conll ../data/ne_reference.txt.conll
