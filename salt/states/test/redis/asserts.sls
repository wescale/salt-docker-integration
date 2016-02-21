# salt/states/test/redis/asserts.sls
# Redis server pid

{%- set redis_pid = salt['cmd.run']('pgrep -f redis-server') -%}

# check redis is listening as needed
test.docker-roles::redis::listen:
  cmd.run:
  - name: lsof -iTCP@0.0.0.0:{{ salt['pillar.get']('redis:port', '6379') }} -a -p {{ redis_pid }}

# Insert a key inside the running redis server
test.docker-roles::redis::insert:
  redis.string:
    - value: Test string data in redis
    - host: localhost
    - port: {{ salt['pillar.get']('redis:port', '6379') }}
    - db: 0
