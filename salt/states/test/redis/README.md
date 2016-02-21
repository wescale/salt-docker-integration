Test d'intégration salt dans Docker pour Redis.

Les grains `test_grains` définissent le rôle `redis`.
Le state asserts.sls vérifie que Redis écoute bien sur le port '6397' comme défini dans les pillars et injecte une clé
dans la base redis.
