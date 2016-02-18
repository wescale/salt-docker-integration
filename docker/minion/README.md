# Construction du salt-minion

Pour construire l'image lancez:

```shell
docker build --rm=true -t salt-minion
```

Pour lancer le conteneur:

```shell
docker run -tid --privileged --name="salt-minion" -v /sys/fs/cgroup:/sys/fs/cgroup:ro salt-minion
```

Cette commande doit vous présenter le démarrage de systemd.

Pour tester le bon fonctionnement du conteneur minion:

```shell
docker exec -ti salt-minion salt-call --local test.ping
```

Pour terminer le conteneur minion:

```shell
docker rm -f salt-minion
```
