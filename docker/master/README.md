# Construction du salt-master

Pour construire l'image lancez:

```shell
docker build --rm=true -t salt-master
```

Pour lancer le conteneur:

```shell
docker run -tid --name="salt-master" -v.:/srv/salt salt-master
```

Cette commande doit vous présenter le démarrage de systemd.

Pour tester le bon fonctionnement du conteneur master:

```shell
docker exec -ti salt-master salt-run manage.versions
```

Pour terminer le conteneur master:

```shell
docker rm -f salt-master
```

