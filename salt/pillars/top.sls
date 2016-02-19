{%- set roles = grains['roles'] -%}

base:
  '*':
     - mine
{%- for role in roles %}
  'roles:{{ role }}':
    - match: grain
    - {{ role }}
{%- endfor -%}
