redis-server:
  pkg.installed:
    - name: redis

  file.managed:
    - name: /etc/redis.conf
    - makedirs: true
    - template: jinja
    - source: salt://redis/files/redis.conf
    - user: root
    - group: root
    - mode: 644
    - require:
        - pkg: redis-server

  selinux.mode:
    - name: permissive

  service.running:
    - name: redis
    - enable: True
    - restart: True
    - watch:
        - pkg: redis-server
        - file: /etc/redis.conf
        - selinux: redis-server

  pip.installed:
    - name: redis

