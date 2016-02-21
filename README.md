# salt-docker-integration

Source de présentation fournissant une solution de test d'intégration saltstack avec docker.

Organisation des sources :

* docker - Contient les Dockerfile salt-master et minion
* salt - Contient les pillars et states fournissant une installation de redis et le test du rôle redis.
* test_salt_roles.py - Test unitaire Python automatisant les tests de rôle SaltStack dans Docker


# Exécution

Pour exécuter les tests, il vous suffit de lancer le script run-all-tests.sh.

Il se charge de :

* Construire les images docker salt-master et salt-minion
* Créer un environnement Python virtualenv
* Installer les requirements du script Python de test
* Lancer le test avec nose2


