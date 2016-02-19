{%- set roles = grains['roles'] -%}

base:
  '*':
    - commons
{%- for role in roles %}
  'roles:{{ role }}':
    - match: grain
    - {{ role }}
{%- endfor -%}
