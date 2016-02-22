# salt-docker-integration

Source de présentation fournissant une solution de test d'intégration saltstack avec docker.

Organisation des sources :

* docker - Contient les Dockerfile salt-master et minion
* salt - Contient les pillars et states fournissant une installation de redis et le test du rôle redis.
* test_salt_roles.py - Test unitaire Python automatisant les tests de rôle SaltStack dans Docker

# Configuration Salt

Salt est configuré pour inclure dans le highstate le state commons.sls et le ou les states correspondant
au rôles listés dans le grain roles.

# Exécution locale

Pour exécuter les tests, il vous suffit de lancer le script run-all-tests.sh.

Il se charge de :

* Construire les images docker salt-master et salt-minion
* Créer un environnement Python virtualenv
* Installer les requirements du script Python de test
* Lancer le test avec nose2


# Exécution Vagrant

Le dépôt fournit un Vagrantfile permettant de lancer une machine virtualbox pré-configurée pour exécuter
les tests.

Lancez la machine avec vagrant :

```shell
$ vagrant up
```

Le premier vagrant up prendra un peu de temps car il se charge de provisionner le système et de créer
les images docker salt-minion et salt-master.

Lancez les tests sur la machine vagrant :

```shell
$ vagrant ssh
$ cd /srv/salt-test/salt-docker-integration
$ ./run-all-tests.sh
```

Les tests génèrent un rapport junit-xml dans le fichier `nose2-junit.xml`.
Ce fichier peut-être utilisé par Jenkins comme source de résultat des tests.
