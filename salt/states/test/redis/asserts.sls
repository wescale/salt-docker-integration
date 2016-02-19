# Carbon daemons pids

{%- set redis_pid = salt['cmd.run']('pgrep -f redis-server') -%}

# check carbon relay connectors

test.docker-roles::redis::listen:
  cmd.run:
  - name: lsof -iTCP@0.0.0.0:6379 -a -p {{ redis_pid }}
